#!/bin/bash

#
#echo "Testing the help command..."
#python main.py -h
echo "Testing the deploy command..."
python cli.py deploy dev -l ~/repos/aws_site_maker/test/test_site

