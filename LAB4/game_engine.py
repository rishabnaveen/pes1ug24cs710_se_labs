import pygame
import random
from .player import Player
from .enemy import EnemyGrid
from .bullet import Bullet

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)
GRAY = (200, 200, 200)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.font = pygame.font.SysFont("Arial", 28)
        self.large_font = pygame.font.SysFont("Arial", 50, bold=True)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.reset()

    def reset(self):
        """Resets the game state for a new game or restart."""
        self.player = Player(self.width // 2 - 20, self.height - 50, 40, 20)
        self.enemy_grid = EnemyGrid(self.width)

        self.player_bullets = []
        self.enemy_bullets = []
        self._shoot_cooldown = 0
        self.enemy_fire_chance = 0.01

        self.score = 0
        self.game_over = False
        self.game_won = False

    def handle_event(self, event):
        # Allow restarting or quitting from the Game Over / Win screen
        if self.game_over or self.game_won:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.reset()
                elif event.key == pygame.K_q:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if self._shoot_cooldown <= 0:
                bullet_x = self.player.center_x() - 2
                self.player_bullets.append(Bullet(bullet_x, self.player.y, direction=-1))
                self._shoot_cooldown = 15

    def handle_input(self):
        if self.game_over or self.game_won:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move(-self.player.speed, self.width)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move(self.player.speed, self.width)

    def update(self):
        if self.game_over or self.game_won:
            return

        if self._shoot_cooldown > 0:
            self._shoot_cooldown -= 1

        self.enemy_grid.move()

        # Check Win Condition (all enemies destroyed)
        if len(self.enemy_grid.alive_enemies()) == 0:
            self.game_won = True
            return

        # Enemy random shooting
        for enemy in self.enemy_grid.alive_enemies():
            if random.random() < self.enemy_fire_chance:
                bullet_x = enemy.x + enemy.width // 2
                self.enemy_bullets.append(Bullet(bullet_x, enemy.y + enemy.height, direction=1))

        # Move bullets
        for bullet in self.player_bullets:
            bullet.move()
        for bullet in self.enemy_bullets:
            bullet.move()

        # Clean off-screen bullets
        self.player_bullets = [b for b in self.player_bullets if not b.off_screen(self.height)]
        self.enemy_bullets = [b for b in self.enemy_bullets if not b.off_screen(self.height)]

        # --- Task 1 Fix: Safe Collision Detection ---
        # Instead of modifying self.player_bullets during iteration,
        # we track bullets to remove to prevent skipping subsequent checks.
        bullets_to_remove = set()
        for bullet in self.player_bullets:
            bullet_rect = bullet.rect()
            for enemy in self.enemy_grid.alive_enemies():
                if enemy.alive and bullet_rect.colliderect(enemy.rect()):
                    enemy.alive = False
                    bullets_to_remove.add(bullet)
                    self.score += 1
                    break

        self.player_bullets = [b for b in self.player_bullets if b not in bullets_to_remove]

        # Enemy bullet hits player
        for bullet in self.enemy_bullets:
            if bullet.rect().colliderect(self.player.rect()):
                self.game_over = True
                break

        # Enemies reach bottom
        if self.enemy_grid.reached_bottom(self.player.y):
            self.game_over = True

    def render(self, screen):
        # Draw Player
        pygame.draw.rect(screen, GREEN, self.player.rect())

        # Draw Enemies
        for enemy in self.enemy_grid.alive_enemies():
            pygame.draw.rect(screen, WHITE, enemy.rect())

        # Draw Bullets
        for bullet in self.player_bullets:
            pygame.draw.rect(screen, WHITE, bullet.rect())
        for bullet in self.enemy_bullets:
            pygame.draw.rect(screen, RED, bullet.rect())

        # Draw In-game Score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # --- Task 2: Game Over / Victory Screen ---
        if self.game_over or self.game_won:
            # Semi-transparent dark overlay
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            screen.blit(overlay, (0, 0))

            if self.game_over:
                title_text = self.large_font.render("GAME OVER", True, RED)
            else:
                title_text = self.large_font.render("YOU WIN!", True, GREEN)

            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            restart_text = self.small_font.render("Press 'R' to Restart  |  'Q' to Quit", True, GRAY)

            # Center text on screen
            screen.blit(title_text, title_text.get_rect(center=(self.width // 2, self.height // 2 - 60)))
            screen.blit(final_score_text, final_score_text.get_rect(center=(self.width // 2, self.height // 2)))
            screen.blit(restart_text, restart_text.get_rect(center=(self.width // 2, self.height // 2 + 50)))