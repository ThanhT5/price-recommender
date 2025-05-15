"""
Welcome screen for the Handmade Goods Pricing Assistant.
Provides options to use the AI assistant or go directly to the calculator.
"""

import tkinter as tk
from tkinter import ttk, font

class WelcomeScreen(ttk.Frame):
    """
    Welcome screen with options to use the AI assistant or go directly to the calculator.
    """
    
    def __init__(self, parent, show_chat_callback, show_calculator_callback):
        """
        Initialize the welcome screen.
        
        Args:
            parent: Parent widget
            show_chat_callback: Callback function to show the chat screen
            show_calculator_callback: Callback function to show the calculator screen
        """
        super().__init__(parent, padding="20")
        self.parent = parent
        self.show_chat_callback = show_chat_callback
        self.show_calculator_callback = show_calculator_callback
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the welcome screen UI."""
        # Configure for responsive layout
        self.columnconfigure(0, weight=1)
        
        # Create a container frame to center all content
        center_container = ttk.Frame(self)
        center_container.grid(row=0, column=0, sticky="ns")
        
        # Logo/Title section
        logo_frame = ttk.Frame(center_container)
        logo_frame.pack(pady=20)
        
        # Title
        title_font = font.Font(family="Arial", size=18, weight="bold")
        title = ttk.Label(
            logo_frame, 
            text="Handmade Goods Pricing Assistant",
            font=title_font
        )
        title.pack(anchor="center")
        
        # Subtitle
        subtitle_font = font.Font(family="Arial", size=12)
        subtitle = ttk.Label(
            logo_frame, 
            text="Helping artisans price their creations fairly and profitably",
            font=subtitle_font
        )
        subtitle.pack(anchor="center", pady=(5, 0))
        
        # Options section
        options_frame = ttk.Frame(center_container, padding="10")
        options_frame.pack(pady=20)
        
        # Description
        description = ttk.Label(
            options_frame,
            text="Choose how you'd like to use the application:",
            font=subtitle_font
        )
        description.pack(anchor="center", pady=(0, 20))
        
        # AI Assistant option
        ai_button_frame = ttk.Frame(options_frame, padding="5")
        ai_button_frame.pack(pady=10)
        
        ai_icon = ttk.Label(ai_button_frame, text="🤖")  # Robot emoji as icon
        ai_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        ai_button_content = ttk.Frame(ai_button_frame)
        ai_button_content.pack(side=tk.LEFT)
        
        ai_button = ttk.Button(
            ai_button_content,
            text="Use AI Pricing Assistant",
            command=self.show_chat_callback,
            style="Accent.TButton",
            width=40
        )
        ai_button.pack(anchor="w")
        
        ai_description = ttk.Label(
            ai_button_content,
            text="Get personalized pricing recommendations through a conversation",
            wraplength=400
        )
        ai_description.pack(anchor="w", pady=(5, 0))
        
        # Calculator option
        calc_button_frame = ttk.Frame(options_frame, padding="5")
        calc_button_frame.pack(pady=10)
        
        calc_icon = ttk.Label(calc_button_frame, text="🧮")  # Abacus emoji as icon
        calc_icon.pack(side=tk.LEFT, padx=(0, 10))
        
        calc_button_content = ttk.Frame(calc_button_frame)
        calc_button_content.pack(side=tk.LEFT)
        
        calc_button = ttk.Button(
            calc_button_content,
            text="Go Directly to Calculator",
            command=self.show_calculator_callback,
            width=40
        )
        calc_button.pack(anchor="w")
        
        calc_description = ttk.Label(
            calc_button_content,
            text="Skip the AI chat and manually enter pricing parameters",
            wraplength=400
        )
        calc_description.pack(anchor="w", pady=(5, 0))
        
        # Info section
        info_frame = ttk.Frame(center_container, padding="10")
        info_frame.pack(pady=20)
        
        # Use a Label instead of Text widget to avoid background issues
        info_label = ttk.Label(
            info_frame, 
            text="The AI assistant will help you determine the best pricing parameters " 
                 "by asking about your product, materials, time investment, and market factors. " 
                 "Your responses will guide it to recommend appropriate values for the calculator.",
            wraplength=600,
            justify=tk.CENTER
        )
        info_label.pack(fill=tk.X) 