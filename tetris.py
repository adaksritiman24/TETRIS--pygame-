import pygame
from pygame.locals import *
import random
import numpy as np
import time

pygame.init()
pygame.font.init()
black = (0,0,0)
width = 400
height = 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris by Sritiman Adak")

bl = [ [[0,1,0],
	    [1,1,1],
	    [0,0,0]],

	    [[0,1,0],
	    [0,1,1],
	    [0,1,0]],

	    [[0,0,0],
	     [1,1,1],
	     [0,1,0]],

		[[0,1,0],
		[1,1,0],
		[0,1,0]]
]


gl =[	[[0,0,0],
		[1,1,1],
		[0,0,0]],

		[[0,1,0],
		[0,1,0],
		[0,1,0]],

		]

el =[	[[0,0,0],
		[0,1,0],
		[0,0,0]] 
		]

	  
cl =[
		[[0,0,0],
	     [1,1,0],
	     [0,1,1]],

	     [[0,1,0],
	     [1,1,0],
	     [1,0,0]]
	
]	

dl = [
		[[0,1,1],
		[0,1,0],
		[0,1,0]],

		[[0,0,0],
		[1,1,1],
		[0,0,1]],

		[[0,1,0],
		[0,1,0],
		[1,1,0]],

		[[1,0,0],
		[1,1,1],
		[0,0,0]],
] 
hl = [

	[[0,0,0],
	[0,1,1],
	[0,1,1]]
]

ter_font = pygame.font.SysFont("lucida",40)
score_font =pygame.font.SysFont("comicsans",20)
base_height = 480
new = False
class Block:
	def __init__(self):
		self.x = 100 + 20*random.randint(0,6)
		self.y = 60
		self.width =20
		self.speed = 20
		self.b = random.choice([gl,bl,cl,dl,el,hl])
		self.index = len(self.b)-1
		self.random_index = random.randint(0,self.index)
		self.bb = self.b[self.random_index]
		self.color = (random.randint(100,255),random.randint(90,255),random.randint(80,255))
		self.setx =[]
		self.sety =[]
		self.allow =0
		self.rate = 0
		self.initialize()
	def initialize(self):	
		for m in range(3):
			for n in range(3):
				if self.bb[m][n]==1:
					self.setx.append(self.x + 20*n)
					self.sety.append(self.y + 20*m)
					self.allow+=1;	
	def reinitialize(self):
		if len(self.b)>1:
			new_x = []
			new_y = []
			al = 0
			ri =self.random_index
			ri+=1
			if ri>self.index:
				ri=0
			self.bb = self.b[ri]
			for m in range(3):
				for n in range(3):
					if self.bb[m][n]==1:
						new_x.append(self.x + 20*n)
						new_y.append(self.y + 20*m)
						al+=1;	
			yes = 0			
			for a in settled:
				for i ,j in zip(new_x, new_y):
					if((j + 20 == a[1]) and (i == a[0])):	
						yes = 1	
						break
			if yes==0:
				self.setx = new_x
				self.sety = new_y
				self.random_index = ri
				self.allow = al
			else:
				self.bb = self.b[self.random_index]	
								
	def draw(self):
		for i,j in zip(self.setx ,self.sety): 
			pygame.draw.rect(win,self.color,(i,j, self.width, self.width))

	def	move(self):
		global new
		n=0	
		for	j in self.sety:
			if j<base_height:
				n+=1;
		if n == self.allow:
			for j in range(len(self.sety)):
				self.sety[j] = self.sety[j] + 20
			self.y = self.y + 20

		else: 
			new = True	

	
	def check_collisions(self):
		global new
		for a in settled:
			for i ,j in zip(self.setx, self.sety):
				if((j +20 == a[1]) and (i == a[0])):
					new = True

	def moveleft(self):
		for x in self.setx:
			if x<= 100:
				return
		for a in settled:
			for i ,j in zip(self.setx, self.sety):
				if (a[0]+20== i) and (a[1]== j+20 or a[1] == j):
						return 
		for i in range(len(self.setx)):
			self.setx[i] = self.setx[i] -20
		if self.x>100:		
			self.x = self.x-20

			
	def moveright(self):
		for x in self.setx:
			if x> 260:
				return
		for a in settled:
			for i ,j in zip(self.setx, self.sety):
				if (i+20== a[0]) and (a[1]== j+20 or a[1]== j):
						return 
		for i in range(len(self.setx)):
			self.setx[i] = self.setx[i] +20
		if self.x<240:	
			self.x = self.x+20
			 	
			
settled = []
grid_color = (150,0,0)

over =False
def gameover():
	for a in settled:
		if a[1]<100:
			print("Game Over")
			return True
	return False				

def placed(i,j,c):
	pygame.draw.rect(win,c,(i,j,20,20))

def tetris():
	t1 = ter_font.render("TETRIS",False,(200,200,0))
	win.blit(t1,(width/2 -50, 40))

def score_board():
	t1 = score_font.render(f"Score : {score}",False,(220,200,220))
	t2 = score_font.render(f"High Score : {highscore}",False,(220,220,220))
	win.blit(t2,(5,5))
	win.blit(t1,(5,30))

def remove():
	loaf = []
	global score
	global highscore
	global settled
	new_settled = []
	r= []
	for a in settled:
		loaf.append(a[1])
	if len(loaf)>=10:
		for l in loaf:
			if loaf.count(l)==10:
				if l not in r:
					r.append(l)
		
		for a in settled:	
			if a[1] not in r:
				new_settled.append(a)
		settled = new_settled	

	if len(r)>=1:
		r.sort()
		for l in r:
			for i in range(len(settled)):
				if settled[i][1]< l:
					settled[i][1] = settled[i][1] + 20	
		score+=len(r)*10;
		if score>highscore:
			highscore+=len(r)*10	
		
def go(score):
	t1 = ter_font.render(f"Game Over",False,(250,250,250))
	t2 = ter_font.render(f"Score : {score}",False,(250,250,250))
	win.blit(t1,(width/2 -70, 200))
	win.blit(t2,(width/2 -50, 250))

def game_grid():
	for i in range(12):
		pygame.draw.rect(win,grid_color,(80+20*i,80,20,20))
		pygame.draw.rect(win,grid_color,(80+20*i,500,20,20))
	for i in range(22):	
		pygame.draw.rect(win,grid_color,(80,80+ i*20,20,20))
		pygame.draw.rect(win,grid_color,(300,80 +i*20,20,20))
	for i in range(13):
		pygame.draw.line(win,(120,120,120),(80+20*i,80),(80+20*i,520),1)
	for i in range(23):
		pygame.draw.line(win,(120,120,120),(80,80+20*i),(320,80+20*i),1)		

def new_block():
	global block
	new = False
	block = Block()
	return block

block = Block()
n =False
i=0
clk =pygame.time.Clock()

def draw_win(oc):
	global block
	global score
	global new
	global run
	global n
	global i

	win.fill((0,0,0))
	
	if oc==3:
		block.check_collisions()
		# print("h")
		if n==False:
			if not new:
				block.move()				
			if new:
				i=0
				for i,j in zip(block.setx,block.sety):
					settled.append([i,j, block.color])
				new_block()
				remove()
				if gameover():
					n=True
					settled.clear()
				new =False
		if n==True:
			go(score)	
			score = 0	
	block.draw()
	for b in settled :
		placed(b[0],b[1],b[2])		
	game_grid()	
	tetris()
	score_board()	
	pygame.time.delay(3)
	pygame.display.update()

	if n==True: 	
		time.sleep(3)
		n=False

highscore =0
score =0

def main():
	run=True
	global score
	global highscore
	score=0
	oc = 0
	while run:
		clk.tick(20)

		for event in pygame.event.get():
			if event.type==pygame.QUIT:
				run = False
			if event.type ==pygame.KEYDOWN:
				if event.key ==pygame.K_LEFT:
					block.moveleft()	

				if event.key == pygame.K_RIGHT:
					block.moveright()

				if event.key ==pygame.K_SPACE:
					block.reinitialize()	
							

		keys = pygame.key.get_pressed()
		# if keys[pygame.K_LEFT]:
		# 	block.moveleft()	

		# if keys[pygame.K_RIGHT]:
		# 	block.moveright()

		# if keys[pygame.K_SPACE]	:
		# 	block.reinitialize()
			
						
		draw_win(oc);
		oc+=1
		if oc==4:
			oc = 0	

	pygame.quit()


main()	
