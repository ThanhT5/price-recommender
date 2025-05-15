"""
Chat interface for interacting with the AI assistant.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, font
from typing import Callable, Optional
import threading
import time

from src.ai.chat_handler import ChatHandler
from src.ai.models import PricingRecommendation
from src.ai.config import DEFAULT_PRICING_PARAMETERS

class ChatFrame(ttk.Frame):
    """
    Chat interface for interacting with the AI assistant.
    """
    
    def __init__(self, parent, on_recommendations_ready: Callable, on_cancel: Callable, chat_handler: Optional[ChatHandler] = None):
        """
        Initialize the chat frame.
        
        Args:
            parent: Parent widget
            on_recommendations_ready: Callback function when recommendations are ready
            on_cancel: Callback function when chat is cancelled
            chat_handler: Optional existing ChatHandler instance to use
        """
        super().__init__(parent, padding="10")
        self.parent = parent
        self.on_recommendations_ready = on_recommendations_ready
        self.on_cancel = on_cancel
        
        # Initialize chat handler
        self.chat_handler = chat_handler or ChatHandler()
        
        # UI state variables
        self.waiting_for_response = False
        
        self._setup_ui()
        self._start_conversation()
    
    def _setup_ui(self):
        """Set up the chat UI."""
        # Configure for responsive layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.columnconfigure(0, weight=1)
        content_frame.rowconfigure(0, weight=1)
        
        # Chat history display
        self.chat_history = scrolledtext.ScrolledText(
            content_frame, 
            wrap=tk.WORD,
            width=60,
            height=20,
            font=("Arial", 10)
        )
        self.chat_history.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.chat_history.config(state=tk.DISABLED)
        
        # Tag configuration for different message types
        self.chat_history.tag_configure("user", foreground="#0055aa", font=("Arial", 10, "bold"))
        self.chat_history.tag_configure("assistant", foreground="#008800", font=("Arial", 10, "bold"))
        self.chat_history.tag_configure("system", foreground="#888888", font=("Arial", 9, "italic"))
        
        # User input area
        input_frame = ttk.Frame(content_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
        input_frame.columnconfigure(0, weight=1)
        
        self.message_input = ttk.Entry(input_frame, font=("Arial", 10))
        self.message_input.grid(row=0, column=0, sticky="ew", padx=(0, 5))
        self.message_input.bind("<Return>", lambda e: self._send_message())
        
        # Send button
        self.send_button = ttk.Button(
            input_frame, 
            text="Send", 
            command=self._send_message
        )
        self.send_button.grid(row=0, column=1)
        
        # Action buttons
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
        
        # Get recommendations button
        self.get_recommendations_button = ttk.Button(
            button_frame, 
            text="Get Recommendations",
            command=self._request_recommendations,
            state=tk.DISABLED
        )
        self.get_recommendations_button.pack(side=tk.LEFT, padx=5)
        
        # Switch to Calculator button
        self.toggle_button = ttk.Button(
            button_frame, 
            text="Switch to Calculator",
            command=lambda: self.on_cancel()
        )
        self.toggle_button.pack(side=tk.RIGHT, padx=5)
    
    def _start_conversation(self):
        """Start the initial conversation with the AI."""
        self._add_message("system", "Starting conversation with AI assistant...")
        
        # Start in a separate thread to avoid blocking UI
        threading.Thread(target=self._initial_greeting).start()
        
        # Enable the recommendations button after a reasonable chat
        self.after(10000, lambda: self.get_recommendations_button.config(state=tk.NORMAL))
    
    def _initial_greeting(self):
        """Get the initial greeting from the AI."""
        initial_prompt = "Hello! I'm looking for help with pricing a handmade item."
        response = self.chat_handler.send_message(initial_prompt)
        
        if response:
            # Update UI in the main thread
            self.after(0, lambda: self._add_message("assistant", response))
        else:
            self.after(0, lambda: self._add_message("system", 
                                                   "AI assistant is not available. You can still "
                                                   "use the calculator directly."))
    
    def _add_message(self, sender_type, message):
        """
        Add a message to the chat history.
        
        Args:
            sender_type: Type of sender ("user", "assistant", or "system")
            message: Message text
        """
        self.chat_history.config(state=tk.NORMAL)
        
        if sender_type == "user":
            self.chat_history.insert(tk.END, "You: ", "user")
        elif sender_type == "assistant":
            self.chat_history.insert(tk.END, "AI Assistant: ", "assistant")
        else:  # system message
            self.chat_history.insert(tk.END, "System: ", "system")
        
        self.chat_history.insert(tk.END, f"{message}\n\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.see(tk.END)
    
    def _send_message(self):
        """Send the user message to the AI."""
        user_message = self.message_input.get().strip()
        if not user_message or self.waiting_for_response:
            return
        
        # Clear input field
        self.message_input.delete(0, tk.END)
        
        # Add user message to chat
        self._add_message("user", user_message)
        
        # Disable input while waiting for response
        self.waiting_for_response = True
        self.send_button.config(state=tk.DISABLED)
        self.message_input.config(state=tk.DISABLED)
        
        # Show typing indicator
        self._add_message("system", "AI is typing...")
        
        # Process in a thread to avoid blocking UI
        threading.Thread(target=self._process_message, args=(user_message,)).start()
    
    def _process_message(self, user_message):
        """
        Process the message in a separate thread.
        
        Args:
            user_message: Message from user
        """
        response = self.chat_handler.send_message(user_message)
        
        # Update UI in the main thread
        self.after(0, lambda: self._handle_response(response))
    
    def _handle_response(self, response):
        """
        Handle the AI response.
        
        Args:
            response: Response from AI
        """
        # Remove typing indicator (last 2 lines + newlines)
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.delete("end-3l", "end")
        self.chat_history.config(state=tk.DISABLED)
        
        if response:
            self._add_message("assistant", response)
        else:
            self._add_message("system", "No response from AI. Please try again or use the calculator directly.")
        
        # Re-enable input
        self.waiting_for_response = False
        self.send_button.config(state=tk.NORMAL)
        self.message_input.config(state=tk.NORMAL)
        self.message_input.focus()
        
        # Always enable get recommendations after a response
        self.get_recommendations_button.config(state=tk.NORMAL)
    
    def _request_recommendations(self):
        """Request pricing recommendations from the AI."""
        self._add_message("system", "Generating pricing recommendations based on our conversation...")
        
        # Disable buttons while processing
        self.get_recommendations_button.config(state=tk.DISABLED)
        self.send_button.config(state=tk.DISABLED)
        self.message_input.config(state=tk.DISABLED)
        
        # Process in a thread
        threading.Thread(target=self._generate_recommendations).start()
    
    def _generate_recommendations(self):
        """Generate the recommendations in a separate thread."""
        recommendations = self.chat_handler.get_recommendations()
        
        # If no recommendations and no AI client, create a fallback recommendation
        if recommendations is None and (not self.chat_handler.ai_client.is_available()):
            # Create a fallback recommendation based on the conversation and default values
            recommendations = PricingRecommendation(
                material_cost=DEFAULT_PRICING_PARAMETERS["material_cost"],
                hours_worked=DEFAULT_PRICING_PARAMETERS["hours_worked"],
                labor_rate=DEFAULT_PRICING_PARAMETERS["labor_rate"],
                uniqueness=DEFAULT_PRICING_PARAMETERS["uniqueness"],
                demand=DEFAULT_PRICING_PARAMETERS["demand"],
                selling_price=DEFAULT_PRICING_PARAMETERS["selling_price"],
                explanation="These are default recommendations since the AI is not available. "
                          "In a real scenario, these would be generated based on our conversation."
            )
            
            # Log the fallback recommendations
            self.after(0, lambda: self._add_message("system", 
                "Using default recommendations since the AI is not available. "
                "Enter your OpenAI API key in the .env file to enable AI features."))
        
        # Update UI in the main thread
        self.after(0, lambda: self._display_recommendations(recommendations))
    
    def _display_recommendations(self, recommendations: Optional[PricingRecommendation]):
        """
        Display the recommendations and notify parent.
        
        Args:
            recommendations: PricingRecommendation object or None if the request failed
        """
        if recommendations:
            # Show recommendations in chat
            summary = (
                f"Based on our conversation, here are my recommendations:\n\n"
                f"Material Cost: ${recommendations.material_cost:.2f}\n"
                f"Hours Worked: {recommendations.hours_worked:.1f}\n"
                f"Labor Rate: ${recommendations.labor_rate:.2f}/hour\n"
                f"Uniqueness: {recommendations.uniqueness:.1f}/10\n"
                f"Demand: {recommendations.demand:.1f}/10\n"
                f"Selling Price: {'Auto-calculate' if recommendations.selling_price == 0 else f'${recommendations.selling_price:.2f}'}\n\n"
                f"Explanation: {recommendations.explanation}"
            )
            
            self._add_message("assistant", summary)
            
            # Remove any existing apply button
            for widget in self.winfo_children():
                if isinstance(widget, ttk.Button) and widget.cget("text") == "Apply Recommendations":
                    widget.destroy()
            
            # Create a new button frame at the bottom
            button_frame = ttk.Frame(self)
            button_frame.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
            
            # Create Apply button in this frame
            apply_button = ttk.Button(
                button_frame, 
                text="Apply Recommendations",
                command=lambda: self.on_recommendations_ready(recommendations)
            )
            apply_button.pack(fill=tk.X, expand=True, padx=5, pady=5)
            
            # Re-enable input 
            self.get_recommendations_button.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.message_input.config(state=tk.NORMAL)
        else:
            self._add_message("system", "Could not generate recommendations. "
                              "You can still use the calculator directly.")
            
            # Re-enable buttons
            self.get_recommendations_button.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.message_input.config(state=tk.NORMAL) 