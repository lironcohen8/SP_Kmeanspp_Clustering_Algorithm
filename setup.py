# -*- coding: utf-8 -*-

from setuptools import Extension, setup

setup(name='mykmeanssp',
     version='0.1.0',
     description='Python wrapper for our kmeans code',
     ext_modules=[
         Extension(
             'mykmeanssp',  
             sources = ['kmeans.c'],
            )
        ]
    )

