import pygame
from pygame.math import Vector2


class Enemy(pygame.sprite.Sprite):
    '''
    Класс, представляющий врага в игре.
    Атрибуты:
        game (Game): Ссылка на объект игры, к которому принадлежит враг.
        image (Surface): Изображение врага.
        rect (Rect): Прямоугольник, определяющий положение и размеры врага.
        path (list): Список координат, по которым движется враг.
        path_index (int): Индекс текущей точки на пути.
        speed (float): Скорость движения врага.
        health (int): Здоровье врага.
        position (Vector2): Вектор, представляющий текущее положение врага.
    '''
    def __init__(self, path, speed=2, health=10, image_path=None, game = None):

        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image = pygame.image.load(image_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.game = game
        self.path = path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.position = Vector2(path[0])
        self.rect.center = self.position

    def take_damage(self, amount):
        ''' Уменьшает здоровье врага на заданное количество.'''
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        '''Обновляет положение врага по пути и проверяет, достиг ли он конца пути.'''
        if self.path_index < len(self.path) - 1:
            start_point = Vector2(self.path[self.path_index])
            end_point = Vector2(self.path[self.path_index + 1])
            direction = (end_point - start_point).normalize()

            self.position += direction * self.speed
            self.rect.center = self.position

            if self.position.distance_to(end_point) < self.speed:
                self.path_index += 1

            if self.path_index >= len(self.path) - 1:
                self.game.game_over()
                self.kill()
