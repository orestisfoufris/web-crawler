from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="Crawler",
    version="0.1.0",
    author='Orestis Foufris',
    author_email='orestis.py@hotmail.com',
    packages=['crawler'],
    include_package_data=True,
    package_data={'crawler':['*'],},    
    description='A simple web crawler',
    long_description=readme(),
    install_requires=[
        'grequests', 'mock', 'bs4',
    ],
)
