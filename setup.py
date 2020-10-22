# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in sales_partner_ig_commission/__init__.py
from sales_partner_ig_commission import __version__ as version

setup(
	name='sales_partner_ig_commission',
	version=version,
	description='Sales Partner Item Groupwise Commission',
	author='GreyCube Technologies',
	author_email='admin@greycube.in',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
