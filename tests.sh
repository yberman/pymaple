#!/bin/sh
python setup.py build
sudo python setup.py install
python src/tests.py -v