from pygame.sprite import Sprite
import pygame

class Ship(pygame.sprite.Sprite):
    def __init__(self, ai_settings, screen):
        '''Initialize the ship and set its starting position.'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and resize it
        self.image = pygame.image.load('images/ship.bmp')
        self.width , self.height = 60 , 60
        self.resized_image = pygame.transform.scale(self.image, (self.width , self.height))
        self.rect = self.resized_image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start the ship at the bottom center of the screen
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's center
        self.center = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        '''Update the ship's position based on the movement flags.'''
        # Update the ship's center value, not the rect directly
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor

        # Update rect object from self.center
        self.rect.centerx = self.center

    def blitme(self):
        '''Draw the ship at its current location.'''
        self.screen.blit(self.resized_image, self.rect)
        
    def center_ship(self):
        """Center the ship on the screen."""
        self.center = self.screen_rect.centerx
