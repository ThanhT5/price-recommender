# AI Module for Price Recommender

This module implements AI features for the Handmade Goods Pricing Assistant.

## Overview

The AI module provides:

1. A conversational assistant to help users input pricing parameters
2. Intelligent pricing recommendations based on conversation context
3. Structured data extraction from natural language conversations

## Components

### Client (client.py)
- Handles communication with the OpenAI API
- Manages API keys and authentication
- Implements error handling and retries
- Extracts structured pricing recommendations from conversations

### Chat Handler (chat_handler.py)
- Manages conversation state and history
- Tracks system and user messages
- Processes AI responses and updates the conversation

### Models (models.py)
- Defines structured data formats for AI interactions
- Implements validation for pricing parameters
- Provides typed interfaces for the rest of the application

### Configuration (config.py)
- Contains API settings and credentials
- Defines system prompts and default behavior
- Manages environment-specific settings

## Usage

The AI module is designed to be used through the chat interface in the main application:

```python
from src.ai.chat_handler import ChatHandler

# Create a chat handler
chat_handler = ChatHandler()

# Send a message and get a response
response = chat_handler.send_message("I'm making a handcrafted leather wallet that takes about 3 hours to complete")

# Get pricing recommendations based on the conversation
recommendations = chat_handler.get_recommendations()
```

## Requirements

- OpenAI API key (set in environment variable `OPENAI_API_KEY`)
- Python 3.8+ with dependencies in requirements.txt 