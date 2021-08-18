import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ID900",
    version="1.0.1",
    author="Xinghua Liu",
    author_email="xinghua.liu94@gmail.com",
    description="python classes for ID900",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/XinghuaLiu/ID900",
    project_urls={
        "Bug Tracker": "https://github.com/XinghuaLiu/ID900/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU3.0 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)