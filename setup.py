import yggtorrentscraper
from setuptools import find_packages, setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='yggtorrentscraper',
    version='0.0.6',
    author='Harkame',
    description='Scraper for YggTorrent',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Harkame/YggTorrentDownloader',
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6'
)
