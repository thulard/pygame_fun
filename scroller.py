# Import the pygame module
import pygame
import random

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Setup for sounds. Defaults are good.
pygame.mixer.init()

# Load and play background music
pygame.mixer.music.load('sounds/music.mp3')
pygame.mixer.music.play(loops=-1)

# Load all sound files
#move_up_sound = pygame.mixer.Sound("Rising_putter.ogg")
#move_down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound('sounds/birds.ogg')


# Initialize pygame
pygame.init()

# setup the gameover flag
gameover = 0

# Define a Player object by extending pygame.sprite.Sprite
# The surface drwan on the screen is now an attribute of 'player'
class Player(pygame.sprite.Sprite):
    '''
    Define the Player class
    '''
    def __init__(self):
        '''
        Setup the class (the chicken)
        '''
        super(Player, self).__init__()
        self.surf = pygame.image.load('pics/flying_bird.png').convert_alpha()
        self.surf.set_colorkey((139, 219, 129), RLEACCEL)
        self.rect = self.surf.get_rect(center=(80,SCREEN_HEIGHT /2))

    # Move the sprite based on user keypresses

    def hurt(self):
        '''
        Raise during collision with enemies
        '''
        self.surf = pygame.image.load('pics/hurt_bird.png').convert_alpha()
        self.surf.set_colorkey((139, 219, 129), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(SCREEN_WIDTH /2 , SCREEN_HEIGHT /2)
        )

    def update(self, pressed_keys): 
        '''
        Object Mouvements
        '''
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -30)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 30)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-30, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(30, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Define the enemy object by extending pygame.sprite.Sprite
# The surfact you draw on the screen is now an attribute of 'enemy'
class Enemy(pygame.sprite.Sprite):
    '''
    Define the Enemy class (the flies)
    '''
    def __init__(self):
        '''
        Setup the class
        '''
        super(Enemy, self).__init__()
        
        self.surf = pygame.image.load("pics/flying_fly.png").convert_alpha()
        self.surf.set_colorkey((184, 255, 249), RLEACCEL)
        #self.surf = pygame.Surface((20,10))
        #self.surf.fill((106, 84, 149))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen 
    def update(self):
        '''
        Object Mouvements
        '''
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Define the cloud object by extending pygame.sprite.Sprite
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        '''
        Setup the class
        '''
        super(Cloud, self).__init__()
        self.surf = pygame.image.load("pics/cloud.png").convert_alpha()
        self.surf.set_colorkey((184, 255, 249), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(1, 5)

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        '''
        Object Mouvements
        '''
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

def redraworder():
    '''
    Use to redraw all the object on the screen in the right order
    background, enemies, player, clouds
    '''
    # Fill the screen with light color
    screen.fill((184, 255, 249))

    # Draw enemies
    for entity in enemies:
        screen.blit(entity.surf, entity.rect)

    # Draw player
    screen.blit(player.surf, player.rect)

    # Draw cloud
    for entity in clouds:
        screen.blit(entity.surf, entity.rect)

    # Flip everything to the display
    pygame.display.flip()


# Setup the clock for a decent framerate
clock = pygame.time.Clock()

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Create a custom event for adding a new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000) # In ms
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 3000)

# Instatiate player
player = Player()

# Create groups to hold enemy sprites and all sprites
# - enemies is used for collision detection and position updates
# - clouds is used for background clouds
# - all_sprites is used for rendering
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

# Variable to keep the main loop running
running = True

# Main loop
while running:
    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

        # Add a new enemy?
        elif event.type == ADDENEMY:
            # Create a new enemy and add it to sprite groups
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # Add a new cloud
        elif event.type == ADDCLOUD:
            # Create the new cloud and add it to sprite groups
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()
    
    # Update the player sprite based on user keypresses
    player.update(pressed_keys)
    
    # Update the enemy position
    enemies.update()
    clouds.update()

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, enemies) and gameover == 0:
        # If so, change player to gameover state, fade the music and play the colission_sound
        player.hurt()
        pygame.mixer.music.fadeout(3000)
        collision_sound.play()
        redraworder()

        gameover = 1

    redraworder()  

    # Ensure program maintains a rate of 30 frames per second
    clock.tick(30)

