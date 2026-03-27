"""
Revenue Engine
Calculates profit and ROI based on production and market prices
"""

class RevenueEngine:
    """Calculates revenue and profitability"""
    
    # Market prices (default values)
    HONEY_PRICE_PER_KG = 12.0  # USD
    WAX_PRICE_PER_KG = 15.0    # USD
    POLLINATION_VALUE_PER_HIVE = 100.0  # USD per season
    ANNUAL_HIVE_COST = 150.0   # USD
    
    def __init__(self, yield_prediction, market_config=None):
        self.yield_prediction = yield_prediction
        if market_config:
            self.HONEY_PRICE_PER_KG = market_config.get('honey_price', self.HONEY_PRICE_PER_KG)
            self.WAX_PRICE_PER_KG = market_config.get('wax_price', self.WAX_PRICE_PER_KG)
            self.POLLINATION_VALUE_PER_HIVE = market_config.get('pollination_value', self.POLLINATION_VALUE_PER_HIVE)
            self.ANNUAL_HIVE_COST = market_config.get('annual_cost', self.ANNUAL_HIVE_COST)
    
    def calculate_monthly_revenue(self):
        """Calculate monthly revenue from honey and wax"""
        honey_kg = self.yield_prediction.predict_monthly_honey()
        wax_kg = self.yield_prediction.predict_beeswax()
        
        honey_revenue = honey_kg * self.HONEY_PRICE_PER_KG
        wax_revenue = wax_kg * self.WAX_PRICE_PER_KG
        pollination_monthly = self.POLLINATION_VALUE_PER_HIVE / 12
        
        return round(honey_revenue + wax_revenue + pollination_monthly, 2)
    
    def calculate_yearly_revenue(self):
        """Calculate yearly revenue"""
        monthly_revenue = self.calculate_monthly_revenue()
        return round(monthly_revenue * 12, 2)
    
    def calculate_monthly_profit(self):
        """Calculate monthly profit (revenue - costs)"""
        monthly_revenue = self.calculate_monthly_revenue()
        monthly_cost = self.ANNUAL_HIVE_COST / 12
        
        return round(monthly_revenue - monthly_cost, 2)
    
    def calculate_yearly_profit(self):
        """Calculate yearly profit"""
        yearly_revenue = self.calculate_yearly_revenue()
        return round(yearly_revenue - self.ANNUAL_HIVE_COST, 2)
    
    def calculate_roi(self, initial_investment=500):
        """Calculate ROI percentage"""
        yearly_profit = self.calculate_yearly_profit()
        roi = (yearly_profit / initial_investment) * 100
        return round(roi, 2)
    
    def breakeven_months(self, initial_investment=500):
        """Calculate months to breakeven"""
        monthly_profit = self.calculate_monthly_profit()
        if monthly_profit <= 0:
            return None
        
        months = initial_investment / monthly_profit
        return round(months, 1)
    
    def forecast_revenue(self, months=12):
        """Generate revenue forecast"""
        forecast = self.yield_prediction.forecast_production(months)
        revenue_forecast = []
        
        for entry in forecast:
            honey_rev = entry['honey_kg'] * self.HONEY_PRICE_PER_KG
            wax_rev = entry['wax_kg'] * self.WAX_PRICE_PER_KG
            pollination_monthly = self.POLLINATION_VALUE_PER_HIVE / 12
            monthly_cost = self.ANNUAL_HIVE_COST / 12
            
            total_revenue = honey_rev + wax_rev + pollination_monthly
            profit = total_revenue - monthly_cost
            
            revenue_forecast.append({
                'month': entry['month'],
                'honey_revenue': round(honey_rev, 2),
                'wax_revenue': round(wax_rev, 2),
                'pollination_revenue': round(pollination_monthly, 2),
                'total_revenue': round(total_revenue, 2),
                'costs': round(monthly_cost, 2),
                'profit': round(profit, 2)
            })
        
        return revenue_forecast
    
    def to_dict(self):
        """Return revenue summary"""
        return {
            'monthly_revenue': self.calculate_monthly_revenue(),
            'yearly_revenue': self.calculate_yearly_revenue(),
            'monthly_profit': self.calculate_monthly_profit(),
            'yearly_profit': self.calculate_yearly_profit(),
            'roi_percent': self.calculate_roi(),
            'breakeven_months': self.breakeven_months()
        }