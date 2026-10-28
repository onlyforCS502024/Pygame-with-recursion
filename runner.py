import pygame
import random
import os
import math
from os import listdir
from os.path import isfile, join
#initializing pygame module
pygame.init()  
#setting caption at the top of the pygame window
pygame.display.set_caption("Runner") 
#setting global variables + game window

width, height = 1000, 800
frames_per_second = 60
player_velocity = 5

game_window = pygame.display.set_mode((width, height))




#defining a class for player that inherits pygame's built in sprite class
class Player(pygame.sprite.Sprite):
    player_colour= (0,0,255) #class variable
    gravity = 1 #like 9.8 acceleration in real life
    def __init__(self, x, y, width_player, height_player):
        #rectangle box to hold the player image for perfect collisions
        self.rect = pygame.Rect(x,y,width_player,height_player)
        #defining player instance variables for horizontal and vertical velocities
        self.horizontal_velocity = 0
        self.vertical_velocity = 0
        self.mask = None
        #tracks player direction movement to put correct animaations and movement 
        self.direction = "left"
        #animation couunt used to tack animation images for player
        self.animation_count = 0
        #to track player's vertical falling time to account for acceleration
        self.falling_count = 0

    #for updating player's position by adding and subtracting velocity from x and y
    def player_move(self, displacement_x, displacement_y):
        #current horizontal cordinate of the box on the screen
        self.rect.x += displacement_x  #+=
        #current vertical cordinate of the box on the screen
        self.rect.y += displacement_y  #+=
    #setting direction to left for correct animation images and movement to left
    def player_move_left(self, velocity):
        self.horizontal_velocity = -velocity
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0 
    #setting direction to right for correct animation images and movement to right
    def player_move_right(self, velocity):
        self.horizontal_velocity = velocity
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0 
    #updating player's position every frame 
    def player_loop(self, fps):
        #increases vertical velocity based on how long the player has been falling, keeping max increase at 1
        self.vertical_velocity += min(1, (self.falling_count/ fps) * self.gravity)
        #updates the player's physical coordinates using the updated velocities 
        self.player_move(self.horizontal_velocity, self.vertical_velocity)
        self.falling_count += 1
    #drawing a temporary colored rectangle to hold the player
    def player_draw(self, player_window):
        pygame.draw.rect(player_window, self.player_colour, self.rect)


def setting_background(tile_block):
    #loading bg image file from assets to pygame bg image loader
    image = pygame.image.load(join("assets", "Background", tile_block))
    #getting exact width & height dimensions of the bg tile
    _x, _y, width_image, height_image = image.get_rect()
    tiles = []
    #finding how many tiles are needed to fill the frame
    for i in range(width// width_image +1):
        for j in range(height // height_image +1):
            # position[x,y] -> gives x, y cordinates of each tile
            position = (i* width_image, j * height_image)
            #tiles stores all cordinates to later form the bg in each frame
            tiles.append(position)

    return tiles, image
#function used to draw each tile in its postion on the frame each second and draws the player
def draw_background_player(game_window, background, bg_image, CHARACTER):
    for tile in background:
        #blit draws each tile on frame
        game_window.blit(bg_image, tile)
    #calls player_draw function in player class to draw the player on screen
    CHARACTER.player_draw(game_window)
    #refreshes screen to make tiles visible
    pygame.display.update()
#function for handling key presses and collision mechanics 
def checking_user_keys_pressed(CHARACTER):
    #getting keys that are currently being pressed by the user
    keys_pressed_currently = pygame.key.get_pressed()
    #keeping velocity zero until the keys are pressed continously 
    CHARACTER.horizontal_velocity = 0
    #setting player velocities as soon as the LEFT and RIGHT keys are pressed
    if keys_pressed_currently[pygame.K_LEFT]:
        CHARACTER.player_move_left(player_velocity)
    if keys_pressed_currently[pygame.K_RIGHT]:
        CHARACTER.player_move_right(player_velocity)


def main(game_window):
    #clock object created
    clock = pygame.time.Clock()
    #variables hold tile position and tile image returned from setting_background function
    background_tile, bg_image = setting_background("Pink.png")
    #player object created right before the game loop starts
    CHARACTER = Player(100,100,50,50)

    run = True 
    while run:
        #making the gamerun 60 times per second
        clock.tick(frames_per_second)
        #iterating through all user inputs
        for event in pygame.event.get():
            #checking if user clicked X(cross)
            if event.type == pygame.QUIT:
                run = False
                break 
        #loop function actually moves the player on screen
        CHARACTER.player_loop(frames_per_second)
        checking_user_keys_pressed(CHARACTER)
        #game started bg needs to be drawn out 
        draw_background_player(game_window, background_tile, bg_image, CHARACTER)
    #closing pygame
    pygame.quit()
    #terminating python program
    quit()




#only executes the file if run directly and not when something is imported from it
if __name__ == "__main__":
    main(game_window)