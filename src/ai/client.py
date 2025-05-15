"""
Client for interacting with the OpenAI API.
"""

import logging
import json
import os
from openai import OpenAI
from typing import List, Optional, Dict
from .config import OPENAI_API_KEY, MODEL_NAME
from .models import PricingRecommendation
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIClient:
    """
    Client for interacting with the OpenAI API.
    Handles API requests, error handling, and retries.
    """
    
    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        """
        Initialize the AI client.
        
        Args:
            api_key: OpenAI API key (defaults to value from config)
            model_name: Model name to use (defaults to value from config)
        """
        # Load API key from environment if not provided
        if api_key is None:
            # Try to load from .env file in project root
            dotenv_path = os.path.join(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__)))), '.env')
            if os.path.exists(dotenv_path):
                load_dotenv(dotenv_path)
            
            # Get API key from environment
            api_key = os.getenv("OPENAI_API_KEY")
            
            if not api_key:
                logger.warning("No OpenAI API key found. AI features will not be available.")
        
        self.api_key = api_key
        self.model_name = model_name or MODEL_NAME
        
        # Initialize OpenAI client
        if self.api_key:
            try:
                self.client = OpenAI(api_key=self.api_key)
                logger.info(f"OpenAI client initialized with model: {self.model_name}")
            except Exception as e:
                logger.error(f"Error initializing OpenAI client: {str(e)}")
                self.client = None
        else:
            self.client = None
    
    def is_available(self) -> bool:
        """Check if the OpenAI client is available for use."""
        return self.client is not None and self.api_key is not None
    
    def chat_completion(
        self, 
        messages: List[Dict[str, str]], 
        temperature: float = 0.7,
        max_tokens: int = 500
    ) -> Optional[str]:
        """
        Send a request to the chat completions API and return the response.
        
        Args:
            messages: List of message objects with role and content
            temperature: Sampling temperature (0.0-2.0)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Response content or None if the request fails
        """
        if not self.is_available():
            logger.warning("AI client not available. Skipping chat completion request.")
            return None
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error in chat completion request: {str(e)}")
            return None
    
    def get_pricing_recommendation(
        self, 
        conversation_summary: str
    ) -> Optional[PricingRecommendation]:
        """
        Get structured pricing recommendations from the conversation.
        Uses a JSON format and OpenAI's function calling capability.
        
        Args:
            conversation_summary: Summary of the conversation with the user
            
        Returns:
            PricingRecommendation object or None if the request fails
        """
        if not self.is_available():
            logger.warning("AI client not available. Skipping pricing recommendation request.")
            return None
        
        try:
            # Set up the function call for structured output
            function_schema = {
                "name": "pricing_recommendation",
                "description": "Generate pricing parameters for a handmade product",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "material_cost": {
                            "type": "number",
                            "description": "Total cost of materials in dollars"
                        },
                        "hours_worked": {
                            "type": "number",
                            "description": "Number of hours spent creating the product"
                        },
                        "labor_rate": {
                            "type": "number",
                            "description": "Suggested hourly labor rate in dollars"
                        },
                        "uniqueness": {
                            "type": "number",
                            "description": "Rating of product uniqueness on scale of 1-10"
                        },
                        "demand": {
                            "type": "number",
                            "description": "Rating of market demand on scale of 1-10"
                        },
                        "selling_price": {
                            "type": "number",
                            "description": "Optional recommended selling price in dollars (0 means calculate automatically)"
                        },
                        "explanation": {
                            "type": "string",
                            "description": "Explanation for the recommendations"
                        }
                    },
                    "required": ["material_cost", "hours_worked", "labor_rate", "uniqueness", "demand", "explanation"]
                }
            }
            
            # Make the request with the JSON response format
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": 
                     """You are a pricing expert for handmade goods. Based on the conversation summary 
                     provided, recommend appropriate pricing parameters. Be realistic and consider 
                     the artisan's experience level, time investment, and material costs.
                     
                     You MUST respond with a valid JSON object containing the following fields:
                     - material_cost: Total cost of materials in dollars (number)
                     - hours_worked: Number of hours spent creating the product (number)
                     - labor_rate: Suggested hourly labor rate in dollars (number)
                     - uniqueness: Rating of product uniqueness on scale of 1-10 (number)
                     - demand: Rating of market demand on scale of 1-10 (number)
                     - selling_price: Optional recommended selling price in dollars (0 for automatic calculation) (number)
                     - explanation: Explanation for the recommendations (string)
                     
                     In most cases, set selling_price to 0 to let the system calculate the price automatically based on costs and market factors. Only provide a specific selling_price if there's a clear market price point that should be targeted regardless of costs.
                     
                     Ensure all number values are reasonable and appropriate.
                     """
                    },
                    {"role": "user", "content": f"Based on this conversation, recommend pricing parameters:\n\n{conversation_summary}"}
                ],
                response_format={"type": "json_object"},
                temperature=0.5,
                max_tokens=1000
            )
            
            # Parse the JSON response
            content = response.choices[0].message.content
            logger.info(f"Received response: {content}")
            
            try:
                data = json.loads(content)
                
                # Create the PricingRecommendation object with default selling_price of 0
                recommendation_data = {
                    "material_cost": data["material_cost"],
                    "hours_worked": data["hours_worked"],
                    "labor_rate": data["labor_rate"],
                    "uniqueness": data["uniqueness"],
                    "demand": data["demand"],
                    "explanation": data["explanation"]
                }
                
                # Only add selling_price if it's in the response and non-zero
                if "selling_price" in data and data["selling_price"] > 0:
                    recommendation_data["selling_price"] = data["selling_price"]
                
                recommendation = PricingRecommendation(**recommendation_data)
                
                return recommendation
                
            except (json.JSONDecodeError, KeyError) as e:
                logger.error(f"Error parsing response: {str(e)}, content: {content}")
                return None
            
        except Exception as e:
            logger.error(f"Error in pricing recommendation request: {str(e)}")
            return None 