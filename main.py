from dataclasses import dataclass
import math
import random
import turtle

def pos_x_over_time(v_0, theta, t):
    return v_0 * math.cos(theta) * t

def pos_y_over_time(v_0, theta, t):
    return -0.5 * 9.8 * t * t + v_0 * math.sin(theta) * t

@dataclass
class Pos:
    x: float = 0
    y: float = 0

class Turtlable:
    def __init__(self, x, y):
        self.init_pos = Pos(x, y)
        self.pos = Pos(self.init_pos.x, self.init_pos.y)

    def turtle_init(self, init_x, init_y):
        turtle.up()
        turtle.goto(init_x, init_y)
        turtle.down()

    # 바뀐 위치로 터틀 이동
    def turtle_draw(self):
        turtle.goto(self.pos.x, self.pos.y)


class Missile(Turtlable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.v_0 = 0 # 초기속도
        self.theta = 0 # 초기 발사각, 라디안 단위

    def calc_pos(self, t):
        x = pos_x_over_time(self.v_0, self.theta, t)
        y = pos_y_over_time(self.v_0, self.theta, t)

        self.pos.x = x
        self.pos.y = y



class AttackMissile(Missile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def launch_by_distance(self, distance):
        # theta의 최대, 최소 범위, 기본값은 0과 1
        lower = 0 # 0 이상 필요
        upper = 1 # 1 이하 필요

        theta = (upper - lower) * random.random() * math.pi / 2 + lower
        v_0 = (distance * 9.8 / math.sin(theta * 2)) ** 0.5

        # print("random", theta, v_0)

        # 이때의 착탄 시간: 2 * v_0 * math.sin(theta) / 9.8
        # 이때의 최대 높이: v_0 ** 2 * math.sin(theta) ** 2 / 2 / 9.8

        self.launch(v_0, theta)

    # 처음 1회만 실행
    def launch(self, v_0, theta):
        self.pos = Pos(self.init_pos.x, self.init_pos.y)
        self.v_0 = v_0
        self.theta = theta

        self.turtle_init(0, 0)
        time = 0.0
        # 땅에 닿기 전까지
        while self.pos.y >= 0:
            self.calc_pos(time)
            print(f"time: {time} {self.pos}")
            time += 0.1
            self.turtle_draw()

        turtle.up()
        turtle.goto(-10,-10)

class DefenseMissile(Missile):
    def __init__(self, x, y):
        super().__init__(x, y)

    def launch_intercept(self):
        # TODO: 시간 처리를 어떻게 할 것인가?
        # TODO: 왼쪽으로 발사되는 수식을 계산하기

if __name__ == '__main__':
    m = AttackMissile(0,0)
    m.pos.x = 10
    print(m.pos)
    #m.launch(50, math.pi/3)
    m.launch_by_distance(100)
    m.launch_by_distance(100)
    m.launch_by_distance(100)
    m.launch_by_distance(100)
    m.launch_by_distance(100)

    input("Press any key")

