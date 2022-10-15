import pygame

#定义玻璃面板类
class Glass(pygame.sprite.Sprite):
    def __init__(self,glass_image,mouse_image,bg_size):
        #初始化动画精灵
        pygame.sprite.Sprite.__init__(self)

        self.glass_image = pygame.image.load(glass_image).convert_alpha()
        self.glass_rect = self.glass_image.get_rect()
        self.glass_rect.left,self.glass_rect.top = (bg_size[0] - self.glass_rect.width) // 2,bg_size[1] - self.glass_rect.height

        self.mouse_image = pygame.image.load(mouse_image).convert_alpha()
        self.mouse_rect = self.mouse_image.get_rect()
        self.mouse_rect.left,self.mouse_rect.top = self.glass_rect.centerx,self.glass_rect.centery
        pygame.mouse.set_visible(False)