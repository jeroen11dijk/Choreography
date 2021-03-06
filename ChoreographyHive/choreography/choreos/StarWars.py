from typing import List

from rlbot.utils.structures.game_interface import GameInterface

from choreography.choreography_main import Choreography
from choreography.choreos.air_show import DoNothing, Fly, Pause
from choreography.group_step import StateSettingStep, ParallelStep, BlindBehaviorStep
from choreography.paths.AirShowPath import get_paths
from drone import Drone
from rlutilities.linear_algebra import vec3
from rlutilities.simulation import Ball, Curve, Input


class BlueTouchesTHeBall(StateSettingStep):

    def set_drone_states(self, drones: List[Drone]):
        drones[3].position = vec3(1000, 1000, 250)
        drones[3].velocity = vec3(0, 0, 0)
        drones[3].angular_velocity = vec3(0, 0, 0)

    def set_ball_state(self, ball: Ball):
        ball.position = vec3(1000, 1000, 100)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class bot1(Fly):
    duration = 10
    curve = Curve(get_paths()[1].to_points(1000))
    target_indexes = range(0, 1)


class bot2(Fly):
    duration = 10
    curve = Curve(get_paths()[2].to_points(1000))
    target_indexes = range(1, 2)


class bot3(Fly):
    duration = 10
    curve = Curve(get_paths()[3].to_points(1000))
    target_indexes = range(2, 3)


class SetHyperSpace(StateSettingStep):
    def set_ball_state(self, ball: Ball):
        ball.position = vec3(-11390, -6950, 470)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class ScoreDistance(StateSettingStep):
    def set_ball_state(self, ball: Ball):
        ball.position = vec3(0, 5500, 300)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class StarWars(Choreography):
    map_name = "Underpass"

    @staticmethod
    def get_appearances(num_bots: int) -> List[str]:
        appearances = ['default.cfg'] * num_bots
        appearances[0] = 'AirShowBlue.cfg'
        appearances[1] = 'AirShowBlue.cfg'
        appearances[2] = 'AirShowBlue.cfg'
        appearances[3] = 'AirShowBlue.cfg'
        return appearances

    @staticmethod
    def get_teams(num_bots: int) -> List[int]:
        # Every other bot is on the orange team.
        teams = [0] * num_bots
        teams[0] = 0
        teams[1] = 1
        teams[2] = 1
        teams[3] = 0
        return teams

    @staticmethod
    def get_num_bots():
        return 4

    def __init__(self, game_interface: GameInterface):
        super().__init__(game_interface)

    def generate_sequence(self):
        self.sequence = [
            Pause(),
            BlueTouchesTHeBall(),
            ParallelStep([
                bot1(),
                bot2(),
                bot3()
            ]),
            SetHyperSpace(),
            ScoreDistance(),
            DoNothing(),
        ]
