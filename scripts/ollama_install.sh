#!/bin/bash

ollama serve &

while true; do
    ollama list
    # if output is error need to wait
    if [ $? -ne 0 ]; then
        sleep 2 
    else
        break 
    fi
done

ollama pull qwen3-embedding:4b
ollama pull llama3.2:1b
ollama pull gemma3:4b

#kill process
pid=$(pgrep ollama)
if [ -n "$pid" ]; then
    kill "$pid"
    echo "Ollama process(es) killed."
else
    echo "No Ollama process found."
fi