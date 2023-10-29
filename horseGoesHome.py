import pygame
from pygame.locals import *
import random
import math
import hurdle as hu
import scoreReader
import score1
import images as im
import startScreen
import endEvent
import colorAndFont as colfon
import settings as set
import sounds as sd

def main():
	# initialise
	pygame.mixer.quit()
	pygame.mixer.pre_init(buffer=64)
	pygame.init()
	
	pygame.display.set_caption('HORSE GOES HOME')

	global screen 
	screen = pygame.display.set_mode((set.WIDTH, set.HEIGHT))

	RESULT = []
	cloud_x = 0
	while True:
		startScreen.show()
		RESULT,cloud_x,city_x = runGame()
		endEvent.show(RESULT,cloud_x,city_x)

def runGame():
	global notes_time_ary,is_hurdle_ary
	notes_time_ary, is_hurdle_ary = scoreReader.make_notes_time_ary(score1.bpm, score1.score)
	j = 0 			#index for judge with TIMING
	s = 0 			#index for set hurdle pictures with TIMING
	INPUT = [0]*170	#input data from player
	JUDGE = ['']*170
	DIST = [0]*170
	cloud_x = 500 #cloud's x
	city_x = 0 #city's x
	hurdles = []
	image = im.IMAGEDICT['stop']
	jump = dict(x = 0, y = 0, defY = 0, height = 100, t = 0, jumping = False)
	time = 0
	judgement = ''

	# 楽曲を読み込み、音量を設定、再生開始
	pygame.mixer.music.load("se/horse.wav")
	pygame.mixer.music.set_volume(1.2)
	pygame.mixer.music.play()
	# main game loop
	while True:	
		time = pygame.mixer.music.get_pos()/1000	#get bgm's play time

		# 背景オブジェクトの描画
		set.DISPLAYSURF.blit(im.IMAGEDICT['back'],(0,0))
		set.DISPLAYSURF.blit(im.IMAGEDICT['cloud'],(cloud_x,0))	
		set.DISPLAYSURF.blit(im.IMAGEDICT['back2'],(city_x,0))
		set.DISPLAYSURF.blit(im.IMAGEDICT['back2'],(city_x+set.WIDTH,0))
		# 4秒後から曲が始まる。
		if time > 4.0:	
			cloud_x = moveCloud(cloud_x)
			city_x = moveCity(city_x)
		
		# 地面にハードルを描画
		s, hurdles = drawHurdle(s,hurdles)
		
		# キーボード入力について分岐
		for event in pygame.event.get():					
			if event.type == KEYDOWN:	
				# スペースキーが押された
				if event.key == K_SPACE:
					jump['jumping'] = True
					# ジャンプ効果音再生
					sd.JUMP.play()
					# 判定	
					j,INPUT,JUDGE,DIST,image,judgement = judge(j,time,INPUT,JUDGE,DIST,image,judgement,jump)
					# 判定で出た画像がbadなら
					if image == im.IMAGEDICT['bad'] and judgement != "Bad":
						# 馬が走っている画像に設定する
						image = im.IMAGEDICT['run1']
				elif event.key == K_f or event.key == K_j:
					if image == im.IMAGEDICT['stop'] or image == im.IMAGEDICT['run2'] or image == im.IMAGEDICT['bad']:
						image = im.IMAGEDICT['run1']
					elif image == im.IMAGEDICT['run1']:
						image = im.IMAGEDICT['run2']
					#判定
					j,INPUT,JUDGE,DIST,image,judgement = judge(j,time,INPUT,JUDGE,DIST,image,judgement,jump)	
				elif event.key == K_RETURN:
					pause()					
				elif event.key == K_ESCAPE:
					set.terminate()
			elif event.type == QUIT:
				set.terminate()

		#音符を見逃したか判定
		if j < len(notes_time_ary):
			j,INPUT,JUDGE,DIST,image,judgement = missed(j,time,INPUT,JUDGE,DIST,image,judgement)

		#判定結果を表示	
		screen.blit(colfon.font.render(judgement, True, (0,0,0)), [260,250])
		#キャラクターを描画
		image,jump = drawCharacter(image,jump)
		
		#prepare for the next frame
		pygame.display.update()
		set.FPSCLOCK.tick_busy_loop(set.FPS)

		#プレイ終了
		if time > 51.20:
			return JUDGE,cloud_x,city_x

# 一時停止
def pause():
	pressKeySurf = colfon.BASICFONT.render('Press ENTER to resume.', True, colfon.DARKGRAY)
	pressKeyRect = pressKeySurf.get_rect()
	pressKeyRect.topleft = (20, set.HEIGHT - 30)
	pauseSurf = colfon.BASICFONT30.render('PAUSED.', True, colfon.DARKGRAY)
	pauseRect = pauseSurf.get_rect()
	pauseRect.center = (set.WIDTH/2, set.HEIGHT/2)
	pygame.mixer.music.pause()
	
	set.DISPLAYSURF.blit(pressKeySurf, pressKeyRect)
	set.DISPLAYSURF.blit(pauseSurf, pauseRect)
	set.refreshFrame()
	while True:
		for event in pygame.event.get(): 
			if event.key == K_RETURN:
				pygame.mixer.music.unpause()
				break
			elif event.key == K_ESCAPE:
				set.terminate()

# オブジェクトの描画
def drawHurdle(S,hurdles):
	SPEED = 21
	mtime = pygame.mixer.music.get_pos()/1000 #get music's play time
	# 右から左へ流すオブジェクトを用意する
	# ウィンドウの端からウマの前足まで約452 pixel
	if S<len(notes_time_ary) and notes_time_ary[S]-mtime<(452/(SPEED*set.FPS)): 
		if is_hurdle_ary[S]:
			rand = random.randint(0,6)
			if rand/3 == 1:
				pic = 'red'
			elif rand/2 == 1:
				pic = 'white'
			elif rand == 0:
				pic = 'mole'
			else: pic = 'yellow'
		elif not is_hurdle_ary[S]: 
			pic = 'stone'
		hurdles.append(hu.Hurdle(pic,SPEED,set.WIDTH))
		S += 1
	if hurdles: # 空でなかったら
		for h in range(len(hurdles)):
			# hurdles内のオブジェクトのxをを進める
			set.DISPLAYSURF.blit(im.IMAGEDICT[hurdles[h].pic],(hurdles[h].move(),0))
		if hurdles[0].x < -70: # ハードル画像の不透明部の幅が約70pixel
			del hurdles[0]
	return S,hurdles

# 雲を動かす
def moveCloud(cloud_x):
	cloud_x -= 0.5
	if cloud_x < -130:
		cloud_x = 700
	return cloud_x

# 背景の街並みを動かす
def moveCity(city_x):
	city_x -= 1
	if city_x < -set.WIDTH:
		city_x = 0
	return city_x

# 失敗判定
def missed(J,time,INPUT,JUDGE,DIST,image,judgement):
	if time-notes_time_ary[J]>0.25:
		if INPUT[J]==0:
			judgement = "Miss"
			JUDGE[J] = judgement
			DIST[J] = None
			INPUT[J] = None
			image = im.IMAGEDICT['bad']
			sd.MISS.play()
			J += 1
	return J,INPUT,JUDGE,DIST,image,judgement

# 
def judge(J,time,INPUT,JUDGE,DIST,image,judgement,jump):
	correctJump = True
	for j in range(J,len(notes_time_ary)):
		dist = abs(notes_time_ary[j]-time)
		if dist < 0.07:
			if is_hurdle_ary[j] and not jump['jumping']:
				correctJump = False
			elif is_hurdle_ary[j] and jump['jumping']:
				correctJump = True
			elif not is_hurdle_ary[j] and jump['jumping']:
				correctJump = False
			elif not is_hurdle_ary[j] and not jump['jumping']:
				correctJump = True
		# 
		if dist < 0.05 and correctJump:
			judgement = "Perfect!"
			JUDGE[j] = judgement
			INPUT[j] = time
			DIST[j] = dist
			sd.CORRECT.play()
			J = j+1
			break
		elif 0.05 <= dist < 0.08 and correctJump:
			judgement = "Good!"
			JUDGE[j] = judgement
			INPUT[j] = time
			DIST[j] = dist
			sd.CORRECT.play()
			J = j+1
			break
		elif 0.08 <= dist <= 0.25 or not correctJump:
			judgement = "Bad"
			JUDGE[j] = judgement
			DIST[j] = dist
			INPUT[j] = time
			image = im.IMAGEDICT['bad']
			sd.FAIL.play()
			J = j+1
			break
		#調べているnotes_time_aryと入力のtimeが遠すぎたら探索を続ける
		pygame.event.clear()
	return J,INPUT,JUDGE,DIST,image,judgement

# 
def drawCharacter(image, jump):
	JUMPRATE = 8
	JUMPHEIGHT = jump['height']
	if jump['jumping']: #ジャンプしている
		jump['y'] = jump['defY'] + math.sin((math.pi / float(JUMPRATE)) * jump['t']) * JUMPHEIGHT
		jump['t'] += 1
		if jump['t'] >= JUMPRATE:
			jump['t'] = 0
			jump['y'] = jump['defY']
			jump['jumping'] = False
		if image == im.IMAGEDICT['bad']:
			set.DISPLAYSURF.blit(image,(jump['x'], jump['defY'] - jump['y']))
		else:
			set.DISPLAYSURF.blit(im.IMAGEDICT['run1'], (jump['x'], jump['defY'] - jump['y']))
	else:
		set.DISPLAYSURF.blit(image, (jump['x'], jump['defY']))     #ジャンプしていない
	return image, jump

if __name__ == "__main__":
    main()
