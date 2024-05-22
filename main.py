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
    self.front_x = self.rect.centerx  
    self.front_y = self.rect.centery 
  def tick(self, target_x, target_y):

    self.angle = math.atan2(target_y - self.rect.centery,
                            target_x - self.rect.centerx)
    self.image = pygame.transform.rotate(
        pygame.transform.scale(pygame.image.load("Assets/Player.png"),
                               (50, 50)), -math.degrees(self.angle) + 90)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.rect.x = max(0, min(self.rect.x, 600 - self.rect.width))
    self.rect.y = max(0, min(self.rect.y, 600 - self.rect.height))
    self.front_x = self.rect.centerx + 25 * math.cos(self.angle)  # Calculate front x coordinate
    self.front_y = self.rect.centery + 25 * math.sin(self.angle)
    self.end_x = self.front_x + 50 * math.cos(self.angle)
    self.end_y = self.front_y + 50 * math.sin(self.angle)



class Projectile(pygame.sprite.Sprite):

  def __init__(self, x, y, target_x, target_y,damage):
    super().__init__()
    self.damage = damage
    self.image = pygame.image.load("Assets/Bullet.png")
    self.image = pygame.transform.scale(self.image, (15, 10))

    self.rect = self.image.get_rect()
    distance = math.sqrt((target_x - x)**2 + (target_y - y)**2)
    self.x_speed = (target_x - x) / distance * 18
    self.y_speed = (target_y - y) / distance * 18
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
      global score
      score = 0
    
      self.num = random.randint(1,4)
      if self.num == 4:
        self.type = "Big Zombie"
      else:
        self.type = "Zombie"

      if self.type == "Big Zombie":
        self.health = 190  
        self.max_health = 190 
        self.size = 75
        self.speed = random.randint(2, 5) / 2
        self.damage = 10
        self.score = 2
      else: 
        self.health = 100  
        self.max_health = 100 
        self.size = 50
        self.speed = random.randint(4, 8) / 2
        self.damage = 5
        self.score = 1

      self.attacking = False
      self.original_image = pygame.image.load("Assets/Zombie.png")
      self.original_image = pygame.transform.scale(self.original_image, (self.size, self.size))
      self.image = pygame.image.load("Assets/Zombie.png")
      self.image = pygame.transform.scale(self.image, (self.size, self.size))
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
      

  def update(self, player_rect, player_x, player_y):
      self.angle = math.atan2(player_y - self.rect.centery, player_x - self.rect.centerx)
      self.image = pygame.transform.rotate(self.original_image, -math.degrees(self.angle) + 90)
      self.player_rect = player_rect
      dx = self.player_rect.centerx - self.rect.centerx
      dy = self.player_rect.centery - self.rect.centery
      length = math.hypot(dx, dy)
      if length != 0:
          dx /= length
          dy /= length
      if self.rect.colliderect(self.player_rect):
          self.attacking = True
      else:
          self.attacking = False
          self.rect.x += dx * self.speed
          self.rect.y += dy * self.speed
      self.rect = self.image.get_rect(center=self.rect.center)
      # Kill the zombie if it reaches the player

      self.draw_health()

  def draw_health(self):
      health_bar_length = 50
      health = (self.health / self.max_health) * health_bar_length

      pygame.draw.rect(window, (0, 0, 0), (self.rect.x-5, self.rect.y - 15, health_bar_length+10, 15))
      pygame.draw.rect(window, (255, 0, 0), (self.rect.x, self.rect.y - 10, health_bar_length, 5))
      pygame.draw.rect(window, (0, 255, 0), (self.rect.x, self.rect.y - 10, health, 5))
  def take_damage(self, damage):
      self.health -= damage
      if self.health <= 0:
        global score
        score += self.score

        self.kill()

class Gun(pygame.sprite.Sprite):
  def __init__(self):
    super().__init__()
    self.ORIGINALimage = pygame.transform.scale(pygame.image.load("Assets/Guns/AK-47.png"),(66,24))
    self.image = self.ORIGINALimage
    
    self.rect = self.image.get_rect()

  def tick(self,Firing,x,y,px,py,posNFX,posNFY):
    if Firing:
      self.angle = math.atan2(py-y,px-x)
      self.image = pygame.transform.rotate(self.ORIGINALimage, -math.degrees(self.angle)+180)
      self.rect = self.image.get_rect(center=(px + 50 * math.cos(self.angle), py + 0 * math.sin(self.angle)))  # Adjust gun position slightly forward in the angle
    else:
      self.angle = math.atan2(posNFY-y,posNFX-x)+180
      self.image = pygame.transform.rotate(self.ORIGINALimage, -math.degrees(self.angle)+180)
      self.rect = self.image.get_rect(center=(posNFX + 1 * math.cos(self.angle), posNFY + 10 * math.sin(self.angle)))  # Adjust gun position slightly forward in the angle
    self.rect.x = x - 25
    self.rect.y = y - 25
    
      
      
      
  
PLAYER = Player() # Instantiate the Player sprite
GUN = Gun()

Players = pygame.sprite.Group()
Players.add(PLAYER)

Zombies = pygame.sprite.Group()
Bullets = pygame.sprite.Group()
Guns = pygame.sprite.Group()
Guns.add(GUN)

Crosshair = pygame.image.load("Assets/Crosshair.png")
Crosshair = pygame.transform.scale(Crosshair, (30, 30))

BACKGROUND = pygame.image.load("Assets/Background.png")
BACKGROUND = pygame.transform.scale(BACKGROUND,(600, 600))

cooldown = 0

SCORE = 0

FIRING = False
SPEED = 6

DAMAGE = 34

DEVMODE = False

ZombieSpawnTimer = 0

Health = 100
MaxHealth = 100
canAttack = 0

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
                                    *pygame.mouse.get_pos(),DAMAGE)
        Bullets.add(new_projectile)

  # Check for continuous key presses
  keys = pygame.key.get_pressed()
  if keys[pygame.K_0]:
    DEVMODE = True
  if keys[pygame.K_w] or keys[pygame.K_UP]:
    PLAYER.rect.y -= SPEED  # Move player up
  if keys[pygame.K_s] or keys[pygame.K_DOWN]:
    PLAYER.rect.y += SPEED  # Move player down
  if keys[pygame.K_a] or keys[pygame.K_LEFT]:
    PLAYER.rect.x -= SPEED  # Move player left
  if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
    PLAYER.rect.x += SPEED  # Move player right
  if keys[pygame.K_SPACE]:
    FIRING = True
    if cooldown < 1:
      new_projectile = Projectile(PLAYER.rect.centerx, PLAYER.rect.centery,
                                *pygame.mouse.get_pos(),DAMAGE)
      Bullets.add(new_projectile)
      cooldown = 1 if DEVMODE else 7
  else:
    FIRING = False
  cooldown -= 1

  if ZombieSpawnTimer < 1:
    if len(Zombies) < 4: 
      new_zombie = Zombie(PLAYER.rect)
      Zombies.add(new_zombie)
      ZombieSpawnTimer = random.randint(30, 60)
  else:
    ZombieSpawnTimer -= 1
      
    
  MousePos = pygame.mouse.get_pos()
    
  PLAYER.tick(MousePos[0], MousePos[1])
  Players.update()
  GUN.tick(FIRING,PLAYER.front_x,PLAYER.front_y,MousePos[0],MousePos[1],PLAYER.end_x,PLAYER.end_y)
  Guns.update()
  Bullets.update()


  for bullet in Bullets:
      zombie_hit_list = pygame.sprite.spritecollide(bullet, Zombies, False)
      for zombie in zombie_hit_list:
          bullet.kill()
          if zombie.health - bullet.damage <= 0:
              SCORE += zombie.score
          zombie.take_damage(bullet.damage)
          
  attacked = 0      
  for zombie in Zombies:
    if zombie.attacking and canAttack < 0:
      attacked = 1
      Health -= zombie.damage

  
  if attacked == 1:
    canAttack = 14   

  canAttack -= 1
    
      

  # Fill with white color
  window.fill((255, 255, 255))
  window.blit(BACKGROUND,(0,0))
  Zombies.update(PLAYER.rect,PLAYER.rect.centerx,PLAYER.rect.centery)
  Players.draw(window)
  Bullets.draw(window)
  Zombies.draw(window)
  Guns.draw(window)

  fps = int(clock.get_fps())
  fps_text = font.render(f"FPS: {fps}", True, (255, 0, 0))
  score_text = font.render(f"Score: {SCORE}", True, (255, 0, 0))
  window.blit(score_text, (10, 40))
  window.blit(fps_text, (10, 10))  # Display FPS in the top left corner
  window.blit(Crosshair, (MousePos[0] - 15, MousePos[1] - 15))
  
  pygame.draw.rect(window, (0, 0, 0), (400, 10, 190, 30))
  pygame.draw.rect(window, (255, 0, 0), (410, 20, 170, 10))
  health_width = (Health / MaxHealth) * 170
  pygame.draw.rect(window, (0, 255, 0), (410, 20, health_width, 10))
  
  if Health <= 0:
    running = False
    
  pygame.display.update()
  clock.tick(45)
pygame.quit()

sys.exit()
