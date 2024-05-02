import math
import os
import random
import sys

import pygame

pygame.init()

# Create a Pygame window
window = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Shooter")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()


# Define a sprite class
class Player(pygame.sprite.Sprite):

  def __init__(self):
    super().__init__()
    self.image = pygame.image.load("Assets/Player.png")
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.rect = self.image.get_rect()
    self.rect.x = 300 - 25
    self.rect.y = 300 - 25

  def tick(self, target_x, target_y):
    self.angle = math.atan2(target_y - self.rect.centery,
                            target_x - self.rect.centerx)
    self.image = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load("Assets/Player.png"),
                               (50, 50)), -math.degrees(self.angle) + 90)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.rect.x = max(0, min(self.rect.x, 600 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))


class Projectile(pygame.sprite.Sprite):

  def __init__(self, x, y, target_x, target_y):
    super().__init__()
    self.image = pygame.image.load("Assets/Bullet.png")
    self.image = pygame.transform.scale(self.image, (15, 10))

    self.rect = self.image.get_rect()
    distance = math.sqrt((target_x - x)**2 + (target_y - y)**2)
    self.x_speed = (target_x - x) / distance * 15
    self.y_speed = (target_y - y) / distance * 15
    self.rect.center = (x + self.x_speed * 2, y + self.y_speed * 2)
    self.angle = math.atan2(target_y - self.rect.centery,
                            target_x - self.rect.centerx)
    self.image = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load("Assets/Bullet.png"),
                               (20, 10)), -math.degrees(self.angle))
    self.rect = self.image.get_rect(center=self.rect.center)

  def update(self):
    self.rect.x += self.x_speed
    self.rect.y += self.y_speed
    if self.rect.x < 0 or self.rect.x > 600 or self.rect.y < 0 or self.rect.y > 600:
      self.kill()


class Zombie(pygame.sprite.Sprite):

  def __init__(self, player_rect):
    super().__init__()
    self.speed = random.randint(4, 9) / 2
    self.original_image = pygame.image.load("Assets/Zombie.png")
    self.original_image = pygame.transform.scale(self.original_image,(50,50))
    self.image = pygame.image.load("Assets/Zombie.png")
    self.image = pygame.transform.scale(self.image, (50, 50))
    self.rect = self.image.get_rect()
    # Spawn zombie on a random edge of the screen
    self.spawn_edge = random.choice(["top", "bottom", "left", "right"])
    if self.spawn_edge == "top":
      self.rect.x = random.randint(0, 600)
      self.rect.y = -50
    elif self.spawn_edge == "bottom":
      self.rect.x = random.randint(0, 600)
      self.rect.y = 600
    elif self.spawn_edge == "left":
      self.rect.x = -50
      self.rect.y = random.randint(0, 600)
    elif self.spawn_edge == "right":
      self.rect.x = 600
      self.rect.y = random.randint(0, 600)
    self.player_rect = player_rect

  def update(self, player_rect,player_x,player_y):

    self.angle = math.atan2(player_y - self.rect.centery,
      player_x - self.rect.centerx)
    self.image = pygame.transform.rotate(self.original_image, -math.degrees(self.angle)+90)
    self.player_rect = player_rect
    dx = self.player_rect.centerx - self.rect.centerx
    dy = self.player_rect.centery - self.rect.centery
    length = math.hypot(dx, dy)
    if length != 0:
      dx /= length
      dy /= length
    if self.rect.colliderect(self.player_rect):
      pass
    else:  
      self.rect.x += dx * self.speed
      self.rect.y += dy * self.speed
    self.rect = self.image.get_rect(center=self.rect.center)
    # Kill the zombie if it reaches the player



PLAYER = Player()  # Instantiate the Player sprite

Players = pygame.sprite.Group()
Players.add(PLAYER)

Zombies = pygame.sprite.Group()
Bullets = pygame.sprite.Group()

Crosshair = pygame.image.load("Assets/Crosshair.png")
Crosshair = pygame.transform.scale(Crosshair, (30, 30))

cooldown = 0

SPEED = 5

os.system("clear")
print('''    CONTROLS
  WASD keys or arrow keys to move
  Space bar or click the mouse to shoot
  Move the mouse to aim''')

running = True
while running:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.MOUSEBUTTONDOWN:
      if event.button == 1:  # Left mouse button
        new_projectile = Projectile(PLAYER.rect.centerx, PLAYER.rect.centery,
                                    *pygame.mouse.get_pos())
        Bullets.add(new_projectile)

  # Check for continuous key presses
  keys = pygame.key.get_pressed()
  if keys[pygame.K_w] or keys[pygame.K_UP]:
    PLAYER.rect.y -= SPEED  # Move player up
  if keys[pygame.K_s] or keys[pygame.K_DOWN]:
    PLAYER.rect.y += SPEED  # Move player down
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    PLAYER.rect.x -= SPEED  # Move player left
  if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    PLAYER.rect.x += SPEED  # Move player right
  if keys[pygame.K_SPACE] and cooldown < 1:
    new_projectile = Projectile(PLAYER.rect.centerx, PLAYER.rect.centery,
                                *pygame.mouse.get_pos())
    Bullets.add(new_projectile)
    cooldown = 10

  cooldown -= 1

  if len(Zombies) < 3:  # Spawn up to 5 zombies
    new_zombie = Zombie(PLAYER.rect)
    Zombies.add(new_zombie)
  MousePos = pygame.mouse.get_pos()
  PLAYER.tick(MousePos[0], MousePos[1])
  Players.update()
  Bullets.update()
  Zombies.update(PLAYER.rect,PLAYER.rect.centerx,PLAYER.rect.centery)

  for bullet in Bullets:
    zombie_hit_list = pygame.sprite.spritecollide(bullet, Zombies, True)
    for zombie in zombie_hit_list:
      bullet.kill()

  # Fill with white color
  window.fill((255, 255, 255))

  Players.draw(window)
  Bullets.draw(window)
  Zombies.draw(window)

  fps = int(clock.get_fps())
  fps_text = font.render(f"FPS: {fps}", True, (255, 0, 0))
  window.blit(fps_text, (10, 10))  # Display FPS in the top left corner
  window.blit(Crosshair, (MousePos[0] - 15, MousePos[1] - 15))

  pygame.display.update()
  clock.tick(30)

pygame.quit()
sys.exit()
