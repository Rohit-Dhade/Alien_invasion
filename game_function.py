import sys
import pygame
from pygame.sprite import Sprite
from bullet import Bullet
from alien import Alien
from time import sleep

def check_keydown_events(event , ai_settings , screen , ship , bullets):
    '''respond to keypresses.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings , screen ,ship , bullets)
    elif event.key == pygame.K_q:
        sys.exit()
            
def fire_bullets(ai_settings , screen , ship , bullets):
    if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen , ship)
            bullets.add(new_bullet)
        
def check_keyup_events(event , ship):
    '''Respond to key releases.'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False
    
def check_events(ai_settings , screen ,stats ,sb, play_button , ship ,aliens, bullets):
    '''Responds to keypresses and mouse events.'''
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event , ai_settings , screen , ship , bullets)
                    
            elif event.type == pygame.KEYUP:
                check_keyup_events(event , ship)
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x , mouse_y = pygame.mouse.get_pos()
                check_play_button(ai_settings , screen ,stats ,sb, play_button ,ship, aliens ,bullets, mouse_x , mouse_y)
                
def check_play_button(ai_settings , screen ,stats ,sb, play_button ,ship , aliens, bullets, mouse_x , mouse_y):
    """Start a new game when the player clicks Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x , mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        if play_button.rect.collidepoint(mouse_x , mouse_y):
            pygame.mouse.set_visible(False)
            stats.reset_stats()
            stats.game_active = True
            
            # reset the scoreboard images.
            sb.prep_score()
            sb.prep_high_score()
            sb.prep_level()
            #sb.prep_ships()
            
            aliens.empty()
            bullets.empty()
            create_fleet(ai_settings , screen , ship , aliens)
            ship.center_ship()
                
def update_screen(ai_settings , screen ,stats, sb, ship ,aliens , bullets , play_button):
    '''Update images on the screen and flip to the new screen.'''
    screen.fill(ai_settings.bg_color)
    sb.show_score()
    
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()
    
def update_bullets(ai_settings , screen ,stats , sb, ship , aliens , bullets):
    '''Update position of bullets and get rid of old bullets.'''
    
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
            
    check_bullet_alien_collisions(ai_settings , screen ,stats ,sb, ship ,aliens , bullets)
    
def check_bullet_alien_collisions(ai_settings ,screen ,stats,sb, ship , aliens , bullets):
    collisions = pygame.sprite.groupcollide(bullets ,aliens ,True , True)
    
    if collisions:
        for alien in collisions.values():
            stats.score += ai_settings.alien_points 
            sb.prep_score()
        check_high_score(stats , sb)
        
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        
        # increased Level.
        stats.level += 1
        sb.prep_level()
        
        create_fleet(ai_settings , screen , ship , aliens)
            
def get_number_alien_x(ai_settings , alien_width):
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_alien_x = int(available_space_x / (2 * alien_width))
    return number_alien_x

def get_number_rows(ai_settings , ship_height , alien_height):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y)/(2*alien_height)
    return number_rows

def create_alien(ai_settings , screen , aliens , alien_number , row_number):
    alien = Alien(ai_settings , screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)
    
def create_fleet(ai_settings , screen , ship , aliens):
    '''Create a full fleet of aliens.'''
    alien = Alien(ai_settings , screen)
    number_alien_x = get_number_alien_x(ai_settings , alien.rect.width)
    number_rows = get_number_rows(ai_settings , ship.rect.height , alien.rect.height)
    
    for row_number in range(int(number_rows)):
        for alien_number in range(number_alien_x):
            create_alien(ai_settings , screen , aliens ,alien_number , row_number)
            
            
def check_fleet_edges(ai_settings ,aliens):
    for alien in aliens.sprites():
        change_fleet_direction(ai_settings , aliens)
        break
    
def change_fleet_direction(ai_settings  , aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1
    
def ship_hit(ai_settings , stats , screen ,sb, ship , aliens , bullets):
    
    if stats.ships_left > 0:
        stats.ships_left -= 1
        # sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings , screen , ship ,aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)
    
def check_aliens_bottom(ai_settings , stats , screen ,sb, ship , aliens , bullets):
    '''Check if any aliens have reached the bottom of the screen.'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings , stats , screen ,sb, ship , aliens, bullets)
            break
            
def update_aliens(ai_settings ,stats , screen ,sb, ship , aliens , bullets):
    check_fleet_edges(ai_settings , aliens)
    aliens.update()
    
    
    if pygame.sprite.spritecollideany(ship, aliens):
            ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottom(ai_settings ,stats , screen ,sb,ship , aliens , bullets)

def check_high_score(stats ,sb):
    """Check to see if there's a new high score."""
    
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()