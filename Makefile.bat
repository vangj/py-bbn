@ECHO off
if /I %1 == default goto :default
if /I %1 == init goto :init
if /I %1 == lint goto :lint
if /I %1 == test goto :test

goto :eof ::can be ommited to run the `default` function similarly to makefiles

:default
goto :test

:init
pip install -r requirements.txt
goto :eof

:lint
python -m flake8 ./bechtel
goto :eof

:test
nosetests tests
goto :eof