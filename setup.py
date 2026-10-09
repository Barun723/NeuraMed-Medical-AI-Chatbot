from setuptools import setup, find_packages
with open('requirements.txt') as f:
    requir = f.read().splitlines()

setup(
    name='medical_book',
    packages=find_packages(),
    install_requires=requir,
)