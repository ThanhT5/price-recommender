"""
Input frame for the Pricing Assistant
Handles collecting user inputs for price calculation
"""

import tkinter as tk
from tkinter import ttk
from functools import partial

class InputFrame(ttk.Frame):
    """Input frame for collecting user input values"""
    
    def __init__(self, parent, calculate_callback):
        super().__init__(parent, padding="10")
        self.calculate_callback = calculate_callback
        
        # Default values
        self.default_values = {
            "material_cost": 10.0,
            "hours_worked": 2.0,
            "labor_rate": 15.0,
            "uniqueness": 5,
            "demand": 5,
            "selling_price": 0.0  # Default to 0 (indicating not set)
        }
        
        # Store recommended values (initially None)
        self.recommended_values = None
        
        # Input variables
        self.material_cost_var = tk.DoubleVar(value=self.default_values["material_cost"])
        self.hours_worked_var = tk.DoubleVar(value=self.default_values["hours_worked"])
        self.labor_rate_var = tk.DoubleVar(value=self.default_values["labor_rate"])
        self.uniqueness_var = tk.DoubleVar(value=self.default_values["uniqueness"])
        self.demand_var = tk.DoubleVar(value=self.default_values["demand"])
        self.selling_price_var = tk.DoubleVar(value=self.default_values["selling_price"])
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the input form UI"""
        # Configure the frame to be responsive
        self.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(self, text="Product Information", font=("Arial", 14, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 10))
        
        # Cost inputs section
        cost_frame = ttk.LabelFrame(self, text="Costs", padding=10)
        cost_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        # Configure cost frame columns for responsiveness
        cost_frame.columnconfigure(1, weight=1)
        
        # Material cost
        ttk.Label(cost_frame, text="Material Cost ($):").grid(row=0, column=0, sticky="w", pady=2)
        material_cost_entry = ttk.Entry(cost_frame, textvariable=self.material_cost_var, width=10)
        material_cost_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Hours worked
        ttk.Label(cost_frame, text="Hours Worked:").grid(row=1, column=0, sticky="w", pady=2)
        hours_worked_entry = ttk.Entry(cost_frame, textvariable=self.hours_worked_var, width=10)
        hours_worked_entry.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Labor rate
        ttk.Label(cost_frame, text="Labor Rate ($/hour):").grid(row=2, column=0, sticky="w", pady=2)
        labor_rate_entry = ttk.Entry(cost_frame, textvariable=self.labor_rate_var, width=10)
        labor_rate_entry.grid(row=2, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Factors section
        factors_frame = ttk.LabelFrame(self, text="Market Factors", padding=10)
        factors_frame.grid(row=2, column=0, sticky="ew", pady=5)
        
        # Configure factors frame columns for responsiveness
        factors_frame.columnconfigure(1, weight=1)
        
        # Uniqueness slider and entry
        ttk.Label(factors_frame, text="Uniqueness:").grid(row=0, column=0, sticky="w", pady=2)
        
        # Create a frame to hold the slider and entry side by side
        uniqueness_input_frame = ttk.Frame(factors_frame)
        uniqueness_input_frame.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 5))
        uniqueness_input_frame.columnconfigure(0, weight=1)
        
        # Create slider with value validation callback
        uniqueness_slider = ttk.Scale(uniqueness_input_frame, from_=1, to=10, 
                                  orient=tk.HORIZONTAL, command=self._validate_uniqueness)
        uniqueness_slider.set(self.uniqueness_var.get())  # Set initial value
        uniqueness_slider.grid(row=0, column=0, sticky="ew")
        
        # Add entry field directly (similar to cost fields)
        vcmd = (self.register(self._validate_float_input), '%P')
        uniqueness_entry = ttk.Entry(uniqueness_input_frame, textvariable=self.uniqueness_var, 
                               width=4, justify='center', validate="key", validatecommand=vcmd)
        uniqueness_entry.grid(row=0, column=1, padx=(10, 0))
        
        # Update slider when entry changes
        self.uniqueness_var.trace_add("write", lambda *args: self._sync_slider_from_entry(
            self.uniqueness_var, uniqueness_slider, 1.0, 10.0))
        
        # Handle slider release - snap to nearest 0.1
        def on_uniqueness_release(event):
            current = float(uniqueness_slider.get())
            rounded = round(current * 10) / 10  # Round to nearest 0.1
            uniqueness_slider.set(rounded)
            self.uniqueness_var.set(rounded)
        
        uniqueness_slider.bind("<ButtonRelease-1>", on_uniqueness_release)
        
        # Also round during the slider drag operation
        def on_uniqueness_motion(value):
            rounded = round(float(value) * 10) / 10  # Round to nearest 0.1
            self.uniqueness_var.set(rounded)
            return rounded
        
        uniqueness_slider.configure(command=on_uniqueness_motion)
        
        # Demand slider and entry
        ttk.Label(factors_frame, text="Demand:").grid(row=1, column=0, sticky="w", pady=2)
        
        # Create a frame to hold the slider and entry side by side
        demand_input_frame = ttk.Frame(factors_frame)
        demand_input_frame.grid(row=1, column=1, sticky="ew", pady=2, padx=(5, 5))
        demand_input_frame.columnconfigure(0, weight=1)
        
        # Create slider with value validation callback
        demand_slider = ttk.Scale(demand_input_frame, from_=1, to=10, 
                              orient=tk.HORIZONTAL, command=self._validate_demand)
        demand_slider.set(self.demand_var.get())  # Set initial value
        demand_slider.grid(row=0, column=0, sticky="ew")
        
        # Add entry field directly (similar to cost fields)
        demand_entry = ttk.Entry(demand_input_frame, textvariable=self.demand_var, 
                           width=4, justify='center', validate="key", validatecommand=vcmd)
        demand_entry.grid(row=0, column=1, padx=(10, 0))
        
        # Update slider when entry changes
        self.demand_var.trace_add("write", lambda *args: self._sync_slider_from_entry(
            self.demand_var, demand_slider, 1.0, 10.0))
        
        # Handle slider release - snap to nearest 0.1
        def on_demand_release(event):
            current = float(demand_slider.get())
            rounded = round(current * 10) / 10  # Round to nearest 0.1
            demand_slider.set(rounded)
            self.demand_var.set(rounded)
        
        demand_slider.bind("<ButtonRelease-1>", on_demand_release)
        
        # Also round during the slider drag operation
        def on_demand_motion(value):
            rounded = round(float(value) * 10) / 10  # Round to nearest 0.1
            self.demand_var.set(rounded)
            return rounded
        
        demand_slider.configure(command=on_demand_motion)
        
        # Price section (renamed from Profit section)
        price_frame = ttk.LabelFrame(self, text="Price Input (Optional)", padding=10)
        price_frame.grid(row=3, column=0, sticky="ew", pady=5)
        
        # Configure price frame columns for responsiveness
        price_frame.columnconfigure(1, weight=1)
        
        # Selling price (optional)
        ttk.Label(price_frame, text="Your Selling Price ($):").grid(row=0, column=0, sticky="w", pady=2)
        selling_price_entry = ttk.Entry(price_frame, textvariable=self.selling_price_var, width=10)
        selling_price_entry.grid(row=0, column=1, sticky="ew", pady=2, padx=(5, 0))
        
        # Help text
        ttk.Label(price_frame, text="Leave at 0 to get a suggested price", font=("Arial", 8, "italic"), 
                 foreground="gray").grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        # Scenario buttons
        scenarios_frame = ttk.LabelFrame(self, text="Sample Scenarios", padding=10)
        scenarios_frame.grid(row=4, column=0, sticky="ew", pady=5)
        
        # Configure scenarios frame columns for responsiveness
        scenarios_frame.columnconfigure(0, weight=1)
        scenarios_frame.columnconfigure(1, weight=1)
        scenarios_frame.columnconfigure(2, weight=1)
        
        # Scenario 1: Simple Jewelry
        ttk.Button(scenarios_frame, text="Simple Jewelry", 
                  command=partial(self._load_scenario, 1)).grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        
        # Scenario 2: Complex Art
        ttk.Button(scenarios_frame, text="Complex Art", 
                  command=partial(self._load_scenario, 2)).grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        
        # Scenario 3: Batch Production
        ttk.Button(scenarios_frame, text="Batch Item", 
                  command=partial(self._load_scenario, 3)).grid(row=0, column=2, padx=5, pady=5, sticky="ew")
        
        # Calculate button
        calculate_button = ttk.Button(self, text="Calculate Price", command=self.calculate_callback)
        calculate_button.grid(row=5, column=0, sticky="ew", pady=10)
        
        # Reset buttons frame
        reset_frame = ttk.Frame(self)
        reset_frame.grid(row=6, column=0, sticky="ew")
        reset_frame.columnconfigure(0, weight=1)
        reset_frame.columnconfigure(1, weight=1)
        
        # Reset to defaults button
        reset_default_button = ttk.Button(reset_frame, text="Reset to Defaults", command=self._reset_to_defaults)
        reset_default_button.grid(row=0, column=0, sticky="ew", padx=(0, 2))
        
        # Reset to recommendations button (initially disabled)
        self.reset_recom_button = ttk.Button(reset_frame, text="Reset to Recommendations", 
                                       command=self._reset_to_recommendations, state=tk.DISABLED)
        self.reset_recom_button.grid(row=0, column=1, sticky="ew", padx=(2, 0))
    
    def _load_scenario(self, scenario_num):
        """Load a predefined scenario"""
        if scenario_num == 1:
            # Simple Jewelry
            self.material_cost_var.set(5.0)
            self.hours_worked_var.set(2.0)
            self.labor_rate_var.set(15.0)
            self.uniqueness_var.set(6.0)
            self.demand_var.set(7.0)
            self.selling_price_var.set(0.0)  # Not set, use suggested price
        elif scenario_num == 2:
            # Complex Art
            self.material_cost_var.set(25.0)
            self.hours_worked_var.set(8.0)
            self.labor_rate_var.set(20.0)
            self.uniqueness_var.set(9.0)
            self.demand_var.set(5.0)
            self.selling_price_var.set(0.0)  # Not set, use suggested price
        elif scenario_num == 3:
            # Batch Production
            self.material_cost_var.set(3.0)
            self.hours_worked_var.set(0.5)
            self.labor_rate_var.set(15.0)
            self.uniqueness_var.set(4.0)
            self.demand_var.set(8.0)
            self.selling_price_var.set(0.0)  # Not set, use suggested price
    
    def _reset_values(self):
        """Reset values based on what's available (kept for compatibility)"""
        if self.recommended_values:
            self._reset_to_recommendations()
        else:
            self._reset_to_defaults()
    
    def _reset_to_defaults(self):
        """Reset all values to original defaults"""
        self.material_cost_var.set(self.default_values["material_cost"])
        self.hours_worked_var.set(self.default_values["hours_worked"])
        self.labor_rate_var.set(self.default_values["labor_rate"])
        self.uniqueness_var.set(float(self.default_values["uniqueness"]))
        self.demand_var.set(float(self.default_values["demand"]))
        self.selling_price_var.set(self.default_values["selling_price"])
    
    def _reset_to_recommendations(self):
        """Reset all values to AI recommendations (if available)"""
        if not self.recommended_values:
            return
            
        self.material_cost_var.set(self.recommended_values["material_cost"])
        self.hours_worked_var.set(self.recommended_values["hours_worked"])
        self.labor_rate_var.set(self.recommended_values["labor_rate"])
        self.uniqueness_var.set(self.recommended_values["uniqueness"])
        self.demand_var.set(self.recommended_values["demand"])
        if "selling_price" in self.recommended_values:
            self.selling_price_var.set(self.recommended_values["selling_price"])
        else:
            self.selling_price_var.set(0.0)  # Not set, use suggested price
    
    def set_recommendations(self, recommendations):
        """
        Store AI recommendations for this session
        
        Args:
            recommendations: Dictionary with recommended values or PricingRecommendation object
        """
        # Allow passing either a dictionary or a PricingRecommendation object
        if hasattr(recommendations, "__dict__"):
            # Convert PricingRecommendation object to dict
            self.recommended_values = {
                "material_cost": recommendations.material_cost,
                "hours_worked": recommendations.hours_worked,
                "labor_rate": recommendations.labor_rate,
                "uniqueness": recommendations.uniqueness,
                "demand": recommendations.demand
            }
            # Only add selling_price if it exists
            if hasattr(recommendations, "selling_price"):
                self.recommended_values["selling_price"] = recommendations.selling_price
        else:
            # Already a dictionary
            self.recommended_values = recommendations
            
        # Enable the recommendations reset button
        self.reset_recom_button.config(state=tk.NORMAL)
    
    def get_values(self):
        """Get all input values as a dictionary"""
        # Validate inputs
        material_cost = self.material_cost_var.get()
        hours_worked = self.hours_worked_var.get()
        labor_rate = self.labor_rate_var.get()
        uniqueness = round(self.uniqueness_var.get(), 1)  # Round to 1 decimal place
        demand = round(self.demand_var.get(), 1)          # Round to 1 decimal place
        selling_price = self.selling_price_var.get()
        
        # Validate that all numeric inputs are positive
        if material_cost < 0:
            raise ValueError("Material cost cannot be negative")
        if hours_worked < 0:
            raise ValueError("Hours worked cannot be negative")
        if labor_rate < 0:
            raise ValueError("Labor rate cannot be negative")
        if selling_price < 0:
            raise ValueError("Selling price cannot be negative")
        
        # Return a dictionary of validated values
        return {
            "material_cost": material_cost,
            "hours_worked": hours_worked,
            "labor_rate": labor_rate,
            "uniqueness": uniqueness,
            "demand": demand,
            "selling_price": selling_price
        }
    
    def _validate_float_input(self, value):
        """Validate that the input can be converted to a float"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _validate_uniqueness(self, value):
        """Update the uniqueness variable when the slider is moved"""
        self.uniqueness_var.set(round(float(value), 1))
        return True
    
    def _validate_demand(self, value):
        """Update the demand variable when the slider is moved"""
        self.demand_var.set(round(float(value), 1))
        return True
    
    def _sync_slider_from_entry(self, var, slider, min_val, max_val):
        """Sync slider position from the entry value"""
        try:
            value = float(var.get())
            value = max(min_val, min(max_val, value))  # Clamp to valid range
            slider.set(value)
        except (ValueError, tk.TclError):
            pass  # Ignore invalid values 