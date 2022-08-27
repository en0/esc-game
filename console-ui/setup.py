from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="esc-ui-console",
    version="0.1.0",
    description="A little game.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Ian Laird",
    author_email="irlaird@gmail.com",
    url="https://github.com/en0/esc",
    packages=["esc.ui.console"],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
