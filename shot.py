import pygame
from circleshape import CircleShape
from constants import *

class Shot(CircleShape, pygame.sprite.Sprite):
    def __init__(self, x, y, SHOT_RADIUS):
        CircleShape.__init__(self, x, y, SHOT_RADIUS)
        self.radius = SHOT_RADIUS
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 255, 255), (self.radius, self.radius), self.radius, 2)
        self.rect = self.image.get_rect(center=(round(self.position.x), round(self.position.y)))

    def update(self, dt):
        self.position.x += self.velocity.x * dt
        self.position.y += self.velocity.y * dt
        self.rect.centerx = round(self.position.x)
        self.rect.centery = round(self.position.y)

        if (self.position.x < -self.radius or self.position.x > SCREEN_WIDTH + self.radius or self.position.y < -self.radius or self.position.y > SCREEN_HEIGHT + self.radius):
            self.kill()