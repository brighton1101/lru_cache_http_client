from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='lru_cache_http_client',
    version='0.0.1',
    author='Brighton Balfrey',
    author_email='balfrey@usc.edu',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        'requests>=2.0'
    ]
)
