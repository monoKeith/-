#This is a really simple physical engine built for simulating collisions of balls.
#The goal is making balls collide with each other, not just collide with the border.
#One second is condisered as 100 frame, one meter is considered as 100 pixel, for the simulations.
#The unit of length is cm [Pixel], unit of velocity is cm/s [Pixel per 100 frames], unit of accleration is cm/s^2 [Pixel per 100 frames square].

#Import libraries
import pygame
import random
import math
from time import sleep

#Initialize global variables:
resolution = (2560, 1600)       #Resolution of the pygame window.
margin = 30                     #margin between the border of the window.
speed_limit = (100, 150)           #Minimum velocity and Maximum velocity for random_velocity generating.
gravity_a = 490                 #Gravity acceleration, unit is Newtons/kg.
air_resist = 1                  #The multiplier to create air resistance per frame
bounce_efficiency = 1           #The multiplier to simulate energy loss during per bounce
ball_radius = 25                #The radius of each ball.
ball_amount = 10                #The amount of balls.
ball_weight = 1                 #The weight for each ball, unit is kg.
#Calculate the react area by using provided resolution and margins (x_min,y_min,x_max,y_max).
react_area = (margin, margin, resolution[0] - margin, resolution[1] - margin)
class motion:
    """ball oriented class"""
    def __init__(self, ball_id):
        self.id = ball_id
        #Assign location for this ball
        self.location = (random.uniform(react_area[0], react_area[2]), random.uniform(react_area[1],react_area[3]))
        self.d_location = (self.location[0], self.location[1])
        self.velocity = (0,0)
        self.weight = ball_weight
        self.colour = (255,255,255)

    #Assign random color for this ball
    def random_colour(self):
        self.colour = (random.randint(0,255),random.randint(0,255),random.randint(0,255))

    #Assign speed of the object with the preset limits
    def random_velocity(self):
        self.velocity = (random.choice([-1,1]) * random.uniform(speed_limit[0], speed_limit[1]), random.choice([-1,1]) * random.uniform(speed_limit[0], speed_limit[1]))

    #Refresh the location by using previous location and the velocity (pixel per 100 frame)
    def refresh_location(self):
        #See if the ball is going to exceed react_area at the next frame
        predict_x, predict_y = self.location[0] + (self.velocity[0] / 100), self.location[1] + (self.velocity[1] / 100)
        #If the ball is not going to bounce in the next frame, proceed the location normally.
        if (react_area[0] < predict_x < react_area[2]) and (react_area[1] < predict_y < react_area[3]):
            self.location = (predict_x, predict_y)
        else:
            #When the predict location is outsode of the react area, perform bounce affect. When bounced, change colour!
            self.random_colour()
            x_reversed = False
            if not react_area[0] < predict_x < react_area[2] :
                x_reversed = True
                if predict_x < react_area[0] :
                    self.location = (2 * react_area[0] - predict_x ,predict_y)
                else:
                    self.location = (2 * react_area[2] - predict_x ,predict_y)
                self.velocity = (-1 * self.velocity[0] * bounce_efficiency, self.velocity[1])
            if not react_area[1] < predict_y < react_area[3] :
                if x_reversed:
                    if predict_y < react_area[1] :
                        self.location = (self.location[0], 2 * react_area[1] - predict_y)
                    else:
                        self.location = (self.location[1], 2 * react_area[3] - predict_y)
                else:
                    if predict_y < react_area[1] :
                        self.location = (predict_x, 2 * react_area[1] - predict_y)
                    else:
                        self.location = (predict_x, 2 * react_area[3] - predict_y)
                self.velocity = (self.velocity[0], -1 * self.velocity[1] * bounce_efficiency)


    #Changing the velocity by the affect of gravitational force
    def gravity(self):
        self.velocity = (self.velocity[0], self.velocity[1] + (gravity_a / 100))

    #Multiplying a value to the velocity to simulate air resistance
    def air_resistance(self):
        self.velocity = (self.velocity[0] * air_resist, self.velocity[1] * air_resist)

    #Changing the location in integer
    def refresh_dl(self):
        self.d_location = (int(self.location[0]), int(self.location[1]))


def main():
    ball_list, running_sign = [], True
    #Gererate a list that contains all the balls
    for ball_id in range(ball_amount):
        ball_list.append(motion(ball_id))
    #Adding initial informations to each ball
    for ball in ball_list:
        ball.random_colour()
        ball.random_velocity()
    #Initialize pygame
    pygame.init()
    py_window = pygame.display.set_mode(resolution)
    py_window.fill((255,255,255))
    #Loop simulating motions
    while running_sign:
        for ball in ball_list:
            ball.gravity()
            ball.air_resistance()
            ball.refresh_location()
            ball.refresh_dl()
            #Draw object on pygame window
            pygame.draw.circle(py_window, ball.colour, ball.d_location, ball_radius)
        #Update display and refresh
        pygame.display.update()
        #py_window.fill((0,0,0))
        #Detect for exit button signals
        for event in pygame.event.get() :
            if event.type == pygame.QUIT:
                running_sign = False

main()
