import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Wino Hunter")

# Load images
player_img = pygame.image.load("police_car.png")
player_img = pygame.transform.scale(player_img, (50, 100))  # Adjusted size
beer_sprites = [
    pygame.image.load("beer1.png"),
    pygame.image.load("beer2.png"),
    pygame.image.load("beer3.png")
]  # Add more beer images if needed

# Resize beer sprites
beer_sprites = [pygame.transform.scale(beer, (50, 50)) for beer in beer_sprites]

# Load power-up image
addHealth_img = pygame.image.load("addHealth.png").convert_alpha()
addHealth_img = pygame.transform.scale(addHealth_img, (25, 25))

# Define Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.lifetime = 20
        self.speed = random.randint(1, 5)
        self.direction = random.uniform(0, 2 * math.pi)
        self.x_speed = self.speed * math.cos(self.direction)
        self.y_speed = self.speed * math.sin(self.direction)
        self.color = random.choice([LIGHT_GRAY, DARK_GRAY])  # Randomly choose color
    
    def update(self):
        self.x += self.x_speed
        self.y += self.y_speed
        self.lifetime -= 1
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

# Particle Manager class
class ParticleManager:
    def __init__(self):
        self.particles = []
    
    def generate_particles(self, x, y):
        for _ in range(20):
            particle = Particle(x, y)
            self.particles.append(particle)
    
    def update(self):
        for particle in self.particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                self.particles.remove(particle)
    
    def draw(self, screen):
        for particle in self.particles:
            particle.draw(screen)

# Initialize particle manager
particle_manager = ParticleManager()

# Player setup
player_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT - 120]
player_speed = 5
player_health = 3

# Enemy setup
enemy_speed = 5
enemy_spawn_time = 500  # milliseconds
last_enemy_spawn_time = pygame.time.get_ticks()

# Power-up setup
powerups = []
powerup_spawn_time = 10000  # 10 seconds
last_powerup_spawn_time = pygame.time.get_ticks()

# Game over setup
game_over = False
font = pygame.font.Font(None, 36)
restart_button_rect = pygame.Rect(300, 300, 200, 50)
quit_button_rect = pygame.Rect(300, 400, 200, 50)

# Score setup
score = 0

# Function to spawn enemies
def spawn_enemy(existing_enemies):
    while True:
        x_pos = random.randint(0, SCREEN_WIDTH - 50)
        enemy_img = random.choice(beer_sprites)
        enemy_rect = enemy_img.get_rect(topleft=(x_pos, 0))
        
        # Check if the new enemy overlaps with any existing enemy
        if not any(enemy_rect.colliderect(e['rect']) for e in existing_enemies):
            return {'rect': enemy_rect, 'image': enemy_img, 'current_hits': random.randint(1, 3)}

# Function to spawn power-ups
def spawn_powerup():
    x_pos = random.randint(50, SCREEN_WIDTH - 50)
    y_pos = -50  # Start just above the screen
    powerup_rect = addHealth_img.get_rect(center=(x_pos, y_pos))
    powerup_speed = random.uniform(0.55, 0.8) * enemy_speed  # Random speed between 55% to 80% of enemy_speed
    powerups.append({'rect': powerup_rect, 'speed': powerup_speed})

# Function to draw health bar
def draw_health_bar(screen, x, y, health):
    heart_img = pygame.image.load("heart.png").convert_alpha()
    heart_img = pygame.transform.scale(heart_img, (25, 25))
    for i in range(3):
        if i < health:
            screen.blit(heart_img, (x + i * 30, y))
        else:
            pygame.draw.rect(screen, BLACK, (x + i * 30, y, 25, 25), 2)

# Function to draw game over screen
def draw_game_over_screen(screen):
    screen.fill(WHITE)
    game_over_text = font.render("Game Over", True, BLACK)
    restart_text = font.render("Restart", True, BLACK)
    quit_text = font.render("Quit", True, BLACK)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, 200))
    pygame.draw.rect(screen, BLACK, restart_button_rect, 2)
    pygame.draw.rect(screen, BLACK, quit_button_rect, 2)
    screen.blit(restart_text, (restart_button_rect.x + 50, restart_button_rect.y + 10))
    screen.blit(quit_text, (quit_button_rect.x + 70, quit_button_rect.y + 10))

def restart_game():
    global game_over, score, player_health, last_enemy_spawn_time, last_powerup_spawn_time
    game_over = False
    score = 0
    player_health = 3
    last_enemy_spawn_time = pygame.time.get_ticks()
    last_powerup_spawn_time = pygame.time.get_ticks()
    powerups.clear()

# Main function
def main():
    global game_over, score, last_enemy_spawn_time, last_powerup_spawn_time, player_health

    running = True
    enemies = []
    bullets = []

    clock = pygame.time.Clock()

    while running:
        if game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if restart_button_rect.collidepoint(event.pos):
                        restart_game()
                    elif quit_button_rect.collidepoint(event.pos):
                        running = False

            draw_game_over_screen(screen)
        else:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Shoot a bullet
                        bullet = pygame.Rect(player_pos[0] + 22.5, player_pos[1], 5, 10)
                        bullets.append(bullet)

            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_pos[0] > 0:
                player_pos[0] -= player_speed
            if keys[pygame.K_RIGHT] and player_pos[0] < SCREEN_WIDTH - 50:
                player_pos[0] += player_speed
            if keys[pygame.K_UP] and player_pos[1] > 0:
                player_pos[1] -= player_speed
            if keys[pygame.K_DOWN] and player_pos[1] < SCREEN_HEIGHT - 100:
                player_pos[1] += player_speed

            # Spawn enemies
            current_time = pygame.time.get_ticks()
            if current_time - last_enemy_spawn_time > enemy_spawn_time:
                for _ in range(random.randint(1, 3)):  # Randomly spawn 1 to 3 enemies at once
                    new_enemy = spawn_enemy(enemies)
                    if new_enemy:
                        enemies.append(new_enemy)
                last_enemy_spawn_time = current_time

            # Spawn power-ups
            if current_time - last_powerup_spawn_time > powerup_spawn_time:
                spawn_powerup()
                last_powerup_spawn_time = current_time

            # Move enemies
            for enemy in enemies[:]:  # Iterate over a copy of enemies list
                enemy['rect'].y += enemy_speed
                if enemy['rect'].y > SCREEN_HEIGHT:
                    enemies.remove(enemy)

            # Move bullets
            for bullet in bullets[:]:  # Iterate over a copy of bullets list
                bullet.y -= 10
                if bullet.y < 0:
                    bullets.remove(bullet)

            # Move power-ups
            for powerup in powerups[:]:  # Iterate over a copy of powerups list
                powerup['rect'].y += powerup['speed']
                if powerup['rect'].y > SCREEN_HEIGHT:
                    powerups.remove(powerup)

            # Check for collisions
            player_rect = pygame.Rect(player_pos[0], player_pos[1], 50, 100)
            for enemy in enemies[:]:  # Iterate over a copy of enemies list
                if player_rect.colliderect(enemy['rect']):
                    particle_manager.generate_particles(enemy['rect'].centerx, enemy['rect'].centery)
                    enemies.remove(enemy)
                    player_health -= 1
                    if player_health <= 0:
                        game_over = True
                for bullet in bullets[:]:  # Iterate over a copy of bullets list
                    if bullet.colliderect(enemy['rect']):
                        bullets.remove(bullet)
                        enemy['current_hits'] -= 1
                        if enemy['current_hits'] <= 0:
                            enemies.remove(enemy)
                            score += 1
                            particle_manager.generate_particles(enemy['rect'].centerx, enemy['rect'].centery)

            # Check for power-up collision with player
            for powerup in powerups[:]:  # Iterate over a copy of powerups list
                if player_rect.colliderect(powerup['rect']):
                    if player_health < 3:
                        player_health += 1
                    powerups.remove(powerup)

            # Drawing
            screen.fill(WHITE)
            screen.blit(player_img, player_pos)
            for enemy in enemies:
                screen.blit(enemy['image'], enemy['rect'].topleft)
            for bullet in bullets:
                pygame.draw.rect(screen, BLACK, bullet)
            for powerup in powerups:
                screen.blit(addHealth_img, powerup['rect'].topleft)

            # Draw particles
            particle_manager.update()
            particle_manager.draw(screen)

            # Draw health bar
            draw_health_bar(screen, 10, 10, player_health)

            # Draw score
            score_text = font.render(f"Score: {score}", True, BLACK)
            screen.blit(score_text, (SCREEN_WIDTH - 150, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
