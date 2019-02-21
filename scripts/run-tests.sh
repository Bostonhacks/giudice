#!/bin/bash

python -c 'from tests.main_tests import *; print run_tests()'
python -c 'from tests.projects_tests import *; print run_tests()'