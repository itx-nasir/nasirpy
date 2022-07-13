from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, encoding="utf-8") as f:
            return f.read()
    return "A Python framework for learning how web frameworks work"

setup(
    name="nasirpy",
    version="0.1.0",
    author="Nasir",
    author_email="Nasir.Iqbal.Dev@gmail.com",
    description="A Python framework for learning how web frameworks work",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/itx-nasir/nasirpy",
    packages=find_packages(),
    install_requires=[
        "uvicorn"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
