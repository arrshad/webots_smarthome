from setuptools import setup, find_packages

setup(
    name="webots_smarthome",
    version="0.0.1",
    author="Sina Arshad",
    author_email="sina.arshad@hotmail.com",
    description="A Python API to interact with and control a smart home simulation using Webots.",
    packages=find_packages(),
    install_requires=[
        "pillow",
        "matplotlib",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)