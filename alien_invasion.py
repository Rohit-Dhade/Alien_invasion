import sys
import time
import pygame
from scoreboard import Scoreboard
from button import Button
from pygame.sprite import Group
from settings import settings
from ship import Ship
#from alien import Alien
from game_stats import Gamestats
import game_function as gf

def run_game():
    """Initialize game and create a screen object."""
    
    pygame.init()
    ai_settings = settings()
    screen = pygame.display.set_mode((ai_settings.screen_width , ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")
    
    # Making a ship. a group of bullets , and a group of aliens.
    ship = Ship(ai_settings , screen)
    bullets = pygame.sprite.Group()
    aliens = pygame.sprite.Group()
    play_button = Button(ai_settings , screen , "PLAY")
    stats = Gamestats(ai_settings)
    sb = Scoreboard(ai_settings , screen , stats)
    clock = pygame.time.Clock()
    gf.create_fleet(ai_settings , screen , ship , aliens)
    
    while True:
        gf.check_events(ai_settings , screen ,stats ,sb, play_button , ship ,aliens , bullets)
        
        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings , screen ,stats , sb, ship , aliens , bullets)
            gf.update_aliens(ai_settings, stats, screen , sb  , ship  , aliens, bullets)
            
        gf.update_screen(ai_settings , screen ,stats, sb, ship , aliens , bullets , play_button)
        clock.tick(35)
run_game()