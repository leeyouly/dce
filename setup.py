
from setuptools import setup, find_packages
import os

os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name = 'dce',
    version = '0.3.0',
    packages = find_packages(),
    entry_points = {'scrapy': ['settings = dce.settings']},
    install_requires = ['mysql-python', 
                        'cx_Oracle', 
                        'scrapy'],
)