import pygame
import sys
import time
from settings import *
from sprites import Player, Ball, Block, Upgrade
from random import choice
import os


class Game:
    def __init__(self):

        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("No_God_Please_NO")
        self.bg = self.create_bg()

        # sprite group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.upgrade_sprites = pygame.sprite.Group()
        self.player = Player(self.all_sprites)
        self.stage_setup()
        self.ball = Ball(self.all_sprites,self.player,self.block_sprites)

        # hearts
        gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        #os.path.join('graphics', 'other', 'PrisonMike_nobg_b.png')
        self.heart_surf = pygame.image.load(os.path.join('graphics', 'other', 'PrisonMike_nobg_b.png')).convert_alpha(gameDisplay)
        #self.heart_surf = pygame.image.load('.\\graphics\\other\\PrisonMike_nobg_b.png').convert_alpha(gameDisplay)
        self.scaled_heart_surf = pygame.transform.scale(self.heart_surf, (BLOCK_WIDTH//4,BLOCK_HEIGHT//2.5))
        self.image = self.scaled_heart_surf

    def create_upgrade(self,pos):
        upgrade_type = choice(UPGRADES)
        Upgrade(pos,upgrade_type,[self.all_sprites,self.upgrade_sprites])

    def create_bg(self):
        
        bg_path = os.path.join('graphics', 'other', 'background.png')
        bg_original = pygame.image.load(bg_path).convert()

        #bg_original = pygame.image.load('.\\graphics\\other\\background.png').convert()
        scaled_bg = pygame.transform.scale(bg_original, (WINDOW_WIDTH, WINDOW_HEIGHT))

        return (scaled_bg)
    
    
    def stage_setup(self):
        # cycle thrught all rows and columns of BLOCK_MAP

        for row_index,row in enumerate(BLOCK_MAP):
            for col_index,col in enumerate(row):
                if col != " ":
                    x = col_index * (BLOCK_WIDTH + GAP_SIZE) + GAP_SIZE//2
                    y = row_index * (BLOCK_HEIGHT + GAP_SIZE) + GAP_SIZE//2
                    Block(col,(x,y),[self.all_sprites,self.block_sprites],self.create_upgrade)

    def display_hearts(self):
        for i in range(self.player.hearts):
            x = i * self.heart_surf.get_width()//8
            self.display_surface.blit(self.image,(x,WINDOW_HEIGHT - 50))


    def upgrade_collision(self):
        overlap_sprites = pygame.sprite.spritecollide(self.player,self.upgrade_sprites,True)
        for sprite in overlap_sprites:
            self.player.upgrade(sprite.upgrade_type)

    def run(self):
        last_time = time.time()
        while True:

            # delta time
            dt = time.time() - last_time
            last_time = time.time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT or self.player.hearts <= 0:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.ball.active = True

            # update the game
            self.all_sprites.update(dt)
            self.upgrade_collision()

            # draw the frame
            self.display_surface.blit(self.bg, (0, 0))
            self.all_sprites.draw(self.display_surface)
            self.display_hearts()
        
            pygame.display.update()
            

    

game = Game()
game.run()
