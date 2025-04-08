"""
LLM Provider Configuration

This module handles the configuration and initialization of language model providers,
supporting both Anthropic Claude and Google Gemini models.

Features:
- Dynamically selects the LLM provider based on environment variables
- Supports Anthropic Claude and Google Gemini AI models
- Uses environment variables for secure API key and model name management
- Easy to extend for additional model providers

Requirements:
- langchain_anthropic for Anthropic Claude integration
- langchain_google_genai for Google Gemini integration
- dotenv for environment variable management

Environment Variables:
- USE_PROVIDER: Which provider to use ('anthropic' or 'google')
- ANTHROPIC_MODEL: The specific Anthropic model name (e.g., 'claude-3-opus-20240229')
- GOOGLE_MODEL: The specific Google model name (e.g., 'gemini-pro')
- ANTHROPIC_API_KEY: Your Anthropic API key (loaded automatically by langchain)
- GOOGLE_API_KEY: Your Google API key (loaded automatically by langchain)
"""

from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env.dev file
# override=True ensures variables in the file take precedence over existing environment variables
load_dotenv(find_dotenv(".env.dev"), override=True)

# Determine which provider to use from environment variables
USE_PROVIDER = os.environ.get("USE_PROVIDER")

# Get model names from environment variables
ANTHROPIC_MODEL = os.environ.get("ANTHROPIC_MODEL")
GOOGLE_MODEL = os.environ.get("GOOGLE_MODEL")

# Dictionary mapping provider names to initialized LangChain chat model instances
providers_dict = {
    "google": ChatGoogleGenerativeAI(model=GOOGLE_MODEL),
    "anthropic": ChatAnthropic(model=ANTHROPIC_MODEL)
}

# Select the model based on the specified provider
# This will be used in other modules that import this configuration
model = providers_dict[USE_PROVIDER]