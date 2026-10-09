import os
from flask import Flask, jsonify, render_template, request, session, redirect, url_for
from markupsafe import Markup
from dotenv import load_dotenv

from app.config.config import BASE_DIR, GROQ_API_KEY
from app.components.retriever import create_qa_chain
from app.common.logger import get_logger

logger = get_logger(__name__)

# Ensure .env is loaded
env_file = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_file):
    load_dotenv(dotenv_path=env_file)
else:
    load_dotenv()

app = Flask(__name__)

# Use persistent secret key so sessions survive server restarts
secret_key = os.environ.get("FLASK_SECRET_KEY")
if os.environ.get("VERCEL") and not secret_key:
    raise RuntimeError("FLASK_SECRET_KEY must be configured in Vercel environment variables.")
app.secret_key = secret_key or "neuramed-local-development-key"

def nl2br(value):
    if not value:
        return ""
    return Markup(str(value).replace("\n", "<br>\n"))

app.jinja_env.filters['nl2br'] = nl2br

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET" and request.args.get("keep_chat") != "1":
        session.pop("messages", None)

    if "messages" not in session:
        session["messages"] = []

    if request.method == "POST":
        user_input = request.form.get("prompt")

        if user_input and user_input.strip():
            user_input = user_input.strip()
            messages = session.get('messages', [])

            messages.append({"role": "user", "content": user_input})
            # Cap session messages to recent 10 turns to avoid 4KB cookie overflow
            session["messages"] = messages[-10:]

            try:
                if not GROQ_API_KEY:
                    raise Exception("GROQ_API_KEY is not set. Add a valid key to the project-root .env file and restart the server.")

                qa_chain = create_qa_chain()
                if qa_chain is None:
                    raise Exception("QA chain could not be created. Please verify your GROQ_API_KEY in .env and ensure vectorstore/db_faiss exists.")

                response = qa_chain.invoke({"query": user_input})

                result = response.get("result", "No response received.")
                # Clean Unicode replacement character (common with smart quotes/ligatures from PDFs)
                if isinstance(result, str):
                    result = result.replace("\ufffd", "'").strip()

                messages.append({"role": "assistant", "content": result})
                session["messages"] = messages[-10:]
                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(answer=result)
            except Exception as e:
                logger.error("Error generating answer: %s", e)
                # Roll back the unanswered user message so chat doesn't get stuck in an inconsistent state
                if messages and messages[-1].get("role") == "user":
                    messages.pop()
                    session["messages"] = messages
                error_msg = f"Error: {str(e)}"

                if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                    return jsonify(error=error_msg), 500

                session["chat_error"] = error_msg
                return redirect(url_for("index", keep_chat="1", _anchor="hero-chat"))

        return redirect(url_for("index", keep_chat="1", _anchor="hero-chat"))

    error = session.pop("chat_error", None)
    return render_template("index.html", messages=session.get("messages", []), error=error)

@app.route("/api/index", methods=["GET", "POST"])
def vercel_index():
    return index()

@app.route("/clear")
def clear():
    session.pop("messages", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )