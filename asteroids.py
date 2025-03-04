import pygame, random
from constants import *
from circleshape import CircleShape

class Asteroid(CircleShape, pygame.sprite.Sprite):
    containers = None
    def __init__(self, x, y, radius):
        CircleShape.__init__(self, x, y, radius)
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.radius = radius
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius, 2)

        # Set the position and rectangle for collision and movement tracking
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius, width=2)
        
    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.center = (self.position.x, self.position.y)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            random_angle = random.uniform(20, 50)
            one = self.velocity.rotate(random_angle)
            two = self.velocity.rotate(-random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            sub_asteroid_1 = Asteroid(self.position.x, self.position.y, new_radius)
            sub_asteroid_2 = Asteroid(self.position.x, self.position.y, new_radius)
            sub_asteroid_1.velocity = one * 1.2
            sub_asteroid_2.velocity = two * 1.2