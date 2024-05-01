import pygame
import sys
import math
import os

pygame.init()

# Create a Pygame window
window = pygame.display.set_mode((500, 500))
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
    self.rect.x = 250 - 25
    self.rect.y = 250 - 25

  def tick(self, target_x, target_y):
    self.angle = math.atan2(target_y - self.rect.centery,
                            target_x - self.rect.centerx)
    self.image = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load("Assets/Player.png"),
                               (50, 50)), -math.degrees(self.angle) + 90)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.rect.x = max(0, min(self.rect.x, 500 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 500 - self.rect.height))


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
    if self.rect.x < 0 or self.rect.x > 500 or self.rect.y < 0 or self.rect.y > 500:
      self.kill()


PLAYER = Player()  # Instantiate the Player sprite

Players = pygame.sprite.Group()
Players.add(PLAYER)

Bullets = pygame.sprite.Group()

Crosshair = pygame.image.load("Assets/Crosshair.png")
Crosshair = pygame.transform.scale(Crosshair, (30, 30))

cooldown = 0

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
    PLAYER.rect.y -= 5  # Move player up
  if keys[pygame.K_s] or keys[pygame.K_DOWN]:
    PLAYER.rect.y += 5  # Move player down
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    PLAYER.rect.x -= 5  # Move player left
  if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    PLAYER.rect.x += 5  # Move player right
  if keys[pygame.K_SPACE] and cooldown < 1:

    new_projectile = Projectile(PLAYER.rect.centerx, PLAYER.rect.centery,
                                *pygame.mouse.get_pos())
    Bullets.add(new_projectile)
    cooldown = 10

  cooldown -= 1

  MousePos = pygame.mouse.get_pos()
  PLAYER.tick(MousePos[0], MousePos[1])
  Players.update()
  Bullets.update()

  # Fill with white color
  window.fill((255, 255, 255))

  Players.draw(window)
  Bullets.draw(window)

  fps = int(clock.get_fps())
  fps_text = font.render(f"FPS: {fps}", True, (255, 0, 0))
  window.blit(fps_text, (10, 10))  # Display FPS in the top left corner
  window.blit(Crosshair, (MousePos[0] - 15, MousePos[1] - 15))

  pygame.display.update()
  clock.tick(30)

pygame.quit()
sys.exit()
