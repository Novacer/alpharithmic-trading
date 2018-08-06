#!/bin/bash

# This script is for quickly activating the python virtual environment for development

echo "Begin"
echo "Trying to activate the virtual environment"

cd env/Scripts

source activate

echo "virtual environment activated"

cd ../../

echo "Done"
