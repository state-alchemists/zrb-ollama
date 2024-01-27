rm -Rf playground
cp -r playground-template playground

cd playground
deactivate 2>/dev/null

_IS_EMPTY_VENV=0
python -m venv .venv
source .venv/bin/activate
pip install --use-feature=in-tree-build "$(pwd)/.."
pip install -r requirements.txt
