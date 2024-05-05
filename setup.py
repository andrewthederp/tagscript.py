from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
desc = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="tagscript.py",
    version="0.0.1",
    description="A preprocessor I made with the goal to mimic TagScript (who could've guessed)",
    long_description=desc,
    long_description_content_type="text/markdown",
    author="andreaw",
    url="https://github.com/andrewthederp/tagscript.py",
    license="Apache",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    include_package_data=True,
    package_data={},
    python_requires=">=3.6",
    packages=find_packages(include=["tagscript", "tagscript.*"]),
)
