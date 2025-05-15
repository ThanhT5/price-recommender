"""
Pydantic models for AI recommendations and structured outputs.
"""

from pydantic import BaseModel, Field, field_validator, confloat


class PricingRecommendation(BaseModel):
    """
    Structured output model for pricing recommendations.
    This ensures the AI provides consistent, parseable output format.
    """
    material_cost: float = Field(
        description="Total cost of materials in dollars",
        ge=0  # greater than or equal to 0
    )
    
    hours_worked: float = Field(
        description="Number of hours spent creating the product",
        ge=0
    )
    
    labor_rate: float = Field(
        description="Suggested hourly labor rate in dollars",
        ge=0
    )
    
    uniqueness: confloat(ge=1, le=10) = Field(
        description="Rating of product uniqueness on scale of 1-10 (with 1 being common and 10 being one-of-a-kind)"
    )
    
    demand: confloat(ge=1, le=10) = Field(
        description="Rating of market demand on scale of 1-10 (with 1 being low demand and 10 being high demand)"
    )
    
    selling_price: float = Field(
        description="Optional recommended selling price in dollars (if blank, will be calculated automatically)",
        ge=0, default=0  # optional field, default to 0 (automatic calculation)
    )
    
    explanation: str = Field(
        description="Explanation for the recommendations"
    )
    
    @field_validator('uniqueness', 'demand')
    @classmethod
    def round_to_one_decimal(cls, v: float) -> float:
        """Round uniqueness and demand to 1 decimal place"""
        return round(v, 1)


class ChatMessage(BaseModel):
    """Model for chat message objects"""
    role: str
    content: str 