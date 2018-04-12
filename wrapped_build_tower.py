# coding: utf-8
import random

import pygame
import sys
import build_tower_utils
import numpy as np

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BRIGHT_RED = (255, 25, 25)
SKY = (78, 192, 202)
GROUND = (224, 215, 146)
DARK_GROUND = (124, 115, 46)
TOWER = (117, 190, 49)
WALL = (239, 177, 33)
RED_WALL = (255, 0, 0)

WIDTH, HEIGHT = 480, 600
TIME_FOR_ONE_TRUE = 20
EVERY_BRICK_WIDTH = 16

pygame.init()

# font
arial18 = pygame.font.SysFont('arial', 18, False, False)
arial30 = pygame.font.SysFont('arial', 30, True, False)
arial35 = pygame.font.SysFont('arial', 35, True, True)

size = (WIDTH, HEIGHT)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Build Tower!")
clock = pygame.time.Clock()

SOUNDS, IMAGES_BKG = build_tower_utils.load_resource()


class BuildTower():
    def __init__(self):
        self.score = 0
        # 墙体的砖块数，最多是10
        self.brick_num = 10
        # 放置的状态。1为normal放置，2为good放置，3为perfect放置，0为还未放置，-1为放置失败
        self.status = 0
        # 放置状态的字符串
        self.evaluation = ""

        # 无需播放音乐
        # self.dead_flag = True
        self.wall = Wall(self)
        self.towers = [Tower((WIDTH - (self.brick_num + 1) * EVERY_BRICK_WIDTH) // 2, HEIGHT - 40,
                             (self.brick_num + 1) * EVERY_BRICK_WIDTH)]

    def every_step(self, input_actions):
        pygame.event.pump()

        reward = 0.1
        terminal = False

        if sum(input_actions) != 1:
            raise ValueError('Multiple input actions!')

        # input_actions[0] == 1: do nothing
        # input_actions[1] == 1: drop the wall
        if input_actions[1] == 1:
            # 放置墙体
            self.wall.drop()

        # 画出天空和背景
        screen.fill(SKY)
        screen.blit(IMAGES_BKG, (0, 0))

        # 更新墙体的位置
        self.wall.update()
        # 画出墙的位置
        self.wall.draw()

        for tower in self.towers:
            # 画出塔的位置
            tower.draw()

        # 在界面上方写上分数
        text = arial30.render(str(self.score), True, BRIGHT_RED)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((WIDTH / 2 - textX / 2), (50 - textY / 2)))
        # 在界面右上方写上评价
        text = arial35.render(self.evaluation, True, BLACK)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((WIDTH - textX - 20), (50 - textY / 2)))

        # ------------------
        # 如果放墙成功，将墙加入塔。重置活动的墙的位置
        if self.status == 1 or self.status == 2 or self.status == 3:
            reward = 0.33 if self.status == 1 else (0.66 if self.status == 2 else 1)
            self.wall.reset()

            # 更新塔的位置
            if len(self.towers) > 9:
                for tower in self.towers:
                    tower.update()

            if len(self.towers) > 0 and self.towers[0].y >= HEIGHT:
                del self.towers[0]

        elif self.status == -1:
            reward = -1
            terminal = True
            self.__init__()
        # ------------------

        image_data = pygame.surfarray.array3d(pygame.display.get_surface())
        pygame.display.update()
        clock.tick(30)

        return image_data, reward, terminal


# 移动的墙体
class Wall():
    def __init__(self, game):
        self.game = game
        self.init()

    def init(self):
        # 出生点横坐标
        self.x = 0
        # 出生点纵坐标，位于屏幕中上
        self.y = WIDTH // 2 - 100
        # 墙体宽度，与砖块数有关，每个砖块EVERY_BRICK_WIDTH个像素
        self.width = EVERY_BRICK_WIDTH * self.game.brick_num
        # 墙体高度
        self.height = 40
        # 30秒走完来回
        self.xV = (WIDTH - self.width) // TIME_FOR_ONE_TRUE

    def drop(self):
        '''
        放下一层墙
        :return:
        '''

        '''检查是否可以放置这层墙体'''
        if len(self.game.towers) == 0:
            # 还没有墙，随便放
            self.y = HEIGHT - self.height
            self.game.status = 1
        else:
            last_wall = self.game.towers[-1]
            self.y = last_wall.y - self.height

            if self.x >= last_wall.x + last_wall.width or self.x + self.width <= last_wall.x:
                # 放置失败，墙掉下去了
                self.y = last_wall.y
                self.game.status = -1
                self.game.evaluation = "Game Over!"
            else:
                # 放置成功。检查墙体长度的变化
                if self.x == last_wall.x:
                    # perfect放置，一次加3分
                    self.game.status = 3
                    self.game.evaluation = "Perfect!"
                elif abs(self.x - last_wall.x) < EVERY_BRICK_WIDTH:
                    # good放置，一次加2分，墙体长度不改变
                    self.game.status = 2
                    self.game.evaluation = "Good!"
                else:
                    # normal放置，需要减少墙体的砖数
                    self.game.status = 1
                    self.game.evaluation = "Normal!"
                    brick_num_to_reduce = abs(self.x - last_wall.x) // EVERY_BRICK_WIDTH
                    self.game.brick_num -= brick_num_to_reduce
                    # 重新调整墙体的宽度和坐标
                    self.width = self.game.brick_num * EVERY_BRICK_WIDTH
                    if self.x < last_wall.x:
                        # 截去多余部分
                        self.x += (brick_num_to_reduce * EVERY_BRICK_WIDTH)

        if self.game.status != -1:
            self.game.score += self.game.status

    def update(self):
        # 墙体还在活动中，更新墙的位置
        if self.game.status == 0:
            self.x += self.xV
            # 检查是否到达边界
            if self.x + self.width > WIDTH:
                self.x = WIDTH - self.width
                self.xV = -self.xV
            elif self.x < 0:
                self.x = 0
                self.xV = -self.xV

    def draw(self):
        if self.game.status == -1:
            # 游戏结束，放墙失败。放一个红色的墙
            pygame.draw.rect(screen, RED_WALL, (self.x, self.y, self.width, self.height))
            '''
            if self.game.dead_flag:
                SOUNDS['die'].play()
                self.game.dead_flag = False
            '''
        else:
            # 放一个墙颜色的墙
            pygame.draw.rect(screen, WALL, (self.x, self.y, self.width, self.height))
            '''
            if self.game.status == 3:
                SOUNDS['perfect'].play()
            elif self.game.status == 2:
                SOUNDS['good'].play()
            elif self.game.status == 1:
                SOUNDS['normal'].play()
            '''

    def reset(self):
        self.game.towers.append(Tower(self.x, self.y, self.width))
        self.game.status = 0

        self.init()


# 已建成的固定的塔
class Tower():
    def __init__(self, x, y, width):
        # 组成塔的已经放置的砖块的位置
        self.x = x
        self.y = y
        self.width = width
        self.height = 40

    def update(self):
        # 向下移动
        self.y += self.height

    # Rect: ((x, y), (width, height)), (x,y)是左上角的坐标
    def draw(self):
        # 绘制已经搭好的塔
        pygame.draw.rect(screen, TOWER, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, DARK_GROUND, (self.x, self.y, self.width, self.height), 3)
        # 绘制每个塔的砖数
        text = arial18.render(str(self.width // EVERY_BRICK_WIDTH), True, BLACK)
        textX = text.get_rect().width
        textY = text.get_rect().height
        screen.blit(text, ((self.x + (self.width - textX) / 2), (self.y + (self.height - textY) / 2)))


if __name__ == '__main__':
    game = BuildTower()
    while True:
        action = np.zeros([2])
        action_index = random.randrange(2)
        action[action_index] = 1

        game.every_step(action)
