#!/usr/bin/env python
# -*- coding: utf-8 -*-
from distutils.core import setup
import pyefa

setup(name='pyefa',
	version=pyefa.__version__,
	description='Python-Bindings vor EFA-APIs. (Elektronische Fahrplanauskunft)',
	author='Nils Martin Klünder',
	author_email='nomoketo@nomoketo.de',
	url='https://github.com/NoMoKeTo/pyefa',
	packages=['pyefa'],
	license='Apache',
	classifiers=[
		'Topic :: Software Development :: Libraries :: Python Modules', 
		'Intended Audience :: Developers',
		'Programming Language :: Python',
		'License :: OSI Approved :: Apache Software License'],
	requires=['bs4', 'colorama'],
	)
