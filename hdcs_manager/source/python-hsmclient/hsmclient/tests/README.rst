=========================================
Hyperstash Manager Testing Infrastructure
=========================================

A note of clarification is in order, to help those who are new to testing in
python-hsmclient:

- actual unit tests are created in the "tests" directory;

This README file attempts to provide current and prospective contributors with
everything they need to know in order to start creating unit tests.

Running Tests
-------------

In the root of the python-hsmclient source code run the run_tests.sh script. This
will offer to create a virtual environment and populate it with dependencies.
If you don't have dependencies installed that are needed for compiling
python-hsmclient's direct dependencies, you'll have to use your operating
system's method of installing extra dependencies. To get help using this script
execute it with the -h parameter to get options `./run_tests.sh -h`
