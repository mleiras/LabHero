#!/bin/bash

# for building online documentation
if [ -n "$1" ]
then
    DOXYFILE=$1
else
    DOXYFILE=ug.dxy
fi

# build a fresh version of UG
make clean -C ../
make -j8 -C ../

# build parameter files and fscip output
echo ">>> preparing parameters file"
cat inc/simpleinstance/default.prm | sed -e "s/# //g" > simple.prm
../bin/fscip simple.prm inc/simpleinstance/simple.lp > /dev/null
mv simple.prm parameters.prm
../bin/fscip inc/simpleinstance/default.prm inc/simpleinstance/simple.lp > output.log
mv -f output.log inc/simpleinstance/.
mv -f simple.sol inc/simpleinstance/.
rm -f simple*

if [ "$HTML_FILE_EXTENSION" = "" ]
then
    HTML_FILE_EXTENSION=html
fi

# finally build the ug documentation
echo ">>> compiling documentation"
doxygen ${DOXYFILE}

CURRENT_DIR=$(pwd)
echo ">>> to view documentation open ${CURRENT_DIR}/html/index.html"
