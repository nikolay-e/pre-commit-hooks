from setuptools import setup, find_packages

setup(
    name="pre-commit-hooks",
    version="2.0.0",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "emoji>=2.15.0",
    ],
    entry_points={
        "console_scripts": [
            "no-emoji=hooks.no_emoji:main",
        ],
    },
)
