from setuptools import setup
import setuptools
from s3_site_maker import __version__
import os
import sys

try:
    from pypandoc import convert
    README = convert('README.md', 'rst')
except ImportError:
    README = open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r', encoding="utf-8").read()

with open(os.path.join(os.path.dirname(__file__), 'requirements.txt')) as f:
    if sys.version_info[0] == 2:
        required = f.read().splitlines()
    else:
        required = []
        for package in f.read().splitlines():
            if 'futures' not in package:
                required.append(package)


setup(
    name='s3_site_maker',
    version=__version__,
    packages=['s3_site_maker'],
    install_requires=required,
    include_package_data=True,
    license='MIT License',
    description='Create a static webstie in an S3 Bucket',
    long_description=README,
    author='Alberto Acuna',
    author_email='aacuna3@asu.edu',
    entry_points={
        'console_scripts': [
            's3_site_maker=s3_site_maker.cli:handler'
        ]
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
