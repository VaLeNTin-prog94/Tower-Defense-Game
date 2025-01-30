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
        self.path = self.game.settings.enemy_path
        self.path_index = 0
        self.speed = speed
        self.health = health
        self.position = pygame.math.Vector2(self.path[self.path_index])
        #self.rect.center = self.position

    def take_damage(self, amount):
        ''' Уменьшает здоровье врага на заданное количество.'''
        self.health -= amount
        if self.health <= 0:
            self.kill()

    def update(self):
        '''Обновляет позицию врага, двигая его по пути'''
        if self.path_index < len(self.path) - 1:
            target_pos = pygame.math.Vector2(self.path[self.path_index + 1])
            direction = target_pos - self.position
            distance = direction.length()

            if distance > 0:
                direction = direction.normalize()
                self.position += direction * self.speed
                self.rect.center = self.position

            # Проверяем, достигли ли следующей точки маршрута
            if distance < self.speed:
                self.path_index += 1

        else:
            # Враг достиг конца пути, можно убрать его из игры
            self.kill()