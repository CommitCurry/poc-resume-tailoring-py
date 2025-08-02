# Local LLM Models Comparison for Ollama

This document provides a comprehensive comparison of locally available LLM models through Ollama, focusing on resume writing and text generation capabilities.

## Model Overview

| Model | Creator | Latest Version | Parameter Sizes | Download Size | Main Purpose |
|-------|---------|----------------|-----------------|---------------|--------------|
| **DeepSeek-R1** | DeepSeek | R1-0528 | 7B, 32B, 70B | 4.7GB - 404GB | Advanced reasoning, step-by-step thinking |
| **Gemma2** | Google | 2.0 | 2B, 9B, 27B | 1.6GB - 16GB | General purpose, efficient performance |
| **Qwen2.5** | Alibaba | 2.5 | 0.5B, 1.5B, 3B, 7B, 14B, 32B, 72B | 394MB - 41GB | Multilingual, coding, reasoning |
| **Llama** | Meta | 3.3 | 1B, 3B, 8B, 70B | 1.3GB - 40GB | General purpose, balanced performance |
| **Mistral** | Mistral AI | 7B v0.3 | 7B | 4.1GB | Professional writing, structured output |
| **Phi** | Microsoft | 4.0 | 14B | 9.1GB | Reasoning, multilingual, compact efficiency |

## Use Case Comparison Matrix

| Use Case | DeepSeek-R1 | Gemma2 | Qwen2.5 | Llama3.3 | Mistral | Phi4 |
|----------|-------------|--------|---------|----------|---------|------|
| **Resume Writing** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Professional Text Generation** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Complex Reasoning** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Speed/Efficiency** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Multilingual Support** | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Code Generation** | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Hardware Requirements** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |

**Rating Scale**: ⭐ = Poor, ⭐⭐ = Fair, ⭐⭐⭐ = Good, ⭐⭐⭐⭐ = Very Good, ⭐⭐⭐⭐⭐ = Excellent

## Detailed Model Specifications

### DeepSeek-R1 (Reasoning Specialist)
- **Strengths**: Advanced step-by-step reasoning, approaches O3/Gemini 2.5 Pro performance
- **Best For**: Complex problem solving, multi-step resume optimization
- **RAM Requirements**: 8GB (7B), 32GB (32B), 64GB+ (70B)
- **Key Features**: Chain-of-thought reasoning, mathematical problem solving
- **Ollama Commands**:
  ```bash
  ollama pull deepseek-r1:7b    # 4.7GB
  ollama pull deepseek-r1:32b   # 19GB
  ollama pull deepseek-r1:70b   # 40GB
  ```

### Gemma2 (Efficient General Purpose)
- **Strengths**: Google's efficient architecture, good performance-to-size ratio
- **Best For**: Quick iterations, balanced performance
- **RAM Requirements**: 4GB (2B), 16GB (9B), 32GB (27B)
- **Key Features**: Fast inference, Google's Gemini technology foundation
- **Ollama Commands**:
  ```bash
  ollama pull gemma2:2b     # 1.6GB
  ollama pull gemma2:9b     # 5.4GB
  ollama pull gemma2:27b    # 16GB
  ```

### Qwen2.5 (Multilingual Powerhouse)
- **Strengths**: Excellent multilingual support, strong reasoning, coding capabilities
- **Best For**: International resume writing, complex text analysis
- **RAM Requirements**: 2GB (0.5B), 8GB (7B), 16GB (14B), 32GB (32B)
- **Key Features**: 128K context length, multilingual excellence, coding proficiency
- **Ollama Commands**:
  ```bash
  ollama pull qwen2.5:0.5b  # 394MB
  ollama pull qwen2.5:7b    # 4.1GB
  ollama pull qwen2.5:14b   # 8.2GB
  ollama pull qwen2.5:32b   # 18GB
  ```

### Llama3.3 (Balanced Performance)
- **Strengths**: Well-rounded capabilities, strong community support
- **Best For**: General resume writing, reliable performance
- **RAM Requirements**: 2GB (1B), 4GB (3B), 8GB (8B), 64GB (70B)
- **Key Features**: Meta's proven architecture, extensive fine-tuning
- **Ollama Commands**:
  ```bash
  ollama pull llama3.3:1b   # 1.3GB
  ollama pull llama3.3:8b   # 4.7GB
  ollama pull llama3.3:70b  # 40GB
  ```

### Mistral 7B (Professional Writing)
- **Strengths**: Excellent for structured, professional content
- **Best For**: High-quality resume writing, business documents
- **RAM Requirements**: 8GB
- **Key Features**: Professional tone, structured output, European language support
- **Ollama Commands**:
  ```bash
  ollama pull mistral:7b    # 4.1GB
  ollama pull mistral:nemo  # 7.1GB (12B variant)
  ```

### Phi4 (Compact Reasoning)
- **Strengths**: Microsoft's efficient reasoning model, multilingual capabilities
- **Best For**: Reasoning-heavy resume optimization, compact deployment
- **RAM Requirements**: 16GB
- **Key Features**: Advanced reasoning in compact size, multilingual support
- **Ollama Commands**:
  ```bash
  ollama pull phi4:14b      # 9.1GB
  ollama pull phi4:mini     # 2.5GB (3.8B variant)
  ```

## Recommended Models for Resume Writing

### 🥇 Top Choice: **ollama:qwen2.5:7b**
- **Why**: Best balance of quality, speed, and features
- **Pros**: Excellent text generation, multilingual, reasonable resource usage
- **Use When**: Default choice for most resume writing tasks

### 🥈 Professional Choice: **ollama:mistral:7b**
- **Why**: Specialized for professional, structured writing
- **Pros**: Exceptional professional tone, structured output
- **Use When**: High-stakes professional documents, formal resumes

### 🥉 Reasoning Choice: **ollama:deepseek-r1:7b**
- **Why**: Advanced reasoning for complex resume optimization
- **Pros**: Step-by-step thinking, complex problem solving
- **Use When**: Need detailed analysis and optimization reasoning

### 🏆 Efficiency Choice: **ollama:gemma2:9b**
- **Why**: Google's efficient architecture with good performance
- **Pros**: Fast inference, good quality, moderate resource usage
- **Use When**: Quick iterations, limited hardware resources

## Hardware Recommendations

| Model Size | Minimum RAM | Recommended RAM | GPU VRAM | Performance |
|------------|-------------|-----------------|----------|-------------|
| **0.5B-3B** | 4GB | 8GB | Optional | Fast, basic quality |
| **7B-9B** | 8GB | 16GB | 6GB+ | Good balance |
| **14B-27B** | 16GB | 32GB | 12GB+ | High quality |
| **32B+** | 32GB | 64GB+ | 24GB+ | Best quality |

## Installation Quick Start

```bash
# Download recommended models for resume writing
ollama pull qwen2.5:7b        # Primary choice
ollama pull mistral:7b         # Professional alternative  
ollama pull gemma2:9b          # Efficient option
ollama pull deepseek-r1:7b     # Reasoning specialist

# Start Ollama server
ollama serve

# Test a model
ollama run qwen2.5:7b
```

## Model Selection Guide

**Choose based on your priorities (use with `uv run commitcurry -m <model>`):**

- **Quality First**: `ollama:qwen2.5:14b` or `ollama:deepseek-r1:32b`
- **Speed First**: `ollama:gemma2:2b` or `ollama:qwen2.5:0.5b`  
- **Balance**: `ollama:qwen2.5:7b` or `ollama:llama3.3:8b`
- **Professional Writing**: `ollama:mistral:7b` or `ollama:mistral:nemo`
- **Reasoning Tasks**: `ollama:deepseek-r1:7b` or `ollama:phi4:14b`
- **Limited Hardware**: `ollama:gemma2:2b` or `ollama:qwen2.5:0.5b`

## Future Considerations

For planned multi-step reasoning and thinking applications:
- **DeepSeek-R1** series excel at chain-of-thought reasoning
- **Phi4** provides compact reasoning capabilities
- **Qwen2.5** offers good reasoning with multilingual support
- Consider larger variants (32B+) for complex reasoning tasks