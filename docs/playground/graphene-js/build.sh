#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d pypyjs-release-nojit ] ; then
	git clone https://github.com/pypyjs/pypyjs-release-nojit.git
fi

grapheneold_DIR="$(python -c "import os; import grapheneold; print os.path.dirname(grapheneold.__file__)")"
GRAPHQL_DIR="$(python -c "import os; import graphql; print os.path.dirname(graphql.__file__)")"
GRAPHQL_RELAY_DIR="$(python -c "import os; import graphql_relay; print os.path.dirname(graphql_relay.__file__)")"
SIX_DIR="$(python -c "import os; import libraries.six as six; print six.__file__.rstrip('c')")"

cd pypyjs-release-nojit

eval python tools/module_bundler.py add ./lib/modules "$grapheneold_DIR"
eval python tools/module_bundler.py add ./lib/modules "$GRAPHQL_DIR"
eval python tools/module_bundler.py add ./lib/modules "$GRAPHQL_RELAY_DIR"
eval python tools/module_bundler.py add ./lib/modules "$SIX_DIR"

python ./tools/module_bundler.py preload ./lib/modules grapheneold
python ./tools/module_bundler.py preload ./lib/modules grapheneold.relay
python ./tools/module_bundler.py preload ./lib/modules graphql
python ./tools/module_bundler.py preload ./lib/modules graphql_relay
python ./tools/module_bundler.py preload ./lib/modules six

python ./tools/module_bundler.py remove ./lib/modules unittest

lib_dirname=`perl -e 'use Cwd "abs_path";print abs_path(shift)' lib/`

if [ -d ../../../static/playground/lib ] ; then
	rm ../../../static/playground/lib
fi

mkdir -p ../../../static/playground

exec ln -s "$lib_dirname/" ../../../static/playground/lib
