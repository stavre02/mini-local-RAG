#!/bin/bash

ollama serve &
PID=$!

until ollama list >/dev/null 2>&1; do
    echo "Waiting for ollama to start..."
    sleep 2
done

ollama pull qwen3-embedding:4b 
ollama pull llama3.2:1b 
ollama pull gemma3:4b

wait $PID