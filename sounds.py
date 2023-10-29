import pygame
# 効果音を読み込み、音量を設定
CORRECT = pygame.mixer.Sound("se/correct.wav")
CORRECT.set_volume(0.1)
JUMP = pygame.mixer.Sound("se/Motion-pop15-1.wav")
FAIL = pygame.mixer.Sound("se/fail.wav")
FAIL.set_volume(0.3)
MISS = pygame.mixer.Sound("se/match4.wav")
MISS.set_volume(0.2)
DRUM = pygame.mixer.Sound("se/Quiz-Results01-2.wav")
CLEAR = pygame.mixer.Sound("se/Shortbridge02-1.wav")