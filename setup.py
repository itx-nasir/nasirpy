from setuptools import setup, find_packages

setup(
    name="nasirpy",
    version="0.1.0",
    author="Nasir",
    author_email="Nasir.Iqbal.Dev@gmail.com",
    description="A Python framework",
    long_description=open("README.md").read(),
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
