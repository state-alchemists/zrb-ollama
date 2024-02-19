if [ ! -d .venv ]
then
  echo "Init virtual environment"
  python -m venv .venv
  pip install --upgrade pip
  pip install "poetry==1.7.1"
fi
echo "Activate virtual environment"
source .venv/bin/activate

