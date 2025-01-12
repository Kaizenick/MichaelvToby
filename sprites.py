import pygame
from pygame.sprite import AbstractGroup
from settings import *
from random import choice,randint
import os

class Upgrade(pygame.sprite.Sprite):
    def __init__(self,pos,upgrade_type,groups):
        super().__init__(*groups)
        self.upgrade_type = upgrade_type
        gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        #os.path.join('graphics', 'upgrades',self.upgrade_type+".png")
        self.image = pygame.image.load(os.path.join('graphics', 'upgrades',self.upgrade_type+".png")).convert_alpha(gameDisplay)
        #self.image = pygame.image.load('.\\graphics\\upgrades\\'+ self.upgrade_type+".png").convert_alpha(gameDisplay)
        self.rect = self.image.get_rect(midtop = pos)

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300

    def update(self,dt):
        self.pos.y += self.speed * dt
        self.rect.y = round(self.pos.y)

        if self.rect.top > WINDOW_HEIGHT + 100:
            self.kill()
        

class Player(pygame.sprite.Sprite):
    def __init__(self,groups):
        super().__init__(groups)

        #setup
        #self.image = pygame.Surface((WINDOW_WIDTH//10,WINDOW_HEIGHT//20))
        import PIL
        gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        #os.path.join('graphics', 'other','Michael.png')
        self.player_img = pygame.image.load(os.path.join('graphics', 'other','Michael.png')).convert_alpha(gameDisplay)
        #self.player_img = pygame.image.load('.\\graphics\\other\\Michael.png').convert_alpha(gameDisplay)
        self.scaled_player_img = pygame.transform.scale(self.player_img, (WINDOW_WIDTH//6, WINDOW_HEIGHT//8))
        self.image = self.scaled_player_img
        #self.image.fill('red')
        self.hearts = 3
        self.size_level = 1
        self.speed_level = 1
        # position
        self.rect = self.image.get_rect(midbottom = (WINDOW_WIDTH//2,WINDOW_HEIGHT))
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 300
        
    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT]:
            self.direction.x = -1
        else:
            self.direction.x = 0
        
    def screen_constraints(self):
        if self.rect.right > WINDOW_WIDTH:
            self.rect.right = WINDOW_WIDTH
            self.pos.x = self.rect.x
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.pos.x = self.rect.x

    def update(self,dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.x = round(self.pos.x)
        self.screen_constraints()
    
    def upgrade(self,upgrade_type):
        if upgrade_type == 'michael_running':
            if self.speed_level == 1:
                self.speed += 50
                self.speed_level += 1
            elif self.speed_level == 2:
                self.speed += 70
                self.speed_level += 1
            else:
                pass
        
        if upgrade_type == 'holly':
            self.hearts += 1

        
        if upgrade_type == 'kevin_chilly':
            if self.size_level == 1:
                gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                #os.path.join('graphics', 'other','Michael_kevin_size1.png')
                self.player_img = pygame.image.load(os.path.join('graphics', 'other','Michael_kevin_size1.png')).convert_alpha(gameDisplay)
                self.scaled_player_img = pygame.transform.scale(self.player_img, (int((WINDOW_WIDTH*1.3//6)), int((WINDOW_HEIGHT//8))))
                self.image = self.scaled_player_img
                self.rect = self.image.get_rect(center = self.rect.center)
                self.pos.x = self.rect.x
                self.size_level += 1
                
            elif self.size_level == 2:
                gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                #os.path.join('graphics', 'other','Michael_kevin_size2.png')
                self.player_img = pygame.image.load(os.path.join('graphics','other','Michael_kevin_size2.png')).convert_alpha(gameDisplay)
                self.scaled_player_img = pygame.transform.scale(self.player_img, (int((WINDOW_WIDTH*1.5//6)), int((WINDOW_HEIGHT//8))))
                self.image = self.scaled_player_img
                self.rect = self.image.get_rect(center = self.rect.center)
                self.pos.x = self.rect.x
                self.size_level += 1
                
            else:
                pass
        
        if upgrade_type == 'toby_hand':
            gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            #os.path.join('graphics', 'other','Michael.png')
            self.player_img = pygame.image.load(os.path.join('graphics', 'other','Michael.png')).convert_alpha(gameDisplay)
            self.scaled_player_img = pygame.transform.scale(self.player_img, (WINDOW_WIDTH//6, WINDOW_HEIGHT//8))
            self.image = self.scaled_player_img
            self.rect = self.image.get_rect(center = self.rect.center)
            self.pos.x = self.rect.x
            
            self.speed = 300
            self.size_level = 1
            self.speed_level = 1
            self.hearts -= 1

        
            
        

class Ball(pygame.sprite.Sprite):
    def __init__(self,group,player,blocks):
        super().__init__(group)

        #collision objects
        self.player = player
        self.blocks = blocks

        gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        os.path.join('graphics', 'other','suck_on_this_withoutback_small.png')
        self.ball_img = pygame.image.load(os.path.join('graphics', 'other','suck_on_this_withoutback_small.png')).convert_alpha(gameDisplay)
        self.scaled_ball_img = pygame.transform.scale(self.ball_img, (WINDOW_WIDTH//35, WINDOW_HEIGHT//20))
        self.image = self.scaled_ball_img

        self.rect = self.image.get_rect(midbottom = player.rect.midtop )
        self.old_rect = self.rect.copy()
        self.direction = pygame.math.Vector2((choice((1,-1)),-1))
        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 400

        # active
        self.active = False
    
    def window_collision(self,direction):
        if direction == 'horizontal':
            if  self.rect.left < 0:
                self.rect.left = 0
                self.pos.x = self.rect.x
                self.direction.x = -1 * self.direction.x
            
            if  self.rect.right > WINDOW_WIDTH:
                self.rect.right = WINDOW_WIDTH
                self.pos.x = self.rect.x
                self.direction.x = -1 * self.direction.x

        if direction == 'vertical':
            if self.rect.top < 0:
                self.rect.top = 0
                self.pos.y = self.rect.y
                self.direction.y = -1 * self.direction.y
            
            if self.rect.bottom > WINDOW_HEIGHT:
                self.active = False
                self.direction.y = -1 * self.direction.y
                self.player.hearts -=1
                gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
                os.path.join('graphics', 'other','Michael.png')
                self.player.player_img = pygame.image.load(os.path.join('graphics', 'other','Michael.png')).convert_alpha(gameDisplay)
                self.player.scaled_player_img = pygame.transform.scale(self.player.player_img, (WINDOW_WIDTH//6, WINDOW_HEIGHT//8))
                self.player.image = self.player.scaled_player_img
                self.player.rect = self.player.image.get_rect(center = self.player.rect.center)
                self.player.pos.x = self.player.rect.x
                self.player.speed = 300
                self.player.size_level = 1
                self.player.speed_level = 1
                

                
                

    def collision(self,direction):
        overlap_sprites = pygame.sprite.spritecollide(self,self.blocks,False)
        if self.rect.colliderect(self.player.rect):
            overlap_sprites.append(self.player)
        

        if overlap_sprites:
            if direction == 'horizontal':
                for sprite in overlap_sprites:
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left - 1
                        self.pos.x = self.rect.x
                        self.direction.x = -1 * self.direction.x
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right + 1
                        self.pos.x = self.rect.x
                        self.direction.x = -1 * self.direction.x

                    if getattr(sprite,'health',None):
                        sprite.get_damage(1)

            if direction == 'vertical':
                for sprite in overlap_sprites:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top - 1
                        self.pos.y = self.rect.y
                        self.direction.y = -1 * self.direction.y
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom + 1
                        self.pos.y = self.rect.y
                        self.direction.y = -1 * self.direction.y

                    if getattr(sprite,'health',None):
                        sprite.get_damage(1)

            



    def update(self,dt):
        if self.active:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.old_rect = self.rect.copy()
            
            # horizontal movement + collision
            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = (round(self.pos.x))
            self.collision('horizontal')
            self.window_collision('horizontal')

            # vertical movement + collision
            self.pos.y += self.direction.y * self.speed * dt
            self.rect.y = (round(self.pos.y))
            self.collision('vertical')
            self.window_collision('vertical')
            
        else:
            midbottom_coordinates = list(self.player.rect.midtop)
            midbottom_coordinates[1] = midbottom_coordinates[1] + 20
            self.rect.midbottom = tuple(midbottom_coordinates)
            self.pos = pygame.math.Vector2(self.rect.topleft)
        
        
class Block(pygame.sprite.Sprite):
    def __init__(self, block_type,pos,groups,create_upgrade):
        super().__init__(groups)
        gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.img = BLOCK_LEGEND[block_type]
        os.path.join('graphics', 'blocks',self.img)
        os.path.join('graphics', 'blocks',self.img)
        self.block_img = pygame.image.load(os.path.join('graphics', 'blocks',self.img)).convert_alpha(gameDisplay)
        #self.block_img = pygame.image.load('.\\graphics\\blocks\\'+self.img).convert_alpha(gameDisplay)
        #self.block_img = pygame.image.load('.\\graphics\\blocks\\'+self.img).convert()
        self.scaled_ball_img = pygame.transform.scale(self.block_img, (BLOCK_WIDTH,BLOCK_HEIGHT))
        self.image = self.scaled_ball_img
        self.rect = self.image.get_rect(topleft = pos)
        self.old_rect = self.rect.copy()

        self.health = int(block_type)
        self.create_upgrade = create_upgrade
    def get_damage(self,amount):
        self.health  -= amount

        if self.health > 0:
            #update the image
            gameDisplay = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.img = BLOCK_LEGEND[str(self.health)]
            self.block_img = pygame.image.load(os.path.join('graphics', 'blocks',self.img)).convert_alpha(gameDisplay)
            #self.block_img = pygame.image.load('.\\graphics\\blocks\\'+self.img).convert()
            self.scaled_ball_img = pygame.transform.scale(self.block_img, (BLOCK_WIDTH,BLOCK_HEIGHT))
            self.image = self.scaled_ball_img
            self.old_rect = self.rect.copy()
            if randint(0,10)<3:
                self.create_upgrade(self.rect.center)
        else:
            if randint(0,10)<7:
                self.create_upgrade(self.rect.center)
            self.kill()




        
            
