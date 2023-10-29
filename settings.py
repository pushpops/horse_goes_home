import pygame
import sys

# 画面サイズ
WIDTH = 700
HEIGHT = 500
# flame per second
FPS = 30
# 画面を生成
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
FPSCLOCK = pygame.time.Clock()
# フレームを新しくする
def refreshFrame():
	pygame.event.get() 
	pygame.display.update()
	FPSCLOCK.tick(set.FPS)
	
# ゲームの終了
def terminate():
    pygame.quit()
    sys.exit()