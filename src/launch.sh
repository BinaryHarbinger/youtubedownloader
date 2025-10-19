#!/bin/bash

SOURCE="${BASH_SOURCE[0]}"
SCRIPT_DIR="$(cd "$(dirname "$SOURCE")" && pwd)"

cd $SCRIPT_DIR

python main.py
