#!/bin/bash

# make sure that the current directory is the one where this script is
cd ${0%/*}

echo "../../extract_gas out/mosaic_0001_ out/mosaic_gas.txt"
../../extract_gas out/mosaic_0001_ out/mosaic_gas.txt
echo "../../numeric_diff true_gas.txt out/mosaic_gas.txt 0 0.01 0 0 2 0"
../../numeric_diff true_gas.txt out/mosaic_gas.txt 0 0.01 0 0 2 0
exit $?