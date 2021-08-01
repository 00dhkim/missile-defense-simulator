from dataclasses import dataclass
import math
import random
import turtle
from abc import *


@dataclass
class Pos:
    x: float = 0
    y: float = 0

class Turtlable:
    def __init__(self, x, y):
        self.init_pos = Pos(x, y)
        self.pos = Pos(self.init_pos.x, self.init_pos.y)
        self.turtle = turtle.Turtle()

    def turtle_init(self, init_x, init_y):
        self.turtle.up()
        self.turtle.goto(init_x, init_y)
        self.turtle.down()

    # 바뀐 위치로 터틀 이동
    def turtle_draw(self):
        self.turtle.goto(self.pos.x, self.pos.y)


class Missile(Turtlable):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.v_0 = 0.0 # 초기속도
        self.theta = 0.0 # 초기 발사각, 라디안 단위
        self.time = 0.0
        self.state = ''

    # 시간에 따른 x, y 좌표 구하기
    def calc_pos(self, t):
        x = self.pos_x_over_time(self.v_0, self.theta, t)
        y = self.pos_y_over_time(self.v_0, self.theta, t)

        self.pos.x = x
        self.pos.y = y

    @abstractmethod
    def pos_x_over_time(self, v_0, theta, t):
        pass

    @abstractmethod
    def pos_y_over_time(self, v_0, theta, t):
        pass


class AttackMissile(Missile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.turtle.pencolor('red')
        # 가능한 state 종류
        # standby: 발사 대기중
        # flying: 미사일 날아가는 중
        # impacted: 목표 지점에 착탄함
        # intercepted: 중간에 요격됨

    # 시간에 따른 x 좌표 계산
    def pos_x_over_time(self, v_0, theta, t):
        return v_0 * math.cos(theta) * t

    # 시간에 따른 y 좌표 계산
    def pos_y_over_time(self, v_0, theta, t):
        return -0.5 * 9.8 * t * t + v_0 * math.sin(theta) * t

    def launch_init_by_distance(self, distance):
        # theta의 최대, 최소 범위, 기본값은 0과 1
        lower = 0.7 # 0 이상 필요
        upper = 1 # 1 이하 필요

        theta = (upper - lower) * random.random() * math.pi / 2 + lower
        v_0 = (distance * 9.8 / math.sin(theta * 2)) ** 0.5

        # print("random", theta, v_0)

        # 이때의 착탄 시간: 2 * v_0 * math.sin(theta) / 9.8
        # 이때의 최대 높이: v_0 ** 2 * math.sin(theta) ** 2 / 2 / 9.8

        self.launch_init(v_0, theta)

    # 처음 1회만 실행
    def launch_init(self, v_0, theta):
        self.pos = Pos(self.init_pos.x, self.init_pos.y)
        self.v_0 = v_0
        self.theta = theta
        self.state = 'standby'

        self.turtle_init(0, 0)
        self.time = 0.0

    # 0.1초 진행마다 실행
    def launching(self, time):
        self.time = time
        self.state = 'flying'
        self.calc_pos(self.time)
        print(f"[ATTACK ] {self.state} time: {self.time} {self.pos}")
        self.turtle_draw()

        if self.pos.y < 0:
            self.state = 'impacted'

    # launching 끝나고 한번 실행
    def launch_end(self):
        self.turtle.up()
        self.turtle.goto(-10, -10)

    def intercepted(self):
        self.state = 'intercepted'

class DefenseMissile(Missile):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.turtle.pencolor('blue')
        self.turtle.up()
        self.turtle.goto(x,0)
        self.turtle.down()
        # 가능한 state 종류
        # standby: 발사 대기중
        # flying: 미사일 날아가는 중 (목표 지점 이전)
        # intercept_success: 요격 성공
        # intercept_passed: 요격 실패 후 지나침
        # impacted: 땅에 착탄

    # 시간에 따른 x 좌표 계산
    def pos_x_over_time(self, v_0, theta, t):
        # theta는 왼쪽 각도를 의미함, 발사가 왼쪽으로 되게끔 기본 세팅
        return self.init_pos.x - v_0 * math.cos(theta) * t

    # 시간에 따른 y 좌표 계산
    def pos_y_over_time(self, v_0, theta, t):
        return -0.5 * 9.8 * t * t + v_0 * math.sin(theta) * t

    # 처음 1회만 실행, 1초 후에 발사되는 경우
    # for case 2.
    def launch_init(self, v_a, theta_a):
        # 공격미사일의 초기속도와 초기발사각을 받아옴
        self.pos = Pos(self.init_pos.x, self.init_pos.y)
        self.v_0 = v_a # 공격미사일의 초기속력과 동일하다고 가정.

        A = v_a**2-40*v_a
        B = v_a ** 2 * math.sin(theta_a) - v_a * 9.8 / 2
        C = -v_a * 9.8 / 2 * math.cos(theta_a) - 40 * v_a * math.sin(theta_a) + 40 * 9.8

        print(f"A: {A}\nB: {B}\nC: {C}")


        print(f"theta_1: {((A-(A**2+B**2-C**2)**0.5)/(B+C))}")
        print(f"theta_2: {((A+(A**2+B**2-C**2)**0.5)/(B+C))}")

        # self.theta = 2 * math.atan((A+(A**2+B**2-C**2)**0.5)/(B+C))
        self.theta = 2 * math.atan((A-(A**2+B**2-C**2)**0.5)/(B+C))
        # 둘 중에 뭐가 맞는지 모르겠음. 둘 다 맞을 수도 있음.

        self.state = 'standby'

    '''
    # 처음 1회만 실행, 공격미사일과 동시에 발사
    # for case 1.
    def launch_init(self, v_a, theta_a):
        # 공격미사일의 초기속도와 초기발사각을 받아옴
        self.pos = Pos(self.init_pos.x, self.init_pos.y)
        self.theta = theta_a
        self.v_0 = v_a
        self.state = 'standby'
    '''

    # 0.1초마다 실행
    def launching(self, time, a_pos_x, a_pos_y):
        self.time = time
        self.state = 'flying'
        self.calc_pos(self.time)
        print(f"[DEFENSE] {self.state} time: {self.time} {self.pos}")
        self.turtle_draw()

        if self.pos.y < 0:
            self.state = 'impacted'
        elif (self.pos.x - a_pos_x)**2 + (self.pos.y - a_pos_y)**2 < 1:
            self.state = 'intercept_success'
        elif self.pos.x < a_pos_x:
            self.state = 'intercept_passed'

    # 땅에 닿을 경우와 요격한 경우 각각 따로
    def launch_end(self):
        self.turtle.up()
        self.turtle.goto(-20, -20)


if __name__ == '__main__':
    am = AttackMissile(0,0) # (0, 0) 좌표에서 발사
    dm = DefenseMissile(40, 0) # (40, 0) 좌표에 방어미사일 위치
    time = 0.0

    am.launch_init_by_distance(100) # 착탄위치 (100, 0)
    print(f"am.v_0: {am.v_0}, am.theta: {am.theta}")
    dm.launch_init(am.v_0, am.theta) # 요격할 대상: am

    # ------------------------------------------------------
    # case 1. -> 결과로그 및 비행 궤적 성공적
    # 공격미사일과 방어미사일이 동시에 날아가되, 방어미사일이 1초 기다리지 않고 공격미사일과 함께 발사
    '''
    while (am.state == 'standby' or am.state == 'flying') and \
            (dm.state == 'standby' or dm.state == 'flying'):

        am.launching(time)
        dm.launching(time, am.pos.x, am.pos.y)

        time += 0.01

        input()

    am.launch_end()
    dm.launch_end()
    '''
    # ------------------------------------------------------

    # ------------------------------------------------------
    # case 2.
    # 공격미사일과 방어미사일이 동시에 날아가는 시뮬레이션
    # '''
    while (am.state == 'standby' or am.state == 'flying') and \
            (dm.state == 'standby' or dm.state == 'flying'):

        am.launching(time)
        if time >= 1.0:
            dm.launching(time, am.pos.x, am.pos.y)

        time += 0.01

        input()

    am.launch_end()
    dm.launch_end()
    # '''
    # ------------------------------------------------------

    # ------------------------------------------------------
    # 공격미사일 먼저, 그 후 방어미사일 각각 날아가는 시뮬레이션
    '''
    while am.state == 'standby' or am.state == 'flying':
        am.launching(time)
        time += 0.1
    am.launch_end()

    time = 0.0
    while dm.state != 'impacted':
        dm.launching(time, am.pos.x, am.pos.y)
        time += 0.1
    dm.launch_end()
    
    '''
    # ------------------------------------------------------


    print('am:', am.state, 'dm:', dm.state)



    input("Press any key")

