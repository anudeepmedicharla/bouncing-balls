import math
import pygame
import random

__author__ = 'anudeep'


def round1(var,limit):
    count=0
    var=str(var)
    return_var=''
    for i in range(len(var)):
        return_var+=var[i]
        if var[i]=='.':
            count=limit+1
        if count>0:
            count-=1
            if count==0:
                break

    return float(return_var)


class Particle(object):
    color = (0, 0, 255)  # color of the ball

    def __init__(self, (x, y), size):
        self.size = size
        (self.x, self.y) = (x, y)
        self.y_initial = self.y  # just for reference, store the initial value of y

        self.gravity = 0.8  # gravity is always downwards so no need of angle,it is always pi/2
        self.angle = random.uniform(0, math.pi)
        self.velocity = random.randint(0,20)
        # ....split velocity into component vectors ....
        self.velocity_x = round1(math.cos(self.angle) * self.velocity, 2)  # velocity at t=0
        self.velocity_y = round1(math.sin(self.angle) * self.velocity,2)  # velocity at t=0
        self.elasticity = 0.9
        self.refer = 0
        self.adjustment = 0
        self.friction=0.99

    def move(self):
        # self.velocity_x = round1(math.cos(self.angle)*self.velocity, 2)
        # self.velocity_y = round1(math.sin(self.angle) * self.velocity, 2)
        self.velocity_y+=self.gravity
        self.velocity=math.hypot(self.velocity_x,self.velocity_y)
        self.x += round1(self.velocity_x,2)
        self.y += round1(self.velocity_y,2)

        if self.x > width - self.size:
            self.x=width-self.size
            self.angle = math.pi - self.angle  # angle after collision
            self.velocity_x = round1(-self.elasticity * self.velocity_x, 2)
        elif self.x < self.size:
            self.x = self.size
            self.angle = math.pi - self.angle  # angle after collision
            self.velocity_x = round1(-self.elasticity * self.velocity_x, 2)
        if self.y > height - self.size:
            self.y = height - self.size
            self.angle = 2 * math.pi - self.angle  # angle after collision
            self.velocity_y = round1(-self.elasticity * self.velocity_y, 2)
            if self.y+round1(self.velocity_y+self.gravity,2)>height-self.size:
                self.velocity_y=0
                self.velocity_x = round1(self.friction*self.velocity_x,2)
        elif self.y < self.size:
            self.y = self.size
            self.angle = 2 * math.pi - self.angle  # angle after collision
            self.velocity_y = -self.velocity_y

        # print 'self.y,self.x,velocity_y,velocity_x', self.y, self.x, self.velocity_y, self.velocity_x

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


if __name__ == '__main__':
    elasticity=0.9

    def collide(p1,p2):
        dx=p1.x-p2.x
        dy=p1.y-p2.y
        distance= math.hypot(dx,dy)  # similar to math.sqrt(dx**2+dy**2)
        if distance<p1.size+p2.size:
            net_distance=p1.size+p2.size-distance
            tangent = math.atan2(dy, dx)
            p1.x+=round1(math.cos(tangent)*net_distance,2)
            p1.y+=round1(math.sin(tangent)*net_distance,2)
            if p1.x>width-size:
                    p1.x=width-size
            if p1.x<size:
                    p1.x=size
            if p1.y>height-size:
                    p1.y=height-size
            if p1.y<size:
                    p1.y=size

            """(p1.velocity_x,p2.velocity_x)=(p2.velocity_x,p1.velocity_x)
            (p1.velocity_y,p2.velocity_y)=(p2.velocity_y,p1.velocity_y)"""

            p1_along_intersection=p1.velocity_x*math.cos(tangent)+p1.velocity_y*math.sin(tangent)
            p1_along_tangent=p1.velocity_x*math.sin(tangent)-p1.velocity_y*math.cos(tangent)
            p2_along_intersection=p2.velocity_x*math.cos(tangent)+p2.velocity_y*math.sin(tangent)
            p2_along_tangent=p2.velocity_x*math.sin(tangent)-p2.velocity_y*math.cos(tangent)
            p1_temp=p2_along_intersection
            p2_temp=p1_along_intersection

            p1.velocity_x=round1(elasticity*(p1_temp*math.cos(tangent)+p1_along_tangent*math.sin(tangent)),2)
            p1.velocity_y=round1(elasticity*(p1_temp*math.sin(tangent)+p1_along_tangent*math.cos(tangent)),2)
            p2.velocity_x=round1(elasticity*(p2_temp*math.cos(tangent)+p2_along_tangent*math.sin(tangent)),2)
            p2.velocity_y=round1(elasticity*(p2_temp*math.sin(tangent)+p2_along_tangent*math.cos(tangent)),2)
            # print "p1.velocity_x,p1.velocity_y",p1.velocity_x,p1.velocity_y
            # print "p2.velocity_x,p2.velocity_y",p2.velocity_x,p2.velocity_y


    def findparticle(particles, x, y):
        for p in particles:
            if math.hypot(p.x - x, p.y - y) <= p.size:
                return p

    selected_particle = None
    mouse_x_prev = 0
    mouse_y_prev = 0
    speed_x = 0
    speed_y = 0
    running = True
    background1_color = (255, 255, 255)  # white
    no_of_particles = 7
    my_particles = []
    (width, height) = (640, 480)
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('gravity ball')

    for n in range(no_of_particles):
        x = random.randint(0, width)
        y = 100  # random.randint(0,height)
        size = 20  # random.randint(0,30)
        my_particles.append(Particle((x, y), size))

    while running:

        for i, particle in enumerate(my_particles):
            if particle != selected_particle:
                particle.move()
            for particle2 in my_particles[i+1:]:
                collide(particle,particle2)
            particle.draw()

        pygame.display.update()
        screen.fill(background1_color)  # fill the window with background1 color
        # pygame.time.delay(90)

        clock.tick(60)  # force pygame for 60fps

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # when pressed close button,quit
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # print 'mouse', mouse_x, mouse_y
                selected_particle = findparticle(my_particles, mouse_x, mouse_y)
            elif event.type == pygame.MOUSEBUTTONUP:
                selected_particle = None
                mouse_x_prev = 0
                mouse_y_prev = 0
                # print "Button up", speed_x, speed_y
            if selected_particle:
                selected_particle.color = (152, 245, 164)
                mouse_x, mouse_y = pygame.mouse.get_pos()
                """for calculating the speed of the mouse movement
                (to transfer the same speed to the particle when released)"""
                speed_x = mouse_x - mouse_x_prev
                speed_y = mouse_y - mouse_y_prev
                mouse_x_prev = mouse_x
                mouse_y_prev = mouse_y

                selected_particle.x = mouse_x
                selected_particle.y = mouse_y
                # set boundaries for the selected particle
                if selected_particle.x>width-size:
                    selected_particle.x=width-size
                if selected_particle.x<size:
                    selected_particle.x=size
                if selected_particle.y>height-size:
                    selected_particle.y=height-size
                if selected_particle.y<size:
                    selected_particle.y=size
                # detect collision with other particles
                lst=[i for i in my_particles if i!=selected_particle]
                for i in lst:
                    collide(i,selected_particle)

                if speed_x != mouse_x:
                    selected_particle.velocity_x = speed_x
                if speed_y != mouse_y:
                    selected_particle.velocity_y = speed_y
                # print speed_x, speed_y
