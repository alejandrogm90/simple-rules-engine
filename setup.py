#! /usr/bin/env python
from setuptools import setup

from simple_rules_engine import __version__ as version

with open('README.md') as f:
    readme = f.read()

with open('HISTORY.md') as f:
    history = f.read()

setup(
    name='simple-rules-engine',
    version=version,
    description='Python DSL for setting up simple rules that can be configured without code',
    long_description='{0}\n\n{1}'.format(readme, history),
    long_description_content_type='text/markdown',
    author='alejandrogm90',
    author_email='alejandrogomezmartin90@outlook.com',
    url='https://github.com/alejandrogm90/simple-rules-engine',
    packages=['simple_rules_engine'],
    license='GNU',
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.0",
)
