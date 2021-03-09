import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# TODO Figure out how to include /examples, /lib, /dat
# vidtools/private in the install

setuptools.setup(
    name="VidTools",
    version="0.0.3",
    author="Andrew Hossack",
    author_email="andrew_hossack@outlook.com",
    description="VidTools is a video tools python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-hossack/VidTools",
    project_urls={
        "Bug Tracker": "https://github.com/andrew-hossack/VidTools/issues",
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