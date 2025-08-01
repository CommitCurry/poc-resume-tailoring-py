#!/bin/bash

# run.sh - Quick test runner for CommitCurry with Ollama models
# Usage: ./run.sh <folder> <model_name>
# Example: ./run.sh samples/ qwen2.5:7b

set -e  # Exit on any error

# Check if correct number of arguments provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <folder> <model_name>"
    echo "Example: $0 samples/ qwen2.5:7b"
    echo ""
    echo "This will run: uv run commitcurry -m ollama:<model_name> <folder>/cv.md <folder>/job.md"
    echo "And save output to: <folder>/result-<model_name>.txt"
    exit 1
fi

FOLDER="$1"
MODEL="$2"

# Remove trailing slash from folder if present
FOLDER="${FOLDER%/}"

# Check if folder exists
if [ ! -d "$FOLDER" ]; then
    echo "Error: Folder '$FOLDER' does not exist"
    exit 1
fi

# Check if CV file exists
CV_FILE="$FOLDER/cv.md"
if [ ! -f "$CV_FILE" ]; then
    echo "Error: CV file not found: $CV_FILE"
    exit 1
fi

# Check if job description file exists
JOB_FILE="$FOLDER/job.md"
if [ ! -f "$JOB_FILE" ]; then
    echo "Error: Job description file not found: $JOB_FILE"
    exit 1
fi

# Prepare output file
OUTPUT_FILE="$FOLDER/result-$MODEL.txt"

# Prepare full model name for CommitCurry
FULL_MODEL="ollama:$MODEL"

echo "🚀 Running CommitCurry with Ollama model: $MODEL"
echo "📁 Folder: $FOLDER"
echo "📄 CV: $CV_FILE"
echo "📋 Job: $JOB_FILE"
echo "💾 Output: $OUTPUT_FILE"
echo "🤖 Model: $FULL_MODEL"
echo ""

# Run CommitCurry and save output
echo "⚡ Processing..."
uv run commitcurry -m "$FULL_MODEL" "$CV_FILE" "$JOB_FILE" > "$OUTPUT_FILE"

echo "✅ Done! Results saved to: $OUTPUT_FILE"
echo "📖 View results: cat $OUTPUT_FILE"