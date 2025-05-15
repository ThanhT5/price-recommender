"""
Result frame for the Pricing Assistant
Displays calculation results and visualizations
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ResultFrame(ttk.Frame):
    """Result frame for displaying calculation results"""
    
    def __init__(self, parent):
        super().__init__(parent, padding="10")
        
        # Setting up variables for displaying results
        self.recommended_price_var = tk.StringVar(value="$0.00")
        self.base_price_var = tk.StringVar(value="$0.00")
        self.economy_price_var = tk.StringVar(value="$0.00")
        self.premium_price_var = tk.StringVar(value="$0.00")
        self.profit_amount_var = tk.StringVar(value="$0.00")
        self.profit_margin_var = tk.StringVar(value="0.0%")
        self.markup_percentage_var = tk.StringVar(value="0.0%")
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the results UI"""
        # Configure the frame for responsive layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)  # Make the chart frame expandable
        
        # Title
        title_label = ttk.Label(self, text="Price Recommendation", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        # Main price display
        price_frame = ttk.Frame(self)
        price_frame.grid(row=1, column=0, sticky="ew", pady=10)
        price_frame.columnconfigure(1, weight=1)
        
        ttk.Label(price_frame, text="Recommended Price:", font=("Arial", 12)).grid(
            row=0, column=0, sticky="w")
        ttk.Label(price_frame, textvariable=self.recommended_price_var, font=("Arial", 16, "bold")).grid(
            row=0, column=1, sticky="e", padx=10)
        
        # Price breakdown section
        breakdown_frame = ttk.LabelFrame(self, text="Price Breakdown", padding=10)
        breakdown_frame.grid(row=2, column=0, sticky="ew", pady=5)
        breakdown_frame.columnconfigure(1, weight=1)
        
        # Base price (cost)
        ttk.Label(breakdown_frame, text="Base Cost:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(breakdown_frame, textvariable=self.base_price_var).grid(
            row=0, column=1, sticky="e", pady=2)
        
        # Profit amount
        ttk.Label(breakdown_frame, text="Profit Amount:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(breakdown_frame, textvariable=self.profit_amount_var).grid(
            row=1, column=1, sticky="e", pady=2)
        
        # Profit margin
        ttk.Label(breakdown_frame, text="Profit Margin:").grid(row=2, column=0, sticky="w", pady=2)
        ttk.Label(breakdown_frame, textvariable=self.profit_margin_var, 
                 foreground="#4CAF50").grid(row=2, column=1, sticky="e", pady=2)
        
        # Markup percentage
        ttk.Label(breakdown_frame, text="Markup Percentage:").grid(row=3, column=0, sticky="w", pady=2)
        ttk.Label(breakdown_frame, textvariable=self.markup_percentage_var, 
                 foreground="#2196F3").grid(row=3, column=1, sticky="e", pady=2)
        
        # Horizontal separator
        ttk.Separator(breakdown_frame, orient=tk.HORIZONTAL).grid(
            row=4, column=0, columnspan=2, sticky="ew", pady=5)
        
        # Brief explanation 
        explanation_text = "Profit Margin: percentage of selling price that is profit\nMarkup: percentage of cost that is added as profit"
        ttk.Label(breakdown_frame, text=explanation_text, font=("Arial", 8, "italic"), 
                 foreground="gray").grid(row=5, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        # Chart placeholder
        self.chart_frame = ttk.Frame(self)
        self.chart_frame.grid(row=3, column=0, sticky="nsew", pady=10)
        self.chart_frame.columnconfigure(0, weight=1)
        self.chart_frame.rowconfigure(0, weight=1)
        
        # Price options
        options_frame = ttk.LabelFrame(self, text="Alternative Pricing Options", padding=10)
        options_frame.grid(row=4, column=0, sticky="ew", pady=5)
        options_frame.columnconfigure(1, weight=1)
        
        # Economy price
        ttk.Label(options_frame, text="Economy Price:").grid(row=0, column=0, sticky="w", pady=2)
        ttk.Label(options_frame, textvariable=self.economy_price_var).grid(
            row=0, column=1, sticky="e", pady=2)
        
        # Premium price
        ttk.Label(options_frame, text="Premium Price:").grid(row=1, column=0, sticky="w", pady=2)
        ttk.Label(options_frame, textvariable=self.premium_price_var).grid(
            row=1, column=1, sticky="e", pady=2)
        
        # Create initial empty chart
        self._create_empty_chart()
    
    def _create_empty_chart(self):
        """Create an empty placeholder chart"""
        # Clear any existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure with responsive sizing
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        self.fig.subplots_adjust(left=0.15, bottom=0.2, right=0.85, top=0.9)
        self.ax = self.fig.add_subplot(111)
        
        # Add text to empty chart
        self.ax.text(0.5, 0.5, "No data to display", 
                   ha='center', va='center', fontsize=12)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Create canvas with responsive sizing
        canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Make sure the canvas adjusts when the window is resized
        self.chart_frame.bind("<Configure>", lambda e: self._on_resize())
    
    def _on_resize(self):
        """Handle resizing of the chart"""
        if hasattr(self, 'fig') and self.fig is not None:
            self.fig.tight_layout()
            self.fig.canvas.draw_idle()
    
    def _create_price_breakdown_chart(self, result):
        """Create a chart showing the price breakdown"""
        # Clear any existing chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create figure with responsive sizing
        self.fig = plt.figure(figsize=(5, 3), dpi=100)
        # Increase top margin to prevent clipping
        self.fig.subplots_adjust(left=0.15, bottom=0.3, right=0.85, top=0.85)
        self.ax = self.fig.add_subplot(111)
        
        # Data for the chart
        components = ['Material', 'Labor', 'Factors', 'Profit']
        values = [
            result["material_cost"],
            result["labor_cost"],
            result["factor_adjustment"],
            result["profit_amount"]
        ]
        
        # Create bar chart with switched colors:
        # Original: Material (green), Labor (blue), Factors (yellow), Profit (red)
        # New: Material (red), Labor (yellow), Factors (blue), Profit (green)
        bars = self.ax.bar(components, values, color=['#F44336', '#FFC107', '#2196F3', '#4CAF50'])
        
        # Add labels and formatting
        self.ax.set_title('Price Components')
        self.ax.set_ylabel('Amount ($)')
        
        # Add values above bars
        for bar in bars:
            height = bar.get_height()
            self.ax.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'${height:.2f}', ha='center', va='bottom', fontsize=8)
        
        # Add padding to y-axis to prevent text clipping
        y_max = max(values) * 1.15  # Add 15% padding to the top
        self.ax.set_ylim(0, y_max)
        
        # Create canvas with responsive sizing
        canvas = FigureCanvasTkAgg(self.fig, master=self.chart_frame)
        canvas.draw()
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
        # Make sure the canvas adjusts when the window is resized
        self.chart_frame.bind("<Configure>", lambda e: self._on_resize())
    
    def update_results(self, result):
        """Update the display with calculation results"""
        # Format currency values
        self.recommended_price_var.set(f"${result['final_price']:.2f}")
        self.base_price_var.set(f"${result['base_price']:.2f}")
        self.economy_price_var.set(f"${result['economy_price']:.2f}")
        self.premium_price_var.set(f"${result['premium_price']:.2f}")
        self.profit_amount_var.set(f"${result['profit_amount']:.2f}")
        
        # Set profit margin and markup to N/A if selling price is 0
        if 'selling_price' in result and result['selling_price'] == 0:
            self.profit_margin_var.set("N/A")
            self.markup_percentage_var.set("N/A")
        else:
            self.profit_margin_var.set(f"{result['profit_margin_percentage']:.1f}%")
            self.markup_percentage_var.set(f"{result['markup_percentage']:.1f}%")
        
        # Update the chart
        self._create_price_breakdown_chart(result) 