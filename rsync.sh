#!/bin/bash
set -e -x
TIMESTAMP=$(date +"%Y-%m-%d")
sed -i 's!^todo_include_todos *=.*$!todo_include_todos = False!g' conf.py
rm -rf build
MAKEFLAGS="" make html pdf
./build_latex.py
rsync -avz build/ ssh.alwaysdata.com:www/tmp/unicode-$TIMESTAMP
sed -i 's!^todo_include_todos *=.*$!todo_include_todos = True!g' conf.py
