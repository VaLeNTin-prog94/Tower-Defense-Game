import pygame
from pygame.math import Vector2
from settings import Settings

class Bullet(pygame.sprite.Sprite):
    """
      Класс, представляющий пулю в игре.
      Атрибуты:
          game (Game): Ссылка на объект игры, к которому принадлежит пуля.
          image (Surface): Изображение пули.
          rect (Rect): Прямоугольник, определяющий положение и размеры пули.
          position (Vector2): Вектор, представляющий текущее положение пули.
          target (Vector2): Вектор, представляющий целевую позицию, к которой движется пуля.
          speed (float): Скорость движения пули.
          damage (int): Урон, который наносит пуля.
          velocity (Vector2): Вектор скорости пули, вычисленный на основе направления к цели.
        """
    def __init__(self, start_pos, target_pos, damage, game):
        super().__init__()
        self.game = game
        self.image = pygame.image.load('assets/bullets/basic_bullet.png').convert_alpha()
        self.rect = self.image.get_rect(center=start_pos)
        self.position = Vector2(start_pos)
        self.target = Vector2(target_pos)
        self.speed = 5
        self.damage = damage
        self.velocity = self.calculate_velocity()
        self.settings = Settings()
    def calculate_velocity(self):
        '''
        Вычисляет вектор скорости пули на основе направления к цели.
        '''
        direction = (self.target - self.position).normalize()
        velocity = direction * self.speed
        return velocity

    def update(self):
        '''
        Обновляет положение пули и проверяет, достигла ли она цели или вышла за пределы экрана.
        '''
        self.position += self.velocity
        self.rect.center = self.position
        if self.position.distance_to(self.target) < 10 or not self.game.is_position_inside(self.position):
            self.kill()
        # Воспроизведение звука выстрела
        pygame.mixer.music.load(self.settings.shoot_sound)
        pygame.mixer.music.play(-1)  # Цикл музыки
    def is_position_inside(self, pos):
        '''
        Проверяет, находится ли заданная позиция внутри границ экрана игры
        .'''
        return 0 <= pos.x <= self.game.settings.screen_width and 0 <= pos.y <= self.game.settings.screen_height
