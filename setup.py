from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vidlang",
    version="0.1.0",
    author="Richijs",
    author_email="richijs@agentmail.to",
    description="A domain-specific language for generating TikTok-style infographic videos with context-aware background media",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/richijsLV/VidLang",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "moviepy>=1.0.3",
        "Pillow>=9.0.0",
        "requests>=2.28.0",
        "openai>=0.27.0",
        "python-dotenv>=0.19.0",
        "pydub>=0.25.1",
        "numpy>=1.21.0",
    ],
    entry_points={
        "console_scripts": [
            "vidlang=vidlang.main:main",
        ],
    },
)
