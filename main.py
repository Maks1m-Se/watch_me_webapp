# /// script
# dependencies = [
#  "pygame-ce",
#  "pygame",
#  "sys",
#  "asyncio",
#  "numpy",
#  "math",
#  "time",
#  "random",
# ]
# ///

import pygame
import random
import time
import math 
import numpy as np
import os, sys
from button import Button
import asyncio
import threading

# Initialize pygame modules
pygame.init()
pygame.font.init()
pygame.mixer.init()


# Set up constants
WIDTH, HEIGHT = 1000, 800
MAX_DISTANC = WIDTH
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)


# Create the game window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("WATCH ME")




# Game elements and attributes
BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 30
MONSTER_VEL = 1
PLAYER_VEL = 3
PLAYER_DIFF_VEL = 3
N_OBSTICLES = 30
DIFFICULTY = 'MILD'
MONSTER_WIDTH, MONSTER_HEIGHT = 45, 45
PLAYER_WIDTH, PLAYER_HEIGHT = 20, 20
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 50, 50
LIGHT_SIZE =  HEIGHT * 6
obstacle_list = []
draw_blood = False
stop_mixer = False
blood_list = []
blood_stain_list = []
keep_playing = True
loading_finished = False
loading_progress = 0
loading_bar_width = 8






# Resize button images
play_image = pygame.transform.scale(pygame.image.load("assets/images/Play Rect.png"), (150, 40))



BG = pygame.image.load("assets/images/menu.png")
bg_width = BG.get_width()
bg_height = BG.get_height()
# Calculate the top-left position to center the image
bg_x = (WIDTH - bg_width) // 2
bg_y = (HEIGHT - bg_height) // 2

LOADING_BG = pygame.transform.scale(pygame.image.load("assets\images\Loading_Bar_Background.png"), (WIDTH*.3, HEIGHT*.03))
LOADING_BG_RECT = LOADING_BG.get_rect(center=(WIDTH//2, HEIGHT*.7))
LOADING_BAR = pygame.image.load("assets\images\Loading_Bar.png")
LOADING_BAR = pygame.transform.scale(pygame.image.load("assets\images\Loading_Bar.png"), (WIDTH*.01, HEIGHT*.03))
position_x_loading_bar = WIDTH//2 - LOADING_BG.get_width()//2
LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft=(position_x_loading_bar, HEIGHT*.7))
BG_opt = pygame.image.load("assets/images/Options.png")
WIN.blit(BG, (bg_x, bg_y))
#WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
pygame.display.update()



PLAYER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'player.png')
    )
PLAYER = pygame.transform.rotate(
    pygame.transform.scale(PLAYER_IMAGE, (PLAYER_WIDTH, PLAYER_HEIGHT)), 0
    )

MONSTER_IMAGE = pygame.image.load(
    os.path.join('assets', 'images', 'monster-removebg-preview.png')
    )
MONSTER = pygame.transform.rotate(
    pygame.transform.scale(MONSTER_IMAGE, (MONSTER_WIDTH, MONSTER_HEIGHT)), 0
    )

CONCRETE = pygame.transform.scale(
    pygame.image.load(os.path.join('assets', 'images', 'concrete.jpg')),
    (WIDTH, HEIGHT)
    )



# Load sounds
possessed_laugh_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'collide', 'possessed-laugh-94851.ogg'))
scream_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', 'scream.ogg'))
hit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', 'piano-shock-impact-99701.ogg'))
jumpscare_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', 'jumpscare-203379.ogg'))
slit_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '104045__willhiccups__knife-slits-1.ogg'))
monster_eating_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '472598__audiopapkin__monster-sound-effects-14.ogg'))
eating_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'kill', '712065__audiopapkin__monster-eating.ogg'))
breathing_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'breathing.ogg'))
start_monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'monster_sounds', 'deep-monster-growl-86780.ogg'))
switch_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'switch2.ogg'))
click_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'click.ogg'))

random_menu_sound = random.choice(os.listdir(os.path.join('assets', 'sounds','music')))
menu_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', random_menu_sound))
menu_sound.play()

def draw_loading_bar(i):
    global LOADING_BAR, LOADING_BAR_RECT, LOADING_BG, LOADING_BG_RECT, loading_bar_width 
    #loading progress bar
    loading_bar_width = int((i / 1625) * WIDTH*.3)
    print('loading_bar_width: ', loading_bar_width)
    LOADING_BAR = pygame.transform.scale(LOADING_BAR, (1+loading_bar_width, HEIGHT*.03))
    LOADING_BAR_RECT = LOADING_BAR.get_rect(midleft=(position_x_loading_bar, HEIGHT*.7))
    WIN.blit(LOADING_BG, LOADING_BG_RECT)
    WIN.blit(LOADING_BAR, LOADING_BAR_RECT)
    pygame.display.update()
    

threading.Thread(target=draw_loading_bar).start()

#LOAD GIRL IMAGES #Long process
BG_girl_images = []
path_BG_girl_images = r'assets\images\BG_animation\extraction_20240730_153740'
# Load the images into the list
for i in range(1625):
    # Construct the filename for each image
    filename = f"frame_{i:04d}.png"  # Ensure filenames are zero-padded
    print(filename)
    image_path = f"{path_BG_girl_images}/{filename}"
    # Load the image
    try:
        BG_girl_image = pygame.image.load(image_path)
        BG_girl_images.append(BG_girl_image)
        print(f"Loaded image {image_path}")
    except pygame.error as e:
        print(f"Error loading image {image_path}: {e}")
    
    draw_loading_bar(i)    

    #closing option
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

switch_sound.play()


# Function Press-Start-2P in the desired size
def get_font(size): 
    return pygame.font.Font("assets/NineteenNinetySeven-11XB.ttf", size)


# Function to create obstacles
def generate_obstacles(num_obstacles, player, monster):
    global obstacle_list
    for _ in range(num_obstacles):
        while True:
            OBSTACLE_WIDTH, OBSTACLE_HEIGHT = random.randint(20, 150), random.randint(10, 80)
            x = random.randint(0, WIDTH - OBSTACLE_WIDTH)
            y = random.randint(HEIGHT * .15, HEIGHT * .85 - OBSTACLE_HEIGHT)
            new_obstacle = pygame.Rect(x, y, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            if not new_obstacle.colliderect(player) and not new_obstacle.colliderect(monster):
                obstacle_list.append(new_obstacle)
                break


# Function to draw game window
def draw_window(monster, player, light):
    WIN.blit(CONCRETE, (0, 0))
    WIN.blit(MONSTER, (monster.x, monster.y))
    
    WIN.blit(light, (player.x - LIGHT_SIZE/2, player.y - LIGHT_SIZE/2))

     # Draw obstacles
    for obstacle in obstacle_list:
        pygame.draw.rect(WIN, BLACK, obstacle)

    

    ####### TEST Darkness ######
    
    # mouse position
    mouse_pos = pygame.mouse.get_pos()
    print('mouse_pos', mouse_pos)

    ## lines light cone
    light_angle = 45
    beta_l = - light_angle/2
    beta_r = light_angle/2

    
    v_lamp_pos = np.array([player.x + PLAYER_WIDTH/2, player.y])
    v_middle = np.array([v_lamp_pos[0]-mouse_pos[0], v_lamp_pos[1]-mouse_pos[1]])


    # Convert beta to radians
    beta_rad_l = math.radians(beta_l)
    beta_rad_r = math.radians(beta_r)

    # Calculate the rotated vector v2 using the rotation matrix
    rotation_matrix_l = np.array([[math.cos(beta_rad_l), -math.sin(beta_rad_l)],
                                  [math.sin(beta_rad_l), math.cos(beta_rad_l)]])
    
    rotation_matrix_r = np.array([[math.cos(beta_rad_r), -math.sin(beta_rad_r)],
                                  [math.sin(beta_rad_r), math.cos(beta_rad_r)]])


    v_left = np.dot(rotation_matrix_l, v_middle)
    v_right = np.dot(rotation_matrix_r, v_middle)

    
    #normalize and elongate the vectors
    v_left_norm = np.linalg.norm(v_left)
    v_right_norm = np.linalg.norm(v_right)
    len_factor = 100
    v_left_len = v_left / v_left_norm * len_factor
    v_right_len = v_right / v_right_norm * len_factor
    # use normalized and elongated vectors


    print('v_middle:', v_middle)
    print('v_left:', v_left)
    print('v_right:', v_right)
    print('v_left_len:', v_left_len)
    print('v_right_len:', v_right_len)


    light_line_middle, light_line_left, light_line_right = v_middle*1+v_lamp_pos, v_left_len*100+v_lamp_pos, v_right_len*100+v_lamp_pos

    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, light_line_middle, width=3)
    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, light_line_left, width=10) # for testing red color
    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, light_line_right, width=10) # for testing blue color

    reflextion_middle = light_line_middle-2*(light_line_middle-v_lamp_pos)
    reflextion_right = light_line_right-2*(light_line_right-v_lamp_pos)
    reflextion_left = light_line_left-2*(light_line_left-v_lamp_pos)

    #pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, reflextion_middle, width=2) guide line mouse
    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, reflextion_left, width=7) # for testing red color
    pygame.draw.line(WIN, (0, 0, 0), v_lamp_pos, reflextion_right, width=7) # for testing blue color

    vector_darkness = [light_line_left,
                       light_line_right,
                       reflextion_left,
                       v_lamp_pos,
                       reflextion_right
                       ]
    

    pygame.draw.polygon(WIN, (0, 0, 0, 100), vector_darkness)
    # mask = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA, ) Trasparency
    # mask.set_alpha(200)

    ###### END TEST Darkness ######

    
    WIN.blit(PLAYER, (player.x, player.y))

    

    pygame.display.update()


# Function drawing blood
def drawing_blood(player, light):
    global draw_blood, LIGHT_SIZE
    if draw_blood:

        WIN.blit(CONCRETE, (0, 0))

        BLOOD_COLOR = (random.randint(90,255),
                       random.randint(0, 5),
                       random.randint(0, 5))
        
        blood_size_factor = random.randint(1, 50)
        blood_distance = int((290/blood_size_factor)**1.4)
        blood = {
            'color': BLOOD_COLOR,
            'position': (player.x + PLAYER_WIDTH//2 + random.randint(-blood_distance, blood_distance),
                         player.y + PLAYER_HEIGHT//2 + random.randint(-blood_distance, blood_distance)),
            'radius': int(blood_size_factor/1.5),
            'alpha': random.randint(1, int(250 * math.exp(-0.09 * blood_size_factor) + 1))
        }

        blood_stain = {
            'color': (130,0,0),
            'position': (player.x + PLAYER_WIDTH//2,
                         player.y + PLAYER_HEIGHT//2),
            'radius': random.randint(5, 10),
            'alpha': 30
        }

        blood_list.append(blood)
        blood_stain_list.append(blood_stain)

        # Draw blood stains
        for blood_stain in blood_stain_list:
            blood_stain_surf = pygame.Surface((blood_stain['radius']*2, blood_stain['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(blood_stain_surf, blood_stain['color'] + (blood_stain['alpha'],), (blood_stain['radius'], blood_stain['radius']), blood_stain['radius'])
            WIN.blit(blood_stain_surf, (blood_stain['position'][0] - blood_stain['radius'], blood_stain['position'][1] - blood_stain['radius']))

        # draw player and monster
        mon_rand_x = random.choice([-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,-10,10])
        mon_rand_y = random.choice([-2,-1,-1,-1,-1,0,0,0,0,1,1,1,1,2,-10,10])
        player.x += random.choice([-3,0,1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0-1,0,0,0,0,0,3,7])
        player.y += random.choice([-4,-2-1,-1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,-1,0,0,0,0,0,0,0,0,3,4])
        
        WIN.blit(PLAYER, (player.x, player.y))
        WIN.blit(MONSTER, (player.x + mon_rand_x, player.y + mon_rand_y))

        # Draw blood splatters
        for blood in blood_list:
            blood_surf = pygame.Surface((blood['radius']*2, blood['radius']*2), pygame.SRCALPHA)
            pygame.draw.circle(blood_surf, blood['color'] + (blood['alpha'],), (blood['radius'], blood['radius']), blood['radius'])
            WIN.blit(blood_surf, (blood['position'][0] - blood['radius'], blood['position'][1] - blood['radius']))
        
        LIGHT_SIZE -= 2
        
        LIGHT = pygame.transform.rotate(
            pygame.transform.scale(light, (LIGHT_SIZE, LIGHT_SIZE)), 0)
        WIN.blit(LIGHT, (player.x - LIGHT_SIZE/2, player.y - LIGHT_SIZE/2))

        for obstacle in obstacle_list:
                pygame.draw.rect(WIN, BLACK, obstacle)


        
        pygame.display.update()
            


# Function movement of the monster
def handle_monster_movement(monster, player):
    # Calculate the direction vector from the monster to the player
    dx = player.x - monster.x
    dy = player.y - monster.y

    # Calculate the angle between the monster and the player
    angle = math.atan2(dy, dx)
    # Calculate the X and Y components of the velocity using trigonometric functions
    vel_x = MONSTER_VEL * math.cos(angle)
    vel_y = MONSTER_VEL * math.sin(angle)

    # Update the monster's position
    monster.x += vel_x
    monster.y += vel_y
    #print(vel_x, vel_y)


# Function player movement
def handle_player_movement(keys_pressed, player):
    global PLAYER
    if keys_pressed[pygame.K_a]: # LEFT
        player.x -= PLAYER_VEL
    if keys_pressed[pygame.K_d]: # RIGHT
        player.x += PLAYER_VEL
    if keys_pressed[pygame.K_w]: # UP
        player.y -= PLAYER_VEL
    if keys_pressed[pygame.K_s]: # DOWN
        player.y += PLAYER_VEL

    player_pos  = WIN.get_rect().center
    player_rect = PLAYER.get_rect(center = player_pos)

    mx, my = pygame.mouse.get_pos()
    dx, dy = mx - player_rect.centerx, my - player_rect.centery
    angle = math.degrees(math.atan2(-dy, dx)) - 0

    PLAYER = pygame.transform.rotate(PLAYER, angle)
    player_rect = PLAYER.get_rect(center = player_rect.center)



### Main game loop ###
async def play_game():
    global PLAYER_VEL, PLAYER_DIFF_VEL, draw_blood, stop_mixer, keep_playing, DIFFICULTY, N_OBSTICLES
    
    pygame.display.set_caption("Play!")

    monster_rect = pygame.Rect(WIDTH * .1, HEIGHT * .1 ,
                               MONSTER_WIDTH, MONSTER_HEIGHT)
    player_rect = pygame.Rect(WIDTH * .9, HEIGHT * .9,
                              PLAYER_WIDTH, PLAYER_HEIGHT)
    

    # load image light
    if DIFFICULTY == 'MILD':
        lichtkegel_image = 'lichtkegel_easy.png'
    elif DIFFICULTY == 'NIGHTMARE':
        lichtkegel_image = 'lichtkegel_medium.png'
    elif DIFFICULTY == 'TERROR':
        lichtkegel_image = 'lichtkegel_hard.png'
    else:
        print('ERROR: Lichtkegel-Bild oder Schwierigkeit falsch beladen')
    
    LIGHT_IMAGE = pygame.image.load(os.path.join('assets', 'images', lichtkegel_image)) # radial gradient used for light pattern
    LIGHT = pygame.transform.rotate(
        pygame.transform.scale(LIGHT_IMAGE, (LIGHT_SIZE, LIGHT_SIZE)), 0)
    
    generate_obstacles(N_OBSTICLES, player_rect, monster_rect)  # Generate N obstacles

    clock = pygame.time.Clock()
    run = True

    # Initialize variables to track time for sound play
    last_monster_sound_play_time = pygame.time.get_ticks()
    last_ambient_sound_play_time = pygame.time.get_ticks()
    sound_interval_monster = 20000 #random.randint(15000, 30000) # 15-30 seconds in milliseconds (1000 ms per second)
    sound_interval_ambient = 60000
    random_monster_sound = random.choice(os.listdir(r"assets\sounds\monster_sounds"))
    monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'monster_sounds', random_monster_sound))
    random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
    ambient_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'ambient_sounds', random_ambient_sound))

    # Variables for collision end sequence handling
    collision_time = None
    game_end_time = 15  # seconds

    start_monster_sound.play()
    breathing_sound.play()
    hit_sound.play()


    while run:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        clock.tick(FPS)

        # Button Back and Difficulty
        PLAY_BACK = Button(image=None, pos=(WIDTH * .95, HEIGHT * .05), 
                            text_input="BACK", font=get_font(10), base_color="Grey", hovering_color="White")
        PLAY_BACK.changeColor(PLAY_MOUSE_POS)

        DIFFICULTY_TEXT = get_font(10).render(f"Difficulty: {DIFFICULTY}",
                                              True, "White")
        DIFFICULTY_RECT = DIFFICULTY_TEXT.get_rect(center=(WIDTH * .1, HEIGHT * .95))
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    pygame.mixer.stop()
                    click_sound.play()
                    time.sleep(1)
                    await main_menu()

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_ESCAPE]: #ESCAPE
            run = False
            pygame.quit()
        
        handle_monster_movement(monster_rect, player_rect)

        if not draw_blood:
            handle_player_movement(keys_pressed, player_rect)
            draw_window(monster_rect, player_rect, LIGHT)
        
        #collision with obsticles
        if player_rect.collidelist(obstacle_list) >= 0:
            print('collision with obsticle: ', player_rect.collidelist(obstacle_list))
            safe_player_vel = PLAYER_VEL
            PLAYER_VEL = 1
        else:
            PLAYER_VEL = PLAYER_DIFF_VEL


        # Check for collision between monster and player (you can play the sound here)
        if monster_rect.colliderect(player_rect):
            PLAYER_VEL = 0
            draw_blood = True

            if collision_time is None:
                collision_time = pygame.time.get_ticks()  # Record the time of collision
            # Check if 15 seconds have passed since the collision
            if collision_time is not None and (pygame.time.get_ticks() - collision_time) / 1000 >= game_end_time:
                run = False  # End the game
                pygame.mixer.stop()
                keep_playing = False
                possessed_laugh_sound.play()
                time.sleep(2)
                main_menu()

            if not stop_mixer:
                pygame.mixer.stop()
                stop_mixer = True
                hit_sound.play()
                scream_sound.play()
                jumpscare_sound
                slit_sound.play()
                monster_eating_sound.play()
                eating_sound.play()
            
            drawing_blood(player_rect, LIGHT)
            
            
        # Check if 15 seconds have passed since the last sound play
        current_time = pygame.time.get_ticks()
        

        # monster sound
        if current_time - last_monster_sound_play_time >= sound_interval_monster:
            random_monster_sound = random.choice(os.listdir(r"assets\sounds\monster_sounds"))
            monster_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'monster_sounds', random_monster_sound))
            monster_sound.play()
            last_monster_sound_play_time = current_time

        # distance monster player & monster sound volume
        dist_monster_player = math.hypot(monster_rect.x-player_rect.x,
                                         monster_rect.y-player_rect.y)
        dist_monster_player_rel = dist_monster_player/MAX_DISTANC
        monster_sound_vol = 1 - dist_monster_player_rel
        monster_sound.set_volume(monster_sound_vol)
        ambient_sound.set_volume(monster_sound_vol)
        

        # ambient sound
        if current_time - last_ambient_sound_play_time >= sound_interval_ambient:
            random_ambient_sound = random.choice(os.listdir(r"assets\sounds\ambient_sounds"))
            ambient_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds',
                                                    'ambient_sounds', random_ambient_sound))
            ambient_sound.play()

            last_ambient_sound_play_time = current_time

        WIN.blit(DIFFICULTY_TEXT, DIFFICULTY_RECT)
        PLAY_BACK.update(WIN)
        pygame.display.update()

        ### Debugging ###
        #debugging space
        print('\n\n', '---Debugging---', '\n')
        print('current time: ', current_time)
        print('dist_monster_player: ', round(dist_monster_player, 2))
        print('dist_monster_player_rel: ', round(dist_monster_player_rel, 2))
        print('monster_sound_vol: ', round(monster_sound_vol, 2))
        print('get monster_sound vol: ', monster_sound.get_volume())
        print('get ambient_sound vol: ', ambient_sound.get_volume())
        print('draw_blood: ', draw_blood)
        print('stop_mixer: ', stop_mixer)


### Options Menu ###
async def options():
    global keep_playing, MONSTER_VEL, PLAYER_VEL, PLAYER_DIFF_VEL, DIFFICULTY, N_OBSTICLES

    # Get dimensions of the background image
    bg_opt_width = BG_opt.get_width()
    bg_opt_height = BG_opt.get_height()

    # Calculate the top-left position to center the image
    bg_opt_x = (WIDTH - bg_opt_width) // 2
    bg_opt_y = (HEIGHT - bg_opt_height) // 2


    easy_rect = pygame.transform.scale(pygame.image.load("assets/images/Options_buttons.png"), (150, 40))
    OPTIONS_EASY = Button(image=easy_rect, pos=(WIDTH//2, HEIGHT*0.35), 
                        text_input="MILD", font=get_font(10), base_color="Blue", hovering_color="Green")
    medium_rect = pygame.transform.scale(pygame.image.load("assets/images/Options_buttons.png"), (150, 40))
    OPTIONS_MEDIUM = Button(image=medium_rect, pos=(WIDTH//2, HEIGHT*0.42), 
                        text_input="NIGHTMARE", font=get_font(10), base_color="Black", hovering_color="Green")
    hard_rect = pygame.transform.scale(pygame.image.load("assets/images/Options_buttons.png"), (150, 40))
    OPTIONS_HARD = Button(image=hard_rect, pos=(WIDTH//2, HEIGHT*0.49), 
                        text_input="TERROR", font=get_font(10), base_color="Black", hovering_color="Green")

    back_opt_rect = pygame.transform.scale(pygame.image.load("assets/images/Options_buttons.png"), (100, 40))
    OPTIONS_BACK = Button(image=back_opt_rect, pos=(WIDTH//2, HEIGHT*0.8), 
                        text_input="BACK", font=get_font(10), base_color="Black", hovering_color="Green")

    while True:
        pygame.display.set_caption("Options")
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        #WIN.fill("white")
        WIN.blit(BG_opt, (bg_opt_x, bg_opt_y))

        OPTIONS_TEXT = get_font(60).render("Choose difficulty.", True, "Black")
        OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(WIDTH//2, HEIGHT*0.2))
        WIN.blit(OPTIONS_TEXT, OPTIONS_RECT)

        

        OPTIONS_EASY.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_EASY.update(WIN)
        OPTIONS_MEDIUM.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MEDIUM.update(WIN)
        OPTIONS_HARD.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_HARD.update(WIN)

        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(WIN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_EASY.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    OPTIONS_EASY.base_color = "Blue"
                    OPTIONS_MEDIUM.base_color = "Black"
                    OPTIONS_HARD.base_color = "Black"
                    MONSTER_VEL, PLAYER_DIFF_VEL = 1, 3
                    N_OBSTICLES = 35
                    DIFFICULTY = "MILD"
                if OPTIONS_MEDIUM.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    OPTIONS_EASY.base_color = "Black"
                    OPTIONS_MEDIUM.base_color = "Blue"
                    OPTIONS_HARD.base_color = "Black"
                    MONSTER_VEL, PLAYER_DIFF_VEL = 2, 3
                    N_OBSTICLES = 40
                    DIFFICULTY = "NIGHTMARE"
                if OPTIONS_HARD.checkForInput(OPTIONS_MOUSE_POS):
                    click_sound.play()
                    OPTIONS_EASY.base_color = "Black"
                    OPTIONS_MEDIUM.base_color = "Black"
                    OPTIONS_HARD.base_color = "Blue"
                    MONSTER_VEL, PLAYER_DIFF_VEL = 2, 3
                    N_OBSTICLES = 50
                    DIFFICULTY = "TERROR"
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    keep_playing = True
                    click_sound.play()
                    time.sleep(1)
                    switch_sound.play()
                    await main_menu()

        pygame.display.update()



### Main Menu ###
async def main_menu():
    global keep_playing, DIFFICULTY

    pygame.display.set_caption("Menu")


    # Get dimensions of the background image
    bg_width = BG.get_width()
    bg_height = BG.get_height()

    # Calculate the top-left position to center the image
    bg_x = (WIDTH - bg_width) // 2
    bg_y = (HEIGHT - bg_height) // 2

    # Resize button images
    play_image = pygame.transform.scale(pygame.image.load("assets/images/Play Rect.png"), (150, 40))
    options_image = pygame.transform.scale(pygame.image.load("assets/images/Options Rect.png"), (150, 40))
    quit_image = pygame.transform.scale(pygame.image.load("assets/images/Quit Rect.png"), (150, 40))

    random_menu_sound = random.choice(os.listdir(os.path.join('assets', 'sounds','music')))
    menu_sound = pygame.mixer.Sound(os.path.join('assets', 'sounds', 'music', random_menu_sound))

    if not keep_playing:
        menu_sound.play()
    keep_playing = False

    bg_girl_width = BG_girl_images[0].get_width()
    bg_girl_height = BG_girl_images[0].get_height()
    # Calculate the top-left position to center the image
    bg_girl_x = (WIDTH - bg_girl_width) // 2
    bg_girl_y = (HEIGHT - bg_girl_height) // 2

    bg_image_counter = 0
    slow_down_counter = 0

    while True:
        # Use the calculated position to blit the background image
        #WIN.blit(BG, (bg_x, bg_y))
        #draw girl BG
        
        

        WIN.blit(BG_girl_images[bg_image_counter], (bg_girl_x, bg_girl_y))
        
        if bg_image_counter >= 1624:
            bg_image_counter = 0
        else:
            if slow_down_counter <= 5:
                slow_down_counter += 1
            else:
                bg_image_counter += 1
                slow_down_counter = 0


        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(15).render("MAIN MENU", True, "#04000D")
        MENU_RECT = MENU_TEXT.get_rect(center=(WIDTH//2, HEIGHT*0.15))

        DIFF_TEXT = get_font(10).render(f"Difficulty: {DIFFICULTY}", True, "White")
        DIFF_RECT = DIFF_TEXT.get_rect(center=(WIDTH * .1, HEIGHT * .95))
        

        PLAY_BUTTON = Button(image=play_image, pos=(WIDTH//2, HEIGHT*0.6), 
                            text_input="PLAY", font=get_font(10), base_color="#9ED702", hovering_color="White")
        OPTIONS_BUTTON = Button(image=options_image, pos=(WIDTH//2, HEIGHT*0.7), 
                            text_input="OPTIONS", font=get_font(10), base_color="#9ED702", hovering_color="White")
        QUIT_BUTTON = Button(image=quit_image, pos=(WIDTH//2, HEIGHT*0.8), 
                            text_input="QUIT", font=get_font(10), base_color="#9ED702", hovering_color="White")

        WIN.blit(DIFF_TEXT, DIFF_RECT)
        WIN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(WIN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.stop()
                    click_sound.play()
                    time.sleep(1)
                    await play_game()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS): # add later
                    click_sound.play()
                    time.sleep(1)
                    switch_sound.play()
                    await options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    click_sound.play()
                    time.sleep(1)
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        await asyncio.sleep(0)


asyncio.run(main_menu())