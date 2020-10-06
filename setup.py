import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="discordqueue",
    version="0.1.0",
    author="Micalobia",
    author_email="micalobiabusiness@gmail.com",
    description="A audiosource queue cog for discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Micalobia/discordqueue",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
