#!/bin/bash

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

rm -r build

eval $installCommand
unset USE_CYTHON
