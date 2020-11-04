from setuptools import setup, find_packages

setup(name='lru_cache_http_client',
    version='0.1',
    author='Brighton Balfrey',
    author_email='balfrey@usc.edu',
    packages=find_packages(),
    install_requires=[
        requests>=2.0.0
    ]
)
