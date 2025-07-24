"""Setup personalizado da API da IQ Option."""
from setuptools import setup, find_packages

setup(
    name="iqoptionapi",
    version="0.0.3",
    packages=find_packages(),
    install_requires=[
        "pylint",
        "requests",
        "websocket-client"
    ],
    include_package_data=True,
    zip_safe=False,
    description="API personalizada da IQ Option",
    long_description="Fork da API do Rafael Faria adaptado por Célio Junior",
    author="Célio Junior",
    author_email="profissional.celiojunior@gmail.com",
    url="https://github.com/celiovmjr/iqoptionapi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
