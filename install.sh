#!/bin/bash

buildCommand='python3 setup.py build_ext --inplace'
installCommand='python3 setup.py install'

unset USE_CYTHON
for opt in "$@"; do
    case $opt in
        '-u' | '--user' )
            installCommand=$installCommand' --user'
            ;;
        '-c' | '--cython')
            export USE_CYTHON=1
            ;;
        *)
            echo "Unknown argument : "$opt
    esac
done

if test $USE_CYTHON; then
    rm -r build
    rm -r IN104_simulateur/cpp/*.so    
fi

eval $buildCommand
eval $installCommand
