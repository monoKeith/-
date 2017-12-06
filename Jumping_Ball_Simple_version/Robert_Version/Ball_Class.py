import random
import pygame
from time import sleep
pygame.init()
resolution = (2560,1600)
speed_limit = 25
gravity = 0.25
ball_radius = 35
ball_number = 10
img = pygame.image.load("Robert.png")
img_res = img.get_rect().size
#bounce_border = (resolution[0]-img_res[0], resolution[1]-img_res[1])
bounce_border = (resolution[0],resolution[1])
window = pygame.display.set_mode(resolution)

class ball:

    def __init__(self, name):
        self.name = name
        self.location = (float(random.randint(0,bounce_border[0])), float(random.randint(0,bounce_border[1])))

    def random_coloring(self):
        self.color = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    #Velocity per frame, not per second.
    def initial_v(self):
        self.v = (float(random.uniform(-1*speed_limit,speed_limit)), float(random.uniform(-1*speed_limit,speed_limit)))

    def gravity(self):
        if self.location[1] < bounce_border[1] - 10:
            self.v = (self.v[0], self.v[1]+gravity)

    def refresh_location(self):
        self.location = (self.location[0]+self.v[0], self.location[1]+self.v[1])

    def show_status(self):
        print("The current location of", self.name, "is:", self.location)
        print("Velocity is:", self.v)
        #print("Color is:   ", self.color)

    def bounce(self):
        #When the x exceed from resolution
        if not 0 <= self.location[0] <= bounce_border[0]:
            self.random_coloring()
            self.v = (-1*self.v[0], self.v[1])
            #Bounce energy efficiency
            if abs(self.v[0]) > 0 :
                self.v = (self.v[0]*0.95, self.v[1])
            #print("Ball",self.name,"bounced!")
        #When the y exceed from resolution
        elif not 0 <= self.location[1] <= bounce_border[1]:
            self.random_coloring()
            self.v = (self.v[0], -1*self.v[1])
            #Bounce energy efficiency
            if abs(self.v[1]) > 0 :
                self.v = (self.v[0], self.v[1]*0.95)
            #print("Ball",self.name,"bounced!")

    def dim_color(self):
        if self.color[0] < 255:
            self.color = (self.color[0]+1, self.color[1], self.color[2])
        if self.color[1] < 255:
            self.color = (self.color[0], self.color[1]+1, self.color[2])
        if self.color[2] < 255:
            self.color = (self.color[0], self.color[1], self.color[2]+1)

    def keep_inside(self):
        if self.location[0] > bounce_border[0]:
            self.location = (bounce_border[0], self.location[1])
        elif self.location[0] < 0 :
            self.location = (0, self.location[1])
        if self.location[1] > bounce_border[1]:
            self.location = (self.location[0], bounce_border[1])
        elif self.location[1] < 0 :
            self.location = (self.location[0], 0)

    def air_resistance(self):
        self.v = (self.v[0]*0.999, self.v[1]*0.999)


def main():
    ball_list = []
    
    for i in range(ball_number):
        ball_list.append(ball(i))
        ball_list[i].random_coloring()
        ball_list[i].initial_v()
    notexit = True
    while notexit:
        window.fill((232,237,236))
        window.blit(img, ((resolution[0]-img_res[0])//2,(resolution[1]-img_res[1])//2))
        for thisball in ball_list:
            #ball_list[i].air_resistance()
            thisball.bounce()
            thisball.gravity()
            thisball.keep_inside()
            thisball.refresh_location()
            thisball.dim_color()
            #window.blit(img, (int(thisball.location[0]), int(thisball.location[1])))
            pygame.draw.circle(window, thisball.color, (int(thisball.location[0]), int(thisball.location[1])), ball_radius)

        pygame.display.update()
        #sleep(0.01)
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                notexit = False

main()
