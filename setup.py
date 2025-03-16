from setuptools import setup, find_packages

setup(
    name="flasksearch",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "flask",
        "elasticsearch",
        "python-dotenv",
        "flask-cors",
    ],
) 