import pygame
from  random import  *

#球类继承自Spirte类
class Ball(pygame.sprite.Sprite):
    def __init__(self,grayball_image,greenball_image,position,speed,bg_size,target):
        #初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.grayball_image = pygame.image.load(grayball_image).convert_alpha()
        self.greenball_image = pygame.image.load(greenball_image).convert_alpha()
        self.rect = self.grayball_image.get_rect()
        #将小球放在指定位置
        self.rect.left,self.rect.top = position
        self.side = [choice([-1,1]),choice([-1,1])]
        self.speed = speed
        self.collide = False
        self.target = target
        self.control = False
        self.width,self.height = bg_size[0],bg_size[1]
        self.radius = self.rect.width / 2

    def move(self):
        if not self.control:
            self.rect = self.rect.move((self.side[0]*self.speed[0]),(self.side[1]*self.speed[1]))

        #如果小球的左（右、上、下）侧出了边界，那么将小球左（右、上、下）侧的位置改为右（左、下、上）侧边界
        if self.rect.right <= 0:
            self.rect.left = self.width
        elif self.rect.left >= self.width:
            self.rect.right = 0
        elif self.rect.bottom <= 0:
            self.rect.top = self.height
        elif self.rect.top >= self.height:
            self.rect.bottom = 0

    def check(self,motion):
        if self.target < motion < self.target + 5:
            return True
        else:
            return False