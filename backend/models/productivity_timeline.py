"""
Productivity Timeline
Analyzes hive lifecycle and productivity trends over time
"""

class ProductivityTimeline:
    """Models hive lifecycle phases and productivity trends"""
    
    PHASES = {
        'Establishment': {'months': 2, 'productivity_factor': 0.4},
        'Build-up': {'months': 4, 'productivity_factor': 0.7},
        'Peak': {'months': 4, 'productivity_factor': 1.0},
        'Decline': {'months': 12, 'productivity_factor': 0.6},
        'Dormant': {'months': float('inf'), 'productivity_factor': 0.2}
    }
    
    def __init__(self, yield_prediction, hive_age_months=0):
        self.yield_prediction = yield_prediction
        self.hive_age_months = hive_age_months
    
    def get_current_phase(self):
        """Determine current lifecycle phase"""
        months_passed = self.hive_age_months
        current_phase = None
        
        for phase, data in self.PHASES.items():
            if months_passed <= data['months']:
                current_phase = phase
                break
            months_passed -= data['months']
        
        return current_phase or 'Dormant'
    
    def get_productivity_factor(self, month_offset=0):
        """Get productivity factor for a specific month"""
        target_month = self.hive_age_months + month_offset
        months_passed = 0
        
        for phase, data in self.PHASES.items():
            if months_passed + data['months'] >= target_month:
                return data['productivity_factor']
            months_passed += data['months']
        
        return 0.2  # Dormant phase
    
    def forecast_5_year_productivity(self):
        """Generate 5-year productivity forecast"""
        forecast = []
        base_honey = self.yield_prediction.predict_monthly_honey()
        
        for month in range(1, 61):  # 60 months = 5 years
            productivity_factor = self.get_productivity_factor(month)
            honey = base_honey * productivity_factor
            revenue = honey * 12  # Simple revenue multiplier
            
            forecast.append({
                'month': month,
                'year': (month - 1) // 12 + 1,
                'honey_kg': round(honey, 2),
                'phase': self.get_phase_for_month(month),
                'productivity_factor': productivity_factor,
                'estimated_revenue': round(revenue, 2)
            })
        
        return forecast
    
    def get_phase_for_month(self, month):
        """Get lifecycle phase for a specific month"""
        months_passed = 0
        for phase, data in self.PHASES.items():
            if months_passed + data['months'] >= month:
                return phase
            months_passed += data['months']
        return 'Dormant'
    
    def get_queen_replacement_recommendation(self):
        """Get queen replacement recommendation"""
        current_phase = self.get_current_phase()
        
        recommendations = {
            'Establishment': 'Monitor queen performance closely',
            'Build-up': 'Queen performing well, no action needed',
            'Peak': 'Consider new queen introduction for continued productivity',
            'Decline': 'Evaluate queen health, replacement may be needed',
            'Dormant': 'Plan for spring assessment and possible replacement'
        }
        
        return recommendations.get(current_phase, 'No recommendation')
    
    def get_optimal_harvest_period(self):
        """Identify optimal harvest periods"""
        forecast = self.forecast_5_year_productivity()
        peak_months = [m for m in forecast if m['productivity_factor'] >= 0.9]
        
        return {
            'peak_productivity_months': [m['month'] for m in peak_months],
            'optimal_harvest': 'Months 10-15 (Summer peak)',
            'avoid_harvest': 'Months 1-3 and 48-60 (Winter/Decline)'
        }
    
    def estimate_hive_lifespan(self):
        """Estimate productive lifespan of hive"""
        forecast = self.forecast_5_year_productivity()
        
        # Hive is considered unproductive if productivity < 0.3
        productive_months = sum(1 for m in forecast if m['productivity_factor'] >= 0.3)
        
        return {
            'productive_years': round(productive_months / 12, 1),
            'recommendation': 'Replace hive after 5-7 years for optimal productivity',
            'end_of_productivity': 'Approximately month 50-60'
        }
    
    def to_dict(self):
        """Return timeline summary"""
        return {
            'current_phase': self.get_current_phase(),
            'queen_recommendation': self.get_queen_replacement_recommendation(),
            'optimal_harvest': self.get_optimal_harvest_period(),
            'lifespan_estimate': self.estimate_hive_lifespan(),
            '5_year_forecast': self.forecast_5_year_productivity()
        }