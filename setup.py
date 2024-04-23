import os

from setuptools import setup, find_packages
from django_admin_tree import __version__ as version

setup(
    name = 'django_admin_tree',
    version = version,
    description = 'Test description',
    long_description='Test description',
    author = 'Vladimir Babaev.',
    author_email = 'vladimir.babaev.12@gmail.com',
    url = 'https://github.com/vovababay/django-admin-tree',
    packages = find_packages(),
    zip_safe=False,
    include_package_data = True,
    install_requires=[
        'Django>=4.2.0',
    ],
    classifiers = [
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ]
)