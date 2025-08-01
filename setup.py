from setuptools import setup, find_packages

setup(
    name="runRadiostat",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "runRadiostat=runRadiostat.__main__:main"
        ]
    },
    install_requires=[],
    author="Benjamin Rodriguez",
    description="CLI tool for running and analyzing Rodeostat electrochemical tests",
)