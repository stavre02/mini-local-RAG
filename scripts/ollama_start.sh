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