#!/usr/bin/env python
import os
import sys
from distutils.core import setup
from distutils.extension import Extension

USE_CYTHON = bool(os.getenv('USE_CYTHON'))
ext = '.pyx' if USE_CYTHON else '.cpp'

extensions = [
    Extension(
        name="simulateur.cpp.gameState",
        sources=["simulateur/cpp/gameState"+ext],
        include_dirs = ["."]
    ),
    Extension(
        name="simulateur.cpp.boardState",
        sources=["simulateur/cpp/boardState"+ext],
        include_dirs = ["."]
    ),
    Extension(
        name="simulateur.cpp.move",
        sources=["simulateur/cpp/move"+ext],
        include_dirs = ["."]
    )
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)
    print("Running setup using Cython")
    
setup(name='IN104_simulateur',
    version='1.0',
    description='Game simulator for checkers and checkers-like games',
    author='Clément Masson',
    author_email='masson.cle@gmail.com',
    url='https://github.com/clement-masson/IN104_simulateur',
    ext_modules = extensions
)

