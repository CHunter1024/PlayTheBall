import pygame
import sys
import traceback
from  pygame.locals import *
from  random import  *
import TheBall
import TheGlass

def main():
    pygame.init()
    pygame.mixer.init()

    #图片
    grayball_image = "photo/gray_ball.png"
    greenball_image = "photo/green_ball.png"
    bg_image = "photo/background.png"
    glass_image = "photo/glass.png"
    mouse_image = "photo/hand.png"
    win_image = "photo/win.png"

    running = True

    #添加背景音乐并播放
    pygame.mixer.music.load("music/bg_music.mp3")
    pygame.mixer.music.play()

    #添加音效
    loser_sound = pygame.mixer.Sound("music/loser.wav")
    winner_sound = pygame.mixer.Sound("music/winner.wav")
    hole_sound = pygame.mixer.Sound("music/hole.wav")

    #音乐播放完时游戏结束
    GAMEOVER = USEREVENT
    pygame.mixer.music.set_endevent(GAMEOVER)

    #根据背景图片指定游戏界面尺寸
    bg_size = width,height = 1024,681
    screen = pygame.display.set_mode(bg_size)
    pygame.display.set_caption("PlayTheBall")

    background = pygame.image.load(bg_image)

    #五个黑洞的位置范围
    hole = [(114,122,196,204),(222,230,387,395),(500,508,317,325),(695,703,189,197),(903,911,416,424)]

    #消息列表
    msgs = []

    #用来存放小球对象的列表
    balls = []
    group = pygame.sprite.Group()

    #创建五个小球
    BALL_NUM = 5
    for i in range(BALL_NUM):
        #位置随机，速度随机
        position = randint(0,width-100),randint(0,height-100)
        speed = [randint(1,5),randint(1,5)]
        ball = TheBall.Ball(grayball_image,greenball_image,position,speed,bg_size,10*(i+1))
        while pygame.sprite.spritecollide(ball,group,False,pygame.sprite.collide_circle):
            ball.rect.left,ball.rect.top = randint(0,width-100),randint(0,height-100)
        balls.append(ball)
        group.add(ball)

    #创建玻璃面板
    glass = TheGlass.Glass(glass_image,mouse_image,bg_size)

    #记录鼠标1s内产生事件数量
    motion = 0

    #自定义事件，每一秒触发该事件，调用check()检测motion的值是否匹配目标，并初始化motion，以便记录下1s的鼠标事件数量
    MYTIMER = USEREVENT + 1
    pygame.time.set_timer(MYTIMER,1000)

    clock = pygame.time.Clock()

    while running:
    	#玩家可操控绿色小球的行为
        key_pressed = pygame.key.get_pressed()
        if key_pressed[K_w] or key_pressed[K_UP]:
            for each in group:
                if each.control:
                    each.rect.top -= 1

        if key_pressed[K_s] or key_pressed[K_DOWN]:
            for each in group:
                if each.control:
                    each.rect.top += 1

        if key_pressed[K_a] or key_pressed[K_LEFT]:
            for each in group:
                if each.control:
                    each.rect.left -= 1

        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            for each in group:
                if each.control:
                    each.rect.left += 1

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == GAMEOVER:
                loser_sound.play()
                pygame.time.delay(4500)
                running = False

            elif event.type == MYTIMER:
                if motion:
                    for each in group:
                        if each.check(motion):
                            each.speed = [0,0]
                            each.control = True
                    motion = 0

            elif event.type == MOUSEMOTION:
                motion += 1

        
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    for each in group:
                        if each.control:
                            for i in hole:
                                if i[0] <= each.rect.left <= i[1] and i[2] <= each.rect.top <= i[3]:
                                    hole_sound.play()
                                    each.speed = [0,0]
                                    group.remove(each)
                                    temp = balls.pop(balls.index(each))
                                    balls.insert(0,temp)
                                    hole.remove(i)
                            if not hole:
                                pygame.mixer.music.stop()
                                winner_sound.play()
                                pygame.time.delay(3000)
                                msg = pygame.image.load(win_image).convert_alpha()
                                msg_pos = (width - msg.get_width()) // 2,(height - msg.get_height()) // 2
                                msgs.append((msg,msg_pos))
                                running = False

        screen.blit(background,(0,0))
        screen.blit(glass.glass_image,glass.glass_rect)

        glass.mouse_rect.left,glass.mouse_rect.top = pygame.mouse.get_pos()
        if glass.mouse_rect.left < glass.glass_rect.left:
            glass.mouse_rect.left = glass.glass_rect.left
        if glass.mouse_rect.right > glass.glass_rect.right:
            glass.mouse_rect.right = glass.glass_rect.right
        if glass.mouse_rect.top < glass.glass_rect.top:
            glass.mouse_rect.top = glass.glass_rect.top
        if glass.mouse_rect.bottom > glass.glass_rect.bottom:
            glass.mouse_rect.bottom = glass.glass_rect.bottom

        screen.blit(glass.mouse_image,glass.mouse_rect)

        for each in balls:
            each.move()
            if each.collide:
                each.speed = [randint(1, 5), randint(1, 5)]
                each.collide = False
            if each.control:
                #画绿色的小球
                screen.blit(each.greenball_image, each.rect)
            else:
                screen.blit(each.grayball_image,each.rect)

        for each in group:
            group.remove(each)

            #碰撞检测
            if pygame.sprite.spritecollide(each,group,False,pygame.sprite.collide_circle):
                each.side[0] = -each.side[0]
                each.side[1] = -each.side[1]
                each.collide = True
                if each.control:
                    each.side[0] = -1
                    each.side[1] = -1
                    each.control = False

            group.add(each)

        for msg in msgs:
            screen.blit(msg[0],msg[1])

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()