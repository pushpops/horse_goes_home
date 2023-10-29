import pygame
import settings as set

IMAGEDICT = {'field': pygame.image.load('pic/field.png'),
			'title': pygame.image.load('pic/title.png'),
			'back': pygame.image.load('pic/back.png'),
			'back2': pygame.image.load('pic/back2.png'),
			'stone': pygame.image.load('pic/stone.png'),
			'walkr': pygame.image.load('pic/walkright.png'),
			'walkl': pygame.image.load('pic/walkleft.png'),
			'stop': pygame.image.load('pic/stop.png'),
			'run1': pygame.image.load('pic/run1.png'),
			'run2': pygame.image.load('pic/run2.png'),
			'smile': pygame.image.load('pic/smile.png'),
			'red': pygame.image.load('pic/red.png'),
			'white': pygame.image.load('pic/white.png'),
			'yellow': pygame.image.load('pic/yellow.png'),
			'mole': pygame.image.load('pic/mole.png'),
			'bad': pygame.image.load('pic/fail.png'),
			'cloud': pygame.image.load('pic/cloud.png'),
			'bird': pygame.image.load('pic/bird.png'),
			'home': pygame.image.load('pic/house.png'),
			'howtoplay': pygame.image.load('pic/howtoplay.png'),
			'crun1R': pygame.transform.scale(pygame.image.load('pic/callotrun1.png'), (int(set.WIDTH*0.8), int(set.HEIGHT*0.8))),
			'crun2R': pygame.transform.scale(pygame.image.load('pic/callotrun2.png'), (int(set.WIDTH*0.8), int(set.HEIGHT*0.8))),
			}
IMAGEDICT['crun1L'] = pygame.transform.flip(IMAGEDICT['crun1R'], True, False)
IMAGEDICT['crun2L'] = pygame.transform.flip(IMAGEDICT['crun2R'], True, False)