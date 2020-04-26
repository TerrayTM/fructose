from setuptools import setup

with open("README.md", "r", encoding="utf-8") as file:
    long_description = file.read()

setup(
    name="fructose",
    packages=["fructose"],
    version="1.0.0",
    description= "Deployment CLI for synchronizing distributions with server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Terry Zheng",
    author_email="contact@terrytm.com",
    url="https://github.com/TerrayTM/fructose",
    python_requires=">=3.8",
    license="Apache 2.0",
    zip_safe=False,
    install_requires=["requests"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development"
    ],
    entry_points={
        "console_scripts": [
            "fructose = fructose.main:main"
        ]
    }
)
