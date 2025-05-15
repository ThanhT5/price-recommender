"""
Handler for managing chat conversations with the AI.
"""

import logging
from typing import List, Dict, Optional
from .client import AIClient
from .config import PRICING_ADVISOR_PROMPT
from .models import PricingRecommendation

logger = logging.getLogger(__name__)

class ChatHandler:
    """
    Handler for managing chat conversations with the AI.
    Tracks conversation history and provides methods for interacting with the AI.
    """
    
    def __init__(self, ai_client: Optional[AIClient] = None):
        """
        Initialize the chat handler.
        
        Args:
            ai_client: AIClient instance or None to create a new one
        """
        self.ai_client = ai_client or AIClient()
        self.conversation_history = []
        self._initialize_conversation()
        
    def _initialize_conversation(self):
        """Initialize the conversation with the system prompt."""
        self.conversation_history = [
            {"role": "system", "content": PRICING_ADVISOR_PROMPT}
        ]
    
    def send_message(self, user_message: str) -> Optional[str]:
        """
        Send a message to the AI and get a response.
        
        Args:
            user_message: Message from the user
            
        Returns:
            Response from the AI or None if the request fails
        """
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": user_message})
        
        # Get response from AI
        response = self.ai_client.chat_completion(self.conversation_history)
        
        if response:
            # Add AI response to history
            self.conversation_history.append({"role": "assistant", "content": response})
            return response
        else:
            logger.warning("No response from AI")
            return None
    
    def get_recommendations(self) -> Optional[PricingRecommendation]:
        """
        Get pricing recommendations based on the conversation history.
        
        Returns:
            PricingRecommendation object or None if the request fails
        """
        # Check if we have enough conversation history
        if len(self.conversation_history) < 3:
            logger.warning("Not enough conversation history to generate recommendations")
            return None
            
        logger.info(f"Generating recommendations based on {len(self.conversation_history)} messages")
        
        # Create a summary of the conversation for the recommendation request
        conversation_summary = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" 
            for msg in self.conversation_history
        ])
        
        logger.debug(f"Conversation summary: {conversation_summary[:500]}...")
        
        try:
            recommendations = self.ai_client.get_pricing_recommendation(conversation_summary)
            
            if recommendations:
                logger.info(f"Successfully generated recommendations: {recommendations}")
                return recommendations
            else:
                logger.error("Failed to generate recommendations - no data returned")
                return None
                
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return None
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self._initialize_conversation()
        
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """
        Get the conversation history.
        
        Returns:
            List of message dictionaries
        """
        return self.conversation_history 