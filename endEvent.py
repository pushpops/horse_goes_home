import images as im
import pygame
from pygame.locals import *
import sounds as sd
import colorAndFont as colfon

# ゲーム終了時の演出
def show(DISPLAYSURF,RESULT,cx,cityx):
	im = 'walkr'
	homex = set.WIDTH+200
	scorefont = pygame.font.Font(None, 90)
	score = list(map(translateChar2Num,RESULT))
	score = round((sum(score)/(len(score)*3))*100,3)
	drumtime = 0
	DRUMLEN = (sd.DRUM.get_length()-3.000)*1000 # millisecond
	WALK = 15*14

	for i in range(WALK):
		if i % 15 == 0:
			if im == 'walkl':
				im = 'walkr'
			else: im = 'walkl'
		elif i == WALK-1:
			im = 'stop'
		cx -= 0.3
		cityx -= 0.3
		homex -= 2.4
		# 背景の描画
		DISPLAYSURF.blit(im.IMAGEDICT['back'], (0, 0))
		DISPLAYSURF.blit(im.IMAGEDICT['cloud'], (cx, 0))
		DISPLAYSURF.blit(im.IMAGEDICT['back2'], (cityx, 0))
		DISPLAYSURF.blit(im.IMAGEDICT['back2'], (cityx + set.WIDTH,0))
		DISPLAYSURF.blit(im.IMAGEDICT['home'], (homex,-10))
		# 馬の描画
		DISPLAYSURF.blit(im.IMAGEDICT[im],(0,0))
		set.refreshFrame()

		if i == 15*6:
			sd.DRUM.play()
			drumtime = pygame.time.get_ticks()

	while drumtime+DRUMLEN-pygame.time.get_ticks()>0:
		set.screen.blit(scorefont.render(str(score)+'%', True, (0,0,0)), [70,50])
		set.refreshFrame()
	
	if score >= 80:
		pygame.time.wait(700)
		sd.CLEAR.play()
		DISPLAYSURF.blit(im.IMAGEDICT['smile'],(0,0))
		set.refreshFrame()
		
	pygame.event.clear() # clear event queue
	drawPressKeyMsgE()
	while True:
		for event in pygame.event.get(): # clear event queue 
			if event.type == KEYDOWN and event.key == K_SPACE:
				pygame.display.update()
				set.FPSCLOCK.tick(set.FPS)
				break
		break
		
def drawPressKeyMsgE():
    pressKeySurf = colfon.BASICFONT.render('Press SPACE to go to the Title.', True, colfon.DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (20, set.HEIGHT - 30)
    set.DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
	
# ノーツの評価を数値に変換する
def translateChar2Num(a_result):
	a_score = 0
	if a_result == 'Perfect!':
		a_score = 3
	elif a_result == 'Good!':
		a_score = 3*0.7
	elif a_result == 'Bad':
		a_score = 3*0.1
	elif a_result == 'Miss':
		a_score = -3*0.1
	return a_score