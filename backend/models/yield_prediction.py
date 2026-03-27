"""
Yield Prediction Engine
Estimates honey and beeswax production based on hive parameters
"""

class YieldPrediction:
    """Predicts honey and beeswax yield"""
    
    def __init__(self, hive):
        self.hive = hive
    
    def predict_monthly_honey(self):
        """
        Calculate monthly honey production
        Honey = Foraging Bees × Nectar Availability × Efficiency
        """
        foraging_bees = self.hive.get_foraging_bees()
        nectar_per_bee = 0.5  # kg per bee per month (base rate)
        efficiency = self.hive.get_total_efficiency()
        
        honey = foraging_bees * nectar_per_bee * efficiency / 1000
        return round(honey, 2)
    
    def predict_yearly_honey(self):
        """Calculate yearly honey production"""
        monthly_honey = self.predict_monthly_honey()
        return round(monthly_honey * 12, 2)
    
    def predict_beeswax(self):
        """
        Calculate beeswax production (1-2% of honey)
        Using 1.5% as average
        """
        honey = self.predict_monthly_honey()
        wax = honey * 0.015
        return round(wax, 2)
    
    def forecast_production(self, months=12):
        """Generate production forecast for specified months"""
        forecast = []
        monthly_honey = self.predict_monthly_honey()
        
        for month in range(1, months + 1):
            # Adjust for seasonal variations
            season_multiplier = self._get_seasonal_multiplier(month)
            honey_this_month = monthly_honey * season_multiplier
            wax_this_month = honey_this_month * 0.015
            
            forecast.append({
                'month': month,
                'honey_kg': round(honey_this_month, 2),
                'wax_kg': round(wax_this_month, 2),
                'total_kg': round(honey_this_month + wax_this_month, 2)
            })
        
        return forecast
    
    def _get_seasonal_multiplier(self, month):
        """Get seasonal production multiplier based on month"""
        # Month 1=Jan, 12=Dec
        if month in [3, 4, 5]:  # Spring
            return 0.8
        elif month in [6, 7, 8]:  # Summer
            return 1.0
        elif month in [9, 10]:  # Fall
            return 0.6
        else:  # Winter
            return 0.2
    
    def to_dict(self):
        """Return prediction summary"""
        return {
            'monthly_honey_kg': self.predict_monthly_honey(),
            'yearly_honey_kg': self.predict_yearly_honey(),
            'monthly_beeswax_kg': self.predict_beeswax(),
            'forecast_12_months': self.forecast_production(12)
        }