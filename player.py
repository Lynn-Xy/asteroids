import pygame
from circleshape import CircleShape
from constants import *
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, shot_group):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 180
        self.shot_group = shot_group
        self.position = pygame.Vector2(x, y)
        self.rect = pygame.Rect(0, 0, 0, 0)
        self.velocity = pygame.Vector2(0, 0)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)  # 1x1 transparent surface
        self.rect = self.image.get_rect(center=(x, y))
        self.shot_timer = 0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        x_coords = [a.x, b.x, c.x]
        y_coords = [a.y, b.y, c.y]
        self.rect = pygame.Rect(
            min(x_coords),  # Left edge
            min(y_coords),  # Top edge
            max(x_coords) - min(x_coords),  # Width
            max(y_coords) - min(y_coords),)  # Height
        return [a, b, c]
        
    def draw(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.shot_timer -= dt

        if keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_RIGHT]:
            self.rotate(dt)

        if keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_DOWN]:
            self.move(-dt)

        if keys[pygame.K_SPACE]:
            if self.shot_timer <= 0:
                self.shoot()
                self.shot_timer = PLAYER_SHOT_COOLDOWN

    def wrap(self):
        if self.position.x > SCREEN_WIDTH:
            self.position.x = 0
        elif self.position.x < 0:
            self.position.x = SCREEN_WIDTH

        # Vertical wrapping
        if self.position.y > SCREEN_HEIGHT:
           self.position.y = 0              # Wrap to top edge
        elif self.position.y < 0:            # Top edge
            self.position.y = SCREEN_HEIGHT   

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.wrap()
        self.rect.center = self.position

    def shoot(self):
        new_shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
        direction = pygame.Vector2(0, 1)
        direction = direction.rotate(self.rotation)
        new_shot.velocity = direction * PLAYER_SHOOT_SPEED
        new_shot.rotation = self.rotation
        self.shot_group.add(new_shot)