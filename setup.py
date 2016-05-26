#!/usr/bin/env python
import os
import sys
from distutils.core import setup
from distutils.extension import Extension

USE_CYTHON = bool(os.getenv('USE_CYTHON'))
ext = '.pyx' if USE_CYTHON else '.cpp'

C_sources = ['IN104_simulateur/cpp/CBoardState.cpp', 'IN104_simulateur/cpp/CCell.cpp', 'IN104_simulateur/cpp/CMove.cpp']

extensions = [
    Extension(
        name="IN104_simulateur.cpp.gameState",
        language='c++',
        sources=["IN104_simulateur/cpp/gameState"+ext]+C_sources,
        include_dirs = ["."]
    ),
    Extension(
        name="IN104_simulateur.cpp.boardState",
        language='c++',
        sources=["IN104_simulateur/cpp/boardState"+ext]+C_sources,
        include_dirs = ["."]
    ),
    Extension(
        name="IN104_simulateur.cpp.move",
        language='c++',
        sources=["IN104_simulateur/cpp/move"+ext]+C_sources,
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
