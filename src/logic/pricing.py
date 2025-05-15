"""
Core pricing logic for the Handmade Goods Pricing Assistant
Handles all price calculations and formulas
"""

class PricingCalculator:
    """Calculator that determines optimal pricing for handmade goods"""
    
    def __init__(self):
        # Default weight values for the price modifiers
        self.uniqueness_weight = 0.05  # 5% per point on 1-10 scale
        self.demand_weight = 0.04      # 4% per point on 1-10 scale
        
        # Price variation modifiers
        self.economy_modifier = 0.85   # Economy price is 85% of standard
        self.premium_modifier = 1.25   # Premium price is 125% of standard
        
        # Suggested price multipliers
        self.suggested_price_multiplier = 2.0  # Default suggested price is 2x costs (100% profit)
    
    def calculate_price(self, material_cost, hours_worked, labor_rate, 
                        uniqueness, demand, selling_price=None):
        """
        Calculate pricing information for a handmade product
        
        Args:
            material_cost: Cost of materials in dollars
            hours_worked: Number of hours spent creating the product
            labor_rate: Hourly labor rate in dollars
            uniqueness: Rating of product uniqueness (1-10)
            demand: Rating of product demand (1-10)
            selling_price: Optional - user's set selling price (if they already have one)
        
        Returns:
            Dictionary containing the calculated prices and breakdowns
        """
        # Calculate base price (materials + labor)
        labor_cost = hours_worked * labor_rate
        base_price = material_cost + labor_cost
        
        # Calculate factor adjustments based on uniqueness and demand
        uniqueness_adjustment = base_price * (uniqueness - 5) * self.uniqueness_weight
        demand_adjustment = base_price * (demand - 5) * self.demand_weight
        factor_adjustment = uniqueness_adjustment + demand_adjustment
        
        # Calculate adjusted price (total costs with adjustments)
        adjusted_price = base_price + factor_adjustment
        
        # If user provided a selling price, use it; otherwise calculate suggested prices
        if selling_price is not None and selling_price > 0:
            final_price = selling_price
        else:
            # Calculate suggested price based on typical multiplier
            final_price = adjusted_price * self.suggested_price_multiplier
            
        # Calculate profit information
        profit_amount = final_price - adjusted_price
        
        # Calculate profit margin percentage (as portion of final price)
        if final_price > 0:
            profit_margin_percentage = (profit_amount / final_price) * 100
        else:
            profit_margin_percentage = 0
            
        # Calculate markup percentage (as portion of costs)
        markup_percentage = (profit_amount / adjusted_price) * 100 if adjusted_price > 0 else 0
        
        # Calculate alternate pricing options
        economy_price = final_price * self.economy_modifier
        premium_price = final_price * self.premium_modifier
        
        # Round prices to 2 decimal places
        final_price = round(final_price, 2)
        economy_price = round(economy_price, 2)
        premium_price = round(premium_price, 2)
        profit_amount = round(profit_amount, 2)
        profit_margin_percentage = round(profit_margin_percentage, 2)
        markup_percentage = round(markup_percentage, 2)
        
        # Return comprehensive results
        return {
            "material_cost": material_cost,
            "labor_cost": labor_cost,
            "base_price": base_price,
            "uniqueness_adjustment": uniqueness_adjustment,
            "demand_adjustment": demand_adjustment,
            "factor_adjustment": factor_adjustment,
            "adjusted_price": adjusted_price,  # This is the total cost
            "profit_amount": profit_amount,
            "profit_margin_percentage": profit_margin_percentage,
            "markup_percentage": markup_percentage,
            "final_price": final_price,
            "economy_price": economy_price,
            "premium_price": premium_price,
            "selling_price": selling_price if selling_price is not None else 0
        }
    
    def update_weights(self, uniqueness_weight=None, demand_weight=None, 
                     economy_modifier=None, premium_modifier=None,
                     suggested_price_multiplier=None):
        """Update the weighting parameters used in calculations"""
        if uniqueness_weight is not None:
            self.uniqueness_weight = uniqueness_weight
        if demand_weight is not None:
            self.demand_weight = demand_weight
        if economy_modifier is not None:
            self.economy_modifier = economy_modifier
        if premium_modifier is not None:
            self.premium_modifier = premium_modifier
        if suggested_price_multiplier is not None:
            self.suggested_price_multiplier = suggested_price_multiplier 