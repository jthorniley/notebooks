#!/usr/bin/env bash

jupyter nbconvert Hex\ Coordinates.ipynb  --execute --to rst  --output-dir docs --output hex

cd docs && make html
