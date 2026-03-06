#!/usr/bin/env bash

set -euo pipefail

model=$1

if [[ -z $model ]]; then
    echo "Usage: $0 <model>"
    exit 1
fi

ollama pull $1
curl -s http://localhost:11434/api/show -d "{\"name\": \"$model\"}" \
    | jq '.model_info | to_entries
    | map(select(.key | test("embedding_length|context_length")))
    | from_entries'
