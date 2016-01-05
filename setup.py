from setuptools import setup, find_packages

import pooled_pika

setup(
    name="pooled-pika",
    version=pooled_pika.__version__,
    py_modules=["pooled_pika"],
    description="a connection pool wrapper about async pika",
    author="Zephor",
    author_email="zephor@qq.com",
    url="https://github.com/Zephor5/pooled-pika",
    license="BSD 3-clause",
    packages=find_packages()
)

