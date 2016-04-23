#!/bin/bash

if test $# -gt 0
then
    rm -r build
    rm -r IN104_simulateur/cpp/*.so
    export USE_CYTHON=1
fi

python3 setup.py build_ext --inplace
echo "\nIN104_simulateur successfully built\n"

if test $# -gt 0
then
    unset USE_CYTHON
fi

python3 setup.py install
echo "\nIN104_simulateur successfully installed"
