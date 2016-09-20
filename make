#! /bin/bash

./parse.py && ./cat.py && latexmk output -pdf
