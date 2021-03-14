import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MediaTools",
    version="1.0.4",
    author="Andrew Hossack",
    author_email="andrew_hossack@outlook.com",
    description="MediaTools is a content management and generation package for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-hossack/ContentTools",
    project_urls={
        "Bug Tracker": "https://github.com/andrew-hossack/MediaTools/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=[
        "google-api-python-client",
        "TikTokApi",
        "oauth2client",
        "praw",
        "google-cloud",
        "google-cloud-core",
        "google-cloud-texttospeech"
    ]
)