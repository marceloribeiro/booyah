from setuptools import setup, find_packages

setup(
    name="booyah",
    version="0.0.10",
    author = "Marcelo Ribeiro",
    author_email = "themarceloribeiro@gmail.com",
    description = "A joyful python web framework",
    url = "https://github.com/marceloribeiro/booyah",
    project_urls = {
        "Bug Tracker": "https://github.com/marceloribeiro/booyah/issues",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = find_packages(where="src"),
    python_requires = ">=3.6",
    entry_points={
        "console_scripts": [
            "booyah = booyah.__main__:main"
        ]
    },
)