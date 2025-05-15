#!/usr/bin/env python3
"""
Handmade Goods Pricing Assistant
Main application entry point
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.ui.app import PricingAssistantApp

def main():
    """Main entry point for the application"""
    app = PricingAssistantApp()
    
    # Ensure the application starts with appropriate size and centering
    root = app.root
    
    # Center the window on screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Calculate position
    window_width = min(1200, screen_width - 100)
    window_height = min(900, screen_height - 100)
    
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    
    # Set window size and position
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    app.run()

if __name__ == "__main__":
    main() 