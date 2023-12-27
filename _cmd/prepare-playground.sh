rm -Rf playground
cp -r playground-template playground

cd playground
deactivate 2>/dev/null

python -m venv .venv
source .venv/bin/activate
pip install --use-feature=in-tree-build "$(pwd)/.."
