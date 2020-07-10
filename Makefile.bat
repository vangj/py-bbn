@ECHO off
if /I %1 == default goto :default
if /I %1 == init goto :init
if /I %1 == lint goto :lint
if /I %1 == test goto :test
if /I %1 == clean goto :clean
if /I %1 == build goto :build
if /I %1 == install goto :install

goto :eof ::can be ommited to run the `default` function similarly to makefiles

:default
goto :test

:init
pip install -r requirements.txt
goto :eof

:lint
python -m flake8 ./pybbn
goto :eof

:test
nosetests tests
goto :eof

:clean
del /S *.pyc
rmdir /S /Q coverage
rmdir /S /Q dist
rmdir /S /Q build
rmdir /S /Q pybbn.egg-info
rmdir /S /Q pybbn/pybbn.egg-info
rmdir /S /Q jupyter/.ipynb_checkpoints
rmdir /S /Q docs/build
rmdir /S /Q joblib_memmap
rmdir /S /Q .pytest_cache
del .coverage
del .noseids
goto :eof

:build
python setup.py bdist_egg sdist bdist_wheel
goto :eof

:install
python setup.py install
goto :eof