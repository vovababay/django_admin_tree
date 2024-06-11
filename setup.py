import os

from setuptools import setup, find_packages

setup(
    name = 'django_admin_tree',
    version = '0.0.2',
    description = 'Test description',
    long_description=open(os.path.join(os.path.dirname(__file__), 'README.rst')).read(),
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
        "License :: MIT License",
    ]
)
