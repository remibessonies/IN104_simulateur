#!/bin/bash

installCommand='python3 setup.py install'

for opt in "$@"; do
    case $opt in
        '-u' | '--user' )
            installCommand=$installCommand' --user'
            ;;
        *)
            echo "Unknown argument : "$opt
    esac
done

rm -r build

eval $installCommand
