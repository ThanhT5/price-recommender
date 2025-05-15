"""
Validation utilities for the Handmade Goods Pricing Assistant
"""

def validate_numeric_input(value, min_value=None, max_value=None, field_name="Value"):
    """
    Validate that a value is numeric and within the specified range
    
    Args:
        value: The value to validate
        min_value: The minimum allowed value (optional)
        max_value: The maximum allowed value (optional)
        field_name: The name of the field for error messages
    
    Returns:
        The validated value as a float
    
    Raises:
        ValueError: If the value is not valid
    """
    try:
        # Try to convert to float
        float_value = float(value)
        
        # Check bounds if provided
        if min_value is not None and float_value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}")
            
        if max_value is not None and float_value > max_value:
            raise ValueError(f"{field_name} cannot exceed {max_value}")
            
        return float_value
        
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid number")

def validate_integer_input(value, min_value=None, max_value=None, field_name="Value"):
    """
    Validate that a value is an integer and within the specified range
    
    Args:
        value: The value to validate
        min_value: The minimum allowed value (optional)
        max_value: The maximum allowed value (optional)
        field_name: The name of the field for error messages
    
    Returns:
        The validated value as an integer
    
    Raises:
        ValueError: If the value is not valid
    """
    try:
        # Try to convert to int
        int_value = int(value)
        
        # Check bounds if provided
        if min_value is not None and int_value < min_value:
            raise ValueError(f"{field_name} must be at least {min_value}")
            
        if max_value is not None and int_value > max_value:
            raise ValueError(f"{field_name} cannot exceed {max_value}")
            
        return int_value
        
    except (ValueError, TypeError):
        raise ValueError(f"{field_name} must be a valid integer")

def validate_pricing_inputs(material_cost, hours_worked, labor_rate, 
                          uniqueness, demand, selling_price=None):
    """
    Validate all pricing inputs at once
    
    Args:
        material_cost: Cost of materials
        hours_worked: Number of hours worked
        labor_rate: Hourly labor rate
        uniqueness: Uniqueness rating (1-10)
        demand: Demand rating (1-10)
        selling_price: Optional selling price (can be None or 0 for automatic calculation)
    
    Returns:
        Dictionary with validated values
    
    Raises:
        ValueError: If any input is invalid
    """
    # Validate each input
    validated_material_cost = validate_numeric_input(
        material_cost, min_value=0, field_name="Material cost")
    
    validated_hours_worked = validate_numeric_input(
        hours_worked, min_value=0, field_name="Hours worked")
    
    validated_labor_rate = validate_numeric_input(
        labor_rate, min_value=0, field_name="Labor rate")
    
    validated_uniqueness = validate_integer_input(
        uniqueness, min_value=1, max_value=10, field_name="Uniqueness rating")
    
    validated_demand = validate_integer_input(
        demand, min_value=1, max_value=10, field_name="Demand rating")
    
    # Selling price is optional but must be non-negative if provided
    validated_selling_price = None
    if selling_price is not None:
        validated_selling_price = validate_numeric_input(
            selling_price, min_value=0, field_name="Selling price")
    
    # Return all validated values
    result = {
        "material_cost": validated_material_cost,
        "hours_worked": validated_hours_worked,
        "labor_rate": validated_labor_rate,
        "uniqueness": validated_uniqueness,
        "demand": validated_demand
    }
    
    # Only include selling_price if it's provided and valid
    if validated_selling_price is not None and validated_selling_price > 0:
        result["selling_price"] = validated_selling_price
        
    return result 