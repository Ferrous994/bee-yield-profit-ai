"""
Hive Model Module
Manages biological and environmental parameters of bee hives
"""

class Hive:
    """Represents a bee hive with biological and environmental parameters"""
    
    def __init__(self, hive_id, colony_size, queen_age, hive_strength, 
                 season, weather_conditions, flower_availability, location, 
                 temperature=20, rainfall=50):
        self.hive_id = hive_id
        self.colony_size = colony_size
        self.queen_age = queen_age
        self.hive_strength = hive_strength
        self.season = season
        self.weather_conditions = weather_conditions
        self.flower_availability = flower_availability
        self.location = location
        self.temperature = temperature
        self.rainfall = rainfall
    
    def get_foraging_bees(self):
        """Calculate number of foraging bees (30-40% of colony)"""
        foraging_rate = 0.35
        return int(self.colony_size * foraging_rate)
    
    def get_queen_efficiency(self):
        """Calculate queen efficiency based on age"""
        if self.queen_age <= 1:
            return 0.7
        elif self.queen_age <= 3:
            return 1.0
        elif self.queen_age <= 4:
            return 0.8
        else:
            return 0.5
    
    def get_season_factor(self):
        """Get productivity factor based on season"""
        season_factors = {
            'spring': 0.8, 'summer': 1.0, 'fall': 0.6, 'winter': 0.2
        }
        return season_factors.get(self.season.lower(), 0.5)
    
    def get_weather_factor(self):
        """Get weather impact factor"""
        weather_factors = {
            'sunny': 1.0, 'cloudy': 0.7, 'rainy': 0.3, 'stormy': 0.1
        }
        return weather_factors.get(self.weather_conditions.lower(), 0.5)
    
    def get_flower_availability_factor(self):
        """Get nectar availability factor"""
        flower_factors = {'low': 0.5, 'medium': 0.8, 'high': 1.0}
        return flower_factors.get(self.flower_availability.lower(), 0.5)
    
    def get_hive_strength_factor(self):
        """Get efficiency factor based on hive strength (1-10)"""
        return self.hive_strength / 10.0
    
    def get_total_efficiency(self):
        """Calculate total efficiency multiplier"""
        return (self.get_queen_efficiency() * self.get_season_factor() * 
                self.get_weather_factor() * self.get_flower_availability_factor() * 
                self.get_hive_strength_factor())
    
    def to_dict(self):
        """Convert hive to dictionary"""
        return {
            'hive_id': self.hive_id,
            'colony_size': self.colony_size,
            'queen_age': self.queen_age,
            'hive_strength': self.hive_strength,
            'season': self.season,
            'foraging_bees': self.get_foraging_bees(),
            'total_efficiency': self.get_total_efficiency()
        }