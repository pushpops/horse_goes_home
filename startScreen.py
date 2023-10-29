import pygame
from pygame.locals import * # キー操作イベント
import colorAndFont as colfon
import math
import horseGoesHome as main
import settings as set
import images as img
import random

def show():
	CHOICE = pygame.mixer.Sound("se/Onoma-Inspiration08-3(Low-Delay).mp3")
	CHOICE.set_volume(0.5)
	pygame.mixer.music.load("se/dummy.wav")
	pygame.mixer.music.set_volume(0.2)
	pygame.mixer.music.play(loops=-1)
	titley = 0
	horsey = 0
	horsex = 0
	im = 'crun1R'
	speed = 5
	noise = 0
	Key = ''
	while True:
		set.DISPLAYSURF.blit(img.IMAGEDICT['field'],(0,0))
		set.DISPLAYSURF.blit(img.IMAGEDICT['title'],(0,titley-30))
		set.DISPLAYSURF.blit(img.IMAGEDICT[im],(horsex,horsey))

		drawPressKeyMsgS()
		Key = checkForKeyPress()
		if Key == 'howToPlay':
			howToPlay()
		elif Key == 'runGame':
			CHOICE.play()
			return
			
		pygame.display.update()
		set.FPSCLOCK.tick(set.FPS)
		titley = 7*math.sin(pygame.time.get_ticks()/600)
		horsey = 10*math.sin(pygame.time.get_ticks()/150)+noise
		horsex += speed

		if horsex % 60 == 0:
			if speed > 0:
				if im == 'crun1R':
					im = 'crun2R'
				else: im = 'crun1R'
			elif im == 'crun1L':
				im = 'crun2L'
			else: im = 'crun1L'
		if horsex < -500 or horsex > set.WIDTH-100:
			speed = -speed
			noise = random.randint(100,200)
			
def drawPressKeyMsgS():
    pressSpaceSurf = colfon.BASICFONT.render('Press SPACE to play.', True, colfon.DARKGRAY)
    pressSpaceRect = pressSpaceSurf.get_rect()
    pressSpaceRect.topleft = (set.WIDTH - 200, set.HEIGHT - 30)
    set.DISPLAYSURF.blit(pressSpaceSurf, pressSpaceRect)

    pressEnterSurf = colfon.BASICFONT.render('Press ENTER to see how to play.', True, colfon.DARKGRAY)
    pressEnterRect = pressEnterSurf.get_rect()
    pressEnterRect.topleft = (20, set.HEIGHT - 30)
    set.DISPLAYSURF.blit(pressEnterSurf, pressEnterRect)
	
def howToPlay():
	im = 'run1'
	jump = dict(x = 350, y = 0, defY = 50, height = 3, t = 0, jumping = True)
	count = 0
	Key = ''
	while True:
		Key = checkForKeyPress()
		if Key == 'howToPlay':
			return
		count += 1
		if count % 20 == 0:
			im = 'run2'
			count = 0
			if jump['jumping'] == False:
				jump['jumping'] = True
		elif count % 10 == 0:
			im = 'run1'
			
		set.DISPLAYSURF.blit(im.IMAGEDICT['howtoplay'],(0,0))
		set.DISPLAYSURF.blit(im.IMAGEDICT[im],(-50,50))
		_, jump = main.drawCharacter(im.IMAGEDICT['run1'],jump)
		set.refreshFrame()
		
def checkForKeyPress():
	for event in pygame.event.get(): # clear event queue 
		if event.type == KEYDOWN:
			if event.key == K_SPACE:
				return 'runGame'
			elif event.key == K_RETURN:
				return 'howToPlay'
			elif event.key == K_ESCAPE:
				set.terminate()
		elif event.type == QUIT:
			set.terminate()
	return 