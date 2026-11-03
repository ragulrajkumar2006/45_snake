import math
from array import array

import pygame
from .snake import Snake
from .food import Food

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
RED = (220, 60, 60)

class GameEngine:
    DIFFICULTIES = {
        pygame.K_1: ("Easy", 5),
        pygame.K_2: ("Medium", 8),
        pygame.K_3: ("Hard", 12),
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cell_size = 20
        self.grid_width = width // self.cell_size
        self.grid_height = height // self.cell_size

        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_title_font = pygame.font.SysFont("Arial", 56)
        self.game_over_score_font = pygame.font.SysFont("Arial", 38)
        self.game_over_prompt_font = pygame.font.SysFont("Arial", 22)
        self.menu_font = pygame.font.SysFont("Arial", 24)

        self.exit_requested = False
        self._food_sound = None
        self._game_over_sound = None
        self._audio_warning_shown = False
        self._initialize_audio()
        self.start_new_game(8)

    def _initialize_audio(self):
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

            mixer_settings = pygame.mixer.get_init()
            if mixer_settings is None:
                raise pygame.error("Pygame mixer did not initialize.")

            sample_rate, sample_format, channels = mixer_settings
            if sample_format != -16:
                raise pygame.error(f"Unsupported Pygame mixer sample format: {sample_format}")

            self._food_sound = self._create_tone((740,), 0.12, sample_rate, channels)
            self._game_over_sound = self._create_tone(
                (440, 330, 220), 0.36, sample_rate, channels
            )
        except (pygame.error, OSError) as error:
            self._disable_audio(error)

    @staticmethod
    def _create_tone(frequencies, duration, sample_rate, channels):
        samples = array("h")
        segment_length = max(1, int(sample_rate * duration / len(frequencies)))

        for frequency in frequencies:
            for index in range(segment_length):
                progress = index / segment_length
                envelope = 1 - progress
                value = int(12000 * envelope * math.sin(2 * math.pi * frequency * index / sample_rate))
                samples.extend([value] * channels)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _disable_audio(self, error):
        self._food_sound = None
        self._game_over_sound = None
        if not self._audio_warning_shown:
            print(f"Audio unavailable; continuing without sound: {error}")
            self._audio_warning_shown = True

    def _play_sound(self, sound):
        if sound is None:
            return
        try:
            sound.play()
        except (pygame.error, OSError) as error:
            self._disable_audio(error)

    def start_new_game(self, moves_per_second):
        self.snake = Snake(self.grid_width // 2, self.grid_height // 2, self.cell_size)
        self.food = Food(self.grid_width, self.grid_height, self.cell_size)
        self.score = 0
        self.moves_per_second = moves_per_second
        self._frame_counter = 0
        self.game_over = False

    def handle_keydown(self, key):
        if self.game_over:
            if key in self.DIFFICULTIES:
                _, speed = self.DIFFICULTIES[key]
                self.start_new_game(speed)
            elif key in (pygame.K_q, pygame.K_ESCAPE):
                self.exit_requested = True
            return

        if key in (pygame.K_UP, pygame.K_w):
            self.snake.set_direction(0, -1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self.snake.set_direction(0, 1)
        elif key in (pygame.K_LEFT, pygame.K_a):
            self.snake.set_direction(-1, 0)
        elif key in (pygame.K_RIGHT, pygame.K_d):
            self.snake.set_direction(1, 0)

    def handle_input(self):
        # Reserved for continuously-held-key input (not used for a
        # grid-based snake, but kept here to mirror the engine's shape).
        pass

    def update(self):
        if self.game_over:
            return

        self._frame_counter += 1
        frames_per_move = max(1, 60 // self.moves_per_second)
        if self._frame_counter < frames_per_move:
            return
        self._frame_counter = 0

        self.snake.move()

        if self.snake.collides_with_wall(self.grid_width, self.grid_height):
            self._finish_game()
            return

        if self.snake.collides_with_self():
            self._finish_game()
            return

        if self.snake.head_rect().colliderect(self.food.rect()):
            self.snake.grow()
            self.score += 1
            self.food.respawn(self.snake.body)
            self._play_sound(self._food_sound)

    def _finish_game(self):
        if self.game_over:
            return
        self.game_over = True
        self._play_sound(self._game_over_sound)

    def render(self, screen):
        # Draw food
        pygame.draw.rect(screen, RED, self.food.rect())

        # Draw snake
        for rect in self.snake.segment_rects():
            pygame.draw.rect(screen, GREEN, rect)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            title = self.game_over_title_font.render("GAME OVER", True, WHITE)
            final_score = self.game_over_score_font.render(
                f"Final Score: {self.score}", True, WHITE
            )
            prompt = self.game_over_prompt_font.render(
                "Choose a difficulty to play again", True, WHITE
            )
            easy = self.menu_font.render("1 - Easy (5 moves/sec)", True, WHITE)
            medium = self.menu_font.render("2 - Medium (8 moves/sec)", True, WHITE)
            hard = self.menu_font.render("3 - Hard (12 moves/sec)", True, WHITE)
            exit_prompt = self.menu_font.render("Q / Esc - Exit", True, WHITE)

            screen.blit(title, title.get_rect(center=(self.width // 2, self.height // 2 - 100)))
            screen.blit(final_score, final_score.get_rect(center=(self.width // 2, self.height // 2 - 45)))
            screen.blit(prompt, prompt.get_rect(center=(self.width // 2, self.height // 2 + 5)))
            screen.blit(easy, easy.get_rect(center=(self.width // 2, self.height // 2 + 45)))
            screen.blit(medium, medium.get_rect(center=(self.width // 2, self.height // 2 + 80)))
            screen.blit(hard, hard.get_rect(center=(self.width // 2, self.height // 2 + 115)))
            screen.blit(exit_prompt, exit_prompt.get_rect(center=(self.width // 2, self.height // 2 + 155)))
