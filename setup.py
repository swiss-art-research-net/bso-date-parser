import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="date-parser-sari", # Replace with your own username
    version="0.8.0",
    author="Florian Kräutli",
    author_email="florian.kraeutli@uzh.ch",
    description="A parser for recognising free-text dates",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/swiss-art-research-net/bso-date-parser.git",
    packages=setuptools.find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)