#!/usr/bin/env python

from setuptools import setup

setup(
    name="static_website_updater",
    version="1",
    packages=["static_website_updater"],

    install_requires=[
        "boto",
        "flickrapi",
        "GitPython",
        "requests>=2.5.1",
    ],
    entry_points={
        "console_scripts": [
            "static_website_updater = static_website_updater.main:main"
        ]
    },
)
