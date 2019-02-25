#!/bin/bash

python3 -c 'from tests.main_tests import run_tests; print(run_tests())'
python3 -c 'from tests.projects_tests import run_tests; print(run_tests())'