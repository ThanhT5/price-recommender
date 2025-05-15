# Handmade Goods Pricing Assistant

A Python-based application designed to help small-scale artisans and handmade goods sellers determine optimal pricing for their products. The system uses a heuristic-based approach that considers multiple key factors:

- Material costs
- Time investment (labor hours)
- Hourly labor rate
- Product uniqueness 
- Market demand
- Target profit margins

## Purpose and Target Users

Pricing handmade goods is a common challenge for artisans and small business owners. The application addresses the following challenges:

1. **Balancing cost recovery with market competitiveness**: Ensuring prices cover costs while remaining attractive to customers
2. **Accounting for intangible factors**: Incorporating uniqueness and demand into pricing decisions
3. **Providing pricing alternatives**: Offering economy, standard, and premium pricing options
4. **Visualizing price breakdown**: Helping sellers understand how different factors contribute to final prices
5. **Enabling what-if analysis**: Allowing users to see how changes in inputs affect the final price

## Features
- Calculate recommended prices based on multiple factors
- Visualize price breakdowns
- Compare different pricing strategies (economy, standard, premium)
- Save and load product templates
- Sample scenarios for different product types


## Pricing Formula

The application uses a multi-step formula to calculate prices:

1. **Base Price Calculation**:
   ```
   base_price = material_cost + (hours_worked * labor_rate)
   ```

2. **Factor Adjustments**:
   ```
   uniqueness_adjustment = base_price * (uniqueness - 5) * uniqueness_weight
   demand_adjustment = base_price * (demand - 5) * demand_weight
   adjusted_price = base_price + uniqueness_adjustment + demand_adjustment
   ```

3. **Profit Margin Application**:
   ```
   final_price = adjusted_price / (1 - profit_margin)
   ```

4. **Alternative Pricing Options**:
   ```
   economy_price = final_price * economy_modifier (default: 0.85)
   premium_price = final_price * premium_modifier (default: 1.25)
   ```

## Installation
1. Clone this repository
2. Install the required dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   This key is required for the AI assistant functionality.
4. Run the application: `python src/main.py` or `python run.py`

## Basic Usage

1. Enter your product's details in the input fields:
   - Material Cost: The total cost of materials used
   - Hours Worked: The time spent creating the product
   - Labor Rate: Your desired hourly rate
   - Uniqueness Rating: How unique your product is (1-10)
   - Demand Rating: Market demand for your product (1-10)
   - Target Profit: Your desired profit margin percentage

2. Click "Calculate Price" to see the recommended price.

3. The results panel will show:
   - The recommended price
   - A breakdown of price components
   - Alternative pricing options (economy and premium)

### Sample Scenarios

The application includes three preset scenarios to help you get started:

- **Simple Jewelry**: A basic item with moderate uniqueness and high demand.
- **Complex Art**: A detailed item with high uniqueness but moderate demand.
- **Batch Item**: A simpler item produced in multiples with lower uniqueness but higher demand.

## Future Enhancements

Potential future enhancements include:

- Integration with cost tracking for materials
- Historical pricing tracking
- Market comparison with similar products
- Batch processing for multiple similar items
- Export functionality for reports and pricing sheets
- Template management for different product categories
