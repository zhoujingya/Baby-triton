#!env bash

cmake -S test -B build -DPYTHON_PATH=`pwd`/.venv/bin -DSRC_DIR=`pwd`

