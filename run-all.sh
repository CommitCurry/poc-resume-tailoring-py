#!/bin/bash

# run-all.sh - Run CommitCurry with all available Ollama models
# Usage: ./run-all.sh <folder>
# Example: ./run-all.sh samples/

set -e  # Exit on any error

# Check if correct number of arguments provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <folder>"
    echo "Example: $0 samples/"
    echo ""
    echo "This will:"
    echo "1. Get all available Ollama models using 'ollama list'"
    echo "2. Run ./run.sh <folder> <model> for each model"
    echo "3. Save results to <folder>/result-<model>.txt for each model"
    exit 1
fi

FOLDER="$1"

# Remove trailing slash from folder if present
FOLDER="${FOLDER%/}"

# Check if folder exists
if [ ! -d "$FOLDER" ]; then
    echo "Error: Folder '$FOLDER' does not exist"
    exit 1
fi

# Check if run.sh exists and is executable
if [ ! -x "./run.sh" ]; then
    echo "Error: ./run.sh not found or not executable"
    echo "Make sure run.sh exists and run: chmod +x run.sh"
    exit 1
fi

# Function to get models via API
get_models_via_api() {
    local api_url="$1"
    echo "🔍 Getting list of available Ollama models via API ($api_url)..." >&2
    
    # Use curl to get models from API
    local models_json
    if ! models_json=$(curl -s "$api_url/api/tags" 2>/dev/null); then
        echo "❌ Failed to connect to Ollama API at $api_url" >&2
        echo "💡 Make sure Ollama server is running at $api_url" >&2
        exit 1
    fi
    
    # Parse JSON to extract model names
    if command -v jq &> /dev/null; then
        # Use jq if available for better JSON parsing
        echo "$models_json" | jq -r '.models[]?.name // empty' | grep -v '^$'
    else
        # Fallback: simple parsing without jq
        echo "$models_json" | grep -o '"name":"[^"]*"' | cut -d'"' -f4 | grep -v '^$'
    fi
}

# Function to get models via CLI
get_models_via_cli() {
    echo "🔍 Getting list of available Ollama models via CLI..." >&2
    
    # Check if ollama command is available
    if ! command -v ollama &> /dev/null; then
        echo "❌ Error: 'ollama' command not found" >&2
        echo "💡 Make sure Ollama is installed and in your PATH" >&2
        exit 1
    fi
    
    # Get list of models from ollama, skip the header line, extract model names
    ollama list | tail -n +2 | awk '{print $1}' | grep -v '^$'
}

# Get models using API if OLLAMA_URL is set, otherwise use CLI
if [ -n "$OLLAMA_URL" ]; then
    MODELS=$(get_models_via_api "$OLLAMA_URL")
else
    MODELS=$(get_models_via_cli)
fi

if [ -z "$MODELS" ]; then
    echo "❌ No Ollama models found"
    echo "💡 Download models with: ollama pull <model_name>"
    echo "💡 Example: ollama pull qwen2.5:7b"
    exit 1
fi

# Count total models
MODEL_COUNT=$(echo "$MODELS" | wc -l | tr -d ' ')

echo "📋 Found $MODEL_COUNT Ollama models:"
echo "$MODELS" | sed 's/^/  - /'
echo ""

# Initialize counters
SUCCESS_COUNT=0
FAILURE_COUNT=0
FAILED_MODELS=""

echo "🚀 Starting batch processing for folder: $FOLDER"
echo "=" | tr -d '\n'; for i in $(seq 1 80); do echo -n "="; done; echo

# Iterate through each model
MODEL_INDEX=1
while IFS= read -r MODEL; do
    if [ -n "$MODEL" ]; then
        echo ""
        echo "[$MODEL_INDEX/$MODEL_COUNT] Processing model: $MODEL"
        echo "-" | tr -d '\n'; for i in $(seq 1 60); do echo -n "-"; done; echo
        
        # Run the model with error handling
        if ./run.sh "$FOLDER" "$MODEL"; then
            echo "✅ Success: $MODEL"
            SUCCESS_COUNT=$((SUCCESS_COUNT + 1))
        else
            echo "❌ Failed: $MODEL"
            FAILURE_COUNT=$((FAILURE_COUNT + 1))
            if [ -z "$FAILED_MODELS" ]; then
                FAILED_MODELS="$MODEL"
            else
                FAILED_MODELS="$FAILED_MODELS, $MODEL"
            fi
        fi
        
        MODEL_INDEX=$((MODEL_INDEX + 1))
    fi
done <<< "$MODELS"

echo ""
echo "=" | tr -d '\n'; for i in $(seq 1 80); do echo -n "="; done; echo
echo "🎯 BATCH PROCESSING COMPLETE"
echo "=" | tr -d '\n'; for i in $(seq 1 80); do echo -n "="; done; echo
echo ""
echo "📊 Summary:"
echo "  Total models: $MODEL_COUNT"
echo "  Successful: $SUCCESS_COUNT"
echo "  Failed: $FAILURE_COUNT"

if [ $FAILURE_COUNT -gt 0 ]; then
    echo "  Failed models: $FAILED_MODELS"
fi

echo ""
echo "📁 Results saved in: $FOLDER/"
echo "📋 List result files:"
ls -la "$FOLDER"/result-*.txt 2>/dev/null || echo "  No result files found"

echo ""
if [ $SUCCESS_COUNT -gt 0 ]; then
    echo "🔍 Quick comparison command:"
    echo "  for file in $FOLDER/result-*.txt; do echo \"=== \$(basename \$file) ===\"; head -5 \"\$file\"; echo; done"
fi

# Exit with error code if any models failed
if [ $FAILURE_COUNT -gt 0 ]; then
    exit 1
fi