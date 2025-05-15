"""
Main UI application for the Pricing Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox
from src.logic.pricing import PricingCalculator
from src.ui.input_frame import InputFrame
from src.ui.result_frame import ResultFrame
from src.ui.welcome_screen import WelcomeScreen
from src.ui.chat_frame import ChatFrame
from src.ai.models import PricingRecommendation
from src.ai.chat_handler import ChatHandler
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PricingAssistantApp:
    """Main application class for the Handmade Goods Pricing Assistant"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Handmade Goods Pricing Assistant")
        # Increase default window size and set a minimum that works better
        self.root.geometry("1024x768")
        self.root.minsize(900, 650)
        
        # Set weight to rows and columns to make the UI more responsive
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.calculator = PricingCalculator()
        
        # Create a chat handler that can be reused
        self.chat_handler = ChatHandler()
        
        # Initialize the UI with a welcome screen
        self._show_welcome_screen()
    
    def _show_welcome_screen(self):
        """Show the welcome screen with options"""
        self._clear_main_frame()
        
        # Create welcome screen
        self.welcome_screen = WelcomeScreen(
            self.root,
            show_chat_callback=self._show_chat,
            show_calculator_callback=self._setup_ui
        )
        self.welcome_screen.pack(fill=tk.BOTH, expand=True)
    
    def _show_chat(self):
        """Show the chat interface"""
        self._clear_main_frame()
        
        # Reset the chat handler to start a fresh conversation
        self.chat_handler.reset_conversation()
        
        # Create chat frame with our existing chat handler
        self.chat_frame = ChatFrame(
            self.root,
            on_recommendations_ready=self._apply_recommendations,
            on_cancel=self._setup_ui,
            chat_handler=self.chat_handler
        )
        
        self.chat_frame.pack(fill=tk.BOTH, expand=True)
    
    def _clear_main_frame(self):
        """Clear any existing frames"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _apply_recommendations(self, recommendations: PricingRecommendation):
        """
        Apply AI recommendations to the input form
        
        Args:
            recommendations: PricingRecommendation object with recommended values
        """
        # First set up the calculator UI
        self._setup_ui()
        
        # Save the AI recommendations for the current session
        self.input_frame.set_recommendations({
            "material_cost": recommendations.material_cost,
            "hours_worked": recommendations.hours_worked,
            "labor_rate": recommendations.labor_rate,
            "uniqueness": recommendations.uniqueness,
            "demand": recommendations.demand,
            "selling_price": recommendations.selling_price if recommendations.selling_price > 0 else 0.0
        })
        
        # Then immediately apply them to the form
        self.input_frame._reset_to_recommendations()
        
        # Calculate and update results based on new values
        self._calculate_price()
        
        # Show a message about the source of the values
        messagebox.showinfo(
            "AI Recommendations Applied",
            f"The pricing parameters have been set based on AI recommendations.\n\n"
            f"Explanation: {recommendations.explanation}"
        )
    
    def _setup_ui(self):
        """Set up the main UI components"""
        self._clear_main_frame()
        
        # Create main frames
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure main frame for responsiveness
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create a notebook for different tabs
        self.notebook = ttk.Notebook(self.main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create main tabs
        self.calculator_tab = ttk.Frame(self.notebook)
        self.help_tab = ttk.Frame(self.notebook)
        
        # Configure tabs for responsiveness
        for tab in [self.calculator_tab, self.help_tab]:
            tab.columnconfigure(0, weight=1)
            tab.rowconfigure(0, weight=1)
        
        self.notebook.add(self.calculator_tab, text="Price Calculator")
        self.notebook.add(self.help_tab, text="Help")
        
        # Set up calculator tab
        self._setup_calculator_tab()
        
        # Set up help tab
        self._setup_help_tab()
        
        # Set up the menu
        self._setup_menu()
    
    def _setup_calculator_tab(self):
        """Set up the main calculator tab UI"""
        # Split into left (input) and right (results) frames
        calc_container = ttk.Frame(self.calculator_tab)
        calc_container.pack(fill=tk.BOTH, expand=True)
        
        # Add AI Chat button at the top
        ai_button_frame = ttk.Frame(calc_container, padding="5")
        ai_button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        switch_to_ai_btn = ttk.Button(
            ai_button_frame,
            text="Switch to AI Assistant",
            command=self._show_chat
        )
        switch_to_ai_btn.pack(side=tk.RIGHT)
        
        # Add the paned window below the button
        self.calc_paned = ttk.PanedWindow(calc_container, orient=tk.HORIZONTAL)
        self.calc_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input frame
        self.input_frame = InputFrame(self.calc_paned, self._calculate_price)
        
        # Result frame
        self.result_frame = ResultFrame(self.calc_paned)
        
        # Add frames to paned window with appropriate weights
        self.calc_paned.add(self.input_frame, weight=40)
        self.calc_paned.add(self.result_frame, weight=60)
        
        # Schedule the sash position to be set after rendering
        self.root.after(100, self._set_paned_position)
    
    def _set_paned_position(self):
        """Set the initial position of the paned window divider"""
        width = self.calculator_tab.winfo_width()
        if width > 10:  # Only set if we have a valid width
            self.calc_paned.sashpos(0, int(width * 0.4))
    
    def _setup_help_tab(self):
        """Set up the help tab UI"""
        # Create a frame for the help content
        help_frame = ttk.Frame(self.help_tab, padding="10")
        help_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Add a title
        title_label = ttk.Label(help_frame, text="How to Use the Pricing Assistant", 
                              font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Add help text using a text widget
        help_text = tk.Text(help_frame, wrap=tk.WORD, height=20, width=80)
        help_text.grid(row=1, column=0, sticky="nsew")
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(help_frame, orient=tk.VERTICAL, command=help_text.yview)
        scrollbar.grid(row=1, column=1, sticky="ns")
        help_text['yscrollcommand'] = scrollbar.set
        
        # Configure the grid
        help_frame.columnconfigure(0, weight=1)
        help_frame.rowconfigure(1, weight=1)
        
        # Add help content
        help_content = """
Handmade Goods Pricing Assistant Help

This application helps you determine optimal pricing for your handmade products based on various factors.

AI Assistant:
--------------------
The application provides an AI assistant to help recommend pricing parameters based on a conversation about your product. To use this feature:

1. Select "Use AI Pricing Assistant" on the welcome screen.
2. Chat with the AI about your product, materials, time investment, and other factors.
3. When ready, click "Get Recommendations" to generate pricing parameters.
4. Review and apply the recommendations to the calculator.

Price Calculator Tab:
--------------------
1. Enter your product's details in the input fields:
   - Material Cost: The total cost of materials used in your product.
   - Hours Worked: The number of hours spent creating the product.
   - Labor Rate: Your desired hourly rate for your time.
   - Uniqueness: How unique your product is on a scale of 1-10.
   - Demand: The market demand for your product on a scale of 1-10.
   - Selling Price (Optional): Your desired selling price. Leave at 0 for a suggested price.

2. Click the "Calculate Price" button to see the recommended price and profit information.

3. The results panel will show:
   - The recommended or user-defined price
   - Your profit amount and percentage
   - A breakdown of price components
   - Alternative pricing options (economy and premium)

Tips for Pricing:
---------------
- Material Cost: Be sure to include all materials, even small amounts.
- Labor Rate: Consider your skill level and the local market rates.
- Uniqueness: Higher for items that require special skills or are one-of-a-kind.
- Demand: Higher for items with proven market interest or during peak seasons.
- Profit Analysis: The app will calculate both profit margin (% of selling price) and markup (% of costs).

The pricing formula takes all these factors into account to help you determine a fair and sustainable price for your handmade goods.
"""
        help_text.insert(tk.END, help_content)
        help_text.configure(state='disabled')  # Make the text read-only
    
    def _setup_menu(self):
        """Set up the application menu"""
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="AI Assistant", command=self._show_chat)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        # Set the menu
        self.root.config(menu=self.menu_bar)
    
    def _calculate_price(self):
        """Calculate the price based on the current input values"""
        try:
            # Get values from input frame
            values = self.input_frame.get_values()
            
            # Calculate the price
            results = self.calculator.calculate_price(**values)
            
            # Update the results display
            self.result_frame.update_results(results)
            
        except ValueError as e:
            # Show error message
            messagebox.showerror("Invalid Input", str(e))
        except Exception as e:
            # Log the error and show a generic message
            logger.exception("Error calculating price")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About Handmade Goods Pricing Assistant",
            "Handmade Goods Pricing Assistant v1.0\n\n"
            "This application helps artisans price their handmade goods fairly and profitably."
        )
    
    def run(self):
        """Run the application"""
        self.root.mainloop() 