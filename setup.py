#!/usr/bin/env python
import os
import sys
from distutils.core import setup
from distutils.extension import Extension

USE_CYTHON = bool(os.getenv('USE_CYTHON'))
ext = '.pyx' if USE_CYTHON else '.cpp'

Csource = ["IN104_simulateur/cpp/CCell.cpp","IN104_simulateur/cpp/CMove.cpp","IN104_simulateur/cpp/CBoardState.cpp"]

extensions = [
    Extension(
        name="IN104_simulateur.cpp.gameState",
        sources=["IN104_simulateur/cpp/gameState"+ext]+Csource,
        include_dirs = ["."]
    ),
    Extension(
        name="IN104_simulateur.cpp.boardState",
        sources=["IN104_simulateur/cpp/boardState"+ext]+Csource,
        include_dirs = ["."]
    ),
    Extension(
        name="IN104_simulateur.cpp.move",
        sources=["IN104_simulateur/cpp/move"+ext]+Csource,
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
    author='Clement Masson',
    author_email='masson.cle@gmail.com',
    url='https://github.com/clement-masson/IN104_simulateur',
    license='MIT',
    packages = ['IN104_simulateur'],
    ext_modules = extensions
)

