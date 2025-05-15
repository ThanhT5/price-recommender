"""
Configuration for the AI recommendation system.
Contains settings for the OpenAI API and prompts.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

# Try to load environment variables from .env file
dotenv_path = Path(__file__).parent.parent.parent / ".env"
if dotenv_path.exists():
    load_dotenv(dotenv_path)

# OpenAI API settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = "gpt-4o-mini"  # Using the 4o mini model as specified

# System prompts
PRICING_ADVISOR_PROMPT = """
You are an expert pricing assistant for handmade goods. Your goal is to help artisans 
determine the best parameters for pricing their handcrafted items. Ask targeted questions 
to gather information about:

1. Materials used and their costs
2. Time spent creating the item
3. Artisan's experience level and desired hourly rate
4. Uniqueness of the product (how different it is from mass-produced alternatives)
5. Market demand for this type of product
6. Selling price (if they already have one in mind)

Be conversational but focused on gathering relevant information to provide accurate
pricing recommendations. If they have a target profit percentage in mind, explain that 
our system now focuses on costs and selling prices directly, showing the resulting profit.
"""

# Default values (fallback if AI is not available)
DEFAULT_PRICING_PARAMETERS = {
    "material_cost": 10.0,
    "hours_worked": 2.0,
    "labor_rate": 15.0,
    "uniqueness": 5.0,
    "demand": 5.0,
    "selling_price": 0.0
} 