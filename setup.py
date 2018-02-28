#!/usr/bin/env python3
# -*- coding : utf-8 -*-
# Author: Bohdan Bobrowski

from setuptools import setup

setup(
    name='keyword_counter',
    version='0.1',
    description="Web keyword counter",
    url="https://github.com/bohdanbobrowski/keyword-counter",
    author="Bohdan Bobrowski",
    author_email="bohdanbobrowski@gmail.com",
    license="MIT",
    packages=["keyword_counter","keyword_counter_lib"],
    install_requires=["PyQt5","pycurl","validators","lxml"],
)
