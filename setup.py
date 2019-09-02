from setuptools import find_packages, setup

with open('README.rst', 'r') as fh:
    long_description = fh.read()

setup(
    name='yggtorrentscraper',
    version='0.0.1',
    author='Harkame',
    description='Scraper for YggTorrent',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Harkame/YggTorrentDownloader',
    py_modules=['yggtorrentscraper'],
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
    ],
    packages=['yggtorrentscraper'],
    python_requires='>=3.6',
)
