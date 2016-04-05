#!/bin/bash

if test $# -gt 0
then
    rm -r build
    rm -r simulateur/cpp/*.so
    export USE_CYTHON=1
fi

python setup.py build_ext --inplace

if test $# -gt 1
then
    unset USE_CYTHON
fi
