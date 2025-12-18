#!/bin/bash

PORT=${1:-8889}  # Use $1 if provided, otherwise default to 8889

uv run --with jupyter jupyter lab \
    --no-browser --ServerApp.token='' --ServerApp.allow_remote_access=true --port=$PORT --ip=127.0.0.1 > /tmp/jupyter.log 2>&1
