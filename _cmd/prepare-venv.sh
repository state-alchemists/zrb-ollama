echo "Install packages"
poetry install --only main
poetry install -E openai -E bedrock -E embedding-cpu
