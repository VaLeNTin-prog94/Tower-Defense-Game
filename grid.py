import pygame


class Grid:
    '''Класс для управления сеткой в игре Tower Defense.

    Атрибуты:
        game (Game): Ссылка на объект игры, который содержит настройки и экран.
        settings (Settings): Настройки игры, включая позиции башен и размер ячейки.
        screen (Surface): Экран Pygame, на котором будет рисоваться сетка.
        available_spots (list): Список доступных координат для размещения башен.
        towers (list): Список размещенных башен.
    '''
    def __init__(self, game):
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.available_spots = self.settings.tower_positions
        self.towers = []

    def update(self):
        '''Обновляет состояние сетки. Метод требует реализации в будущем.'''
        pass

    def draw(self, screen):
        '''
        Рисует сетку и доступные позиции на экране
        :param screen: Экран, на котором будет нарисована сетка.
        '''
        for pos in self.game.settings.tower_positions:
            pygame.draw.circle(self.screen, (128, 0, 0), pos, 10)
        for spot in self.available_spots:
            pygame.draw.circle(self.screen, (255, 255, 255), spot, 15, 2)

    def place_tower(self, tower=None):
        '''
        Размещает башню на сетке, если это возможно
        :param tower:Объект башни, который нужно разместить.
        '''
        grid_pos = self.get_grid_position(tower.position)
        if grid_pos in self.available_spots and not any(tower.rect.collidepoint(grid_pos) for tower in self.towers):
            self.towers.append(tower)
            return True
        return False

    def remove_tower(self, tower):
        '''
        Удаляет башню из сетки, если она существует
        :param tower: Объект башни, который нужно удалить.
        '''
        if tower in self.towers:
            self.towers.remove(tower)

    def get_grid_position(self, mouse_pos):
        '''
        Получаем координаты клетки сетки по положению мыши
        :param mouse_pos (tuple): координаты мыши (x, y).
        :return:
        '''

        grid_x = mouse_pos[0] // 64 * 64 + 32
        grid_y = mouse_pos[1] // 64 * 64 + 32
        return grid_x, grid_y

    def is_spot_available(self, grid_pos):
        '''Проверяет, доступна ли позиция для размещения башни.'''
        return grid_pos in self.available_spots and all(not tower.rect.collidepoint(grid_pos) for tower in self.towers)
