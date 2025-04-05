class settings():
    '''A class to store all settings for alien invasion.'''
    
    def __init__(self):
        """Initialize the screen settings."""
        
        # screen settings.
        
        self.screen_width = 800
        self.screen_height = 750
        self.bg_color = (0 , 0 , 0)
        self.ship_limit = 3
        
        # bullet settings.
        
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255,255,255)
        self.bullets_allowed = 100
        
        # alien settings.
        
        self.speedup_scale = 1.1
        self.fleet_drop_speed = 0.5
        self.score_scale = 1.5
        
        self.initialize_dynamic_settings()
        
    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.bullet_speed_factor = 50.5
        self.ship_speed_factor = 10.5
        self.alien_speed_factor = 1
        self.fleet_direction = 1
        self.alien_points = 50
        
    def increase_speed(self):
        """Increase speed settings."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)  
            
            