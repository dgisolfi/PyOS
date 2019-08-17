#!/usr/bin/python3
# Daniel Nicolas Gisolfi

from setuptools import find_packages
from setuptools import setup

setup(
	name='Py-OS',
	version='1.0.0',
	description=(
		'An OS that runs a subset of the 6502 opcodes, implemented in python'
	),
	long_description=open('README.md').read(),
	long_description_content_type='text/markdown',
	url='https://github.com/dgisolfi/PyOS',
	author='dgisolfi',
	license='MIT',
	packages=find_packages(),
   
	# install_requires=[ # Add any dependencies here ],
	zip_safe=False,
	entry_points='''
	[console_scripts]
	pyos=pyos.__main__:main
	'''
)