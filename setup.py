import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyrigee",
    version="1.0.1",
    author="Jack Sheehan",
    description="A python package for visualizing spacecraft orbits and orbital maneuvers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JackCSheehan/pyrigee",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Topic :: Scientific/Engineering :: Astronomy",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
    python_requires='>=3.6',
)