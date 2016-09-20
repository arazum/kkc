#! /bin/bash

mkdir -p json && ./parse.py && ./cat.py && latexmk output -pdf
