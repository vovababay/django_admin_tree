import os
import io
from setuptools import setup, find_packages

PATH_BASE = os.path.dirname(__file__)

def read_file(fpath):
    """Reads a file within package directories."""
    with io.open(os.path.join(PATH_BASE, fpath)) as f:
        return f.read()

setup(
    name = 'django_admin_tree',
    version = '0.1.1',
    description = 'Test description',
    long_description=read_file('README.rst'),
    author = 'Vladimir Babaev.',
    license='MIT License',

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
        "License :: OSI Approved :: MIT License",
    ]
)
