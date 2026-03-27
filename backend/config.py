"""
Configuration Module
Contains market prices, costs, and system settings
"""

import json

class Config:
    """System configuration"""
    
    # Market Prices
    HONEY_PRICE_PER_KG = 12.0  # USD
    WAX_PRICE_PER_KG = 15.0    # USD
    POLLINATION_VALUE = 100.0  # USD per hive per season
    
    # Costs
    ANNUAL_HIVE_MAINTENANCE = 150.0  # USD
    INITIAL_SETUP_COST = 500.0       # USD
    
    # Hive Parameters
    MIN_COLONY_SIZE = 10000
    MAX_COLONY_SIZE = 60000
    OPTIMAL_COLONY_SIZE = 40000
    
    # Efficiency Factors
    FORAGING_BEE_PERCENTAGE = 0.35
    BEESWAX_PERCENTAGE = 0.015
    
    @staticmethod
    def load_market_prices():
        """Load market prices from config"""
        return {
            'honey_price': Config.HONEY_PRICE_PER_KG,
            'wax_price': Config.WAX_PRICE_PER_KG,
            'pollination_value': Config.POLLINATION_VALUE,
            'annual_cost': Config.ANNUAL_HIVE_MAINTENANCE
        }
    
    @staticmethod
    def to_dict():
        """Convert config to dictionary"""
        return {
            'honey_price': Config.HONEY_PRICE_PER_KG,
            'wax_price': Config.WAX_PRICE_PER_KG,
            'pollination_value': Config.POLLINATION_VALUE,
            'annual_maintenance': Config.ANNUAL_HIVE_MAINTENANCE,
            'initial_setup': Config.INITIAL_SETUP_COST
        }