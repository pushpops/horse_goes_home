class Hurdle:
	pic = ''
	x = 0
	# コンストラクタ
	def __init__(self, pic, speed, WIDTH):
		self.pic = pic
		self.speed = speed
		self.x = WIDTH
	def move(self):
		self.x -= self.speed
		return self.x
	
