import math
from typing import List

from rlbot.utils.structures.game_interface import GameInterface

from choreography.choreography_main import Choreography
from choreography.choreos.air_show import YeetTheBallOutOfTheUniverse, DoNothing, Boost
from choreography.drone import Drone
from choreography.group_step import StateSettingStep, BlindBehaviorStep
from rlutilities.linear_algebra import vec3, look_at, euler_to_rotation
from rlutilities.simulation import Input


class SetUp(StateSettingStep):
    def set_drone_states(self, drones: List[Drone]):
        drones[0].position = vec3(0, 0, 100)
        drones[0].orientation = euler_to_rotation(vec3(0, math.pi / 2, 0))
        drones[0].velocity = vec3(0, 0, 0)
        drones[0].angular_velocity = vec3(0, 0, 0)
        drones[1].position = vec3(-250, 4500, 100)
        drones[1].orientation = euler_to_rotation(vec3(0, -math.pi / 2, 0))
        drones[1].velocity = vec3(0, 0, 0)
        drones[1].angular_velocity = vec3(0, 0, 0)
        drones[2].position = vec3(250, 4500, 100)
        drones[2].orientation = euler_to_rotation(vec3(0, -math.pi / 2, 0))
        drones[2].velocity = vec3(0, 0, 0)
        drones[2].angular_velocity = vec3(0, 0, 0)
        for i in range(3, 7):
            drones[i].position = vec3(0, -4500, 500)


class SetUpShot(StateSettingStep):
    def set_drone_states(self, drones: List[Drone]):
        drones[3].position = vec3(250, 250, 100)
        drones[3].orientation = euler_to_rotation(vec3(0, math.pi / 2, 0))
        drones[3].velocity = vec3(0, 3000, 0)
        drones[3].angular_velocity = vec3(0, 0, 0)
        drones[4].position = vec3(-250, 250, 100)
        drones[4].orientation = euler_to_rotation(vec3(0, math.pi / 2, 0))
        drones[4].velocity = vec3(0, 3000, 0)
        drones[4].angular_velocity = vec3(0, 0, 0)
        drones[5].position = vec3(250, 4250, 100)
        drones[5].orientation = euler_to_rotation(vec3(0, -math.pi / 2, 0))
        drones[5].velocity = vec3(0, -3000, 0)
        drones[5].angular_velocity = vec3(0, 0, 0)
        drones[6].position = vec3(-250, 4250, 100)
        drones[6].orientation = euler_to_rotation(vec3(0, -math.pi / 2, 0))
        drones[6].velocity = vec3(0, -3000, 0)
        drones[6].angular_velocity = vec3(0, 0, 0)


class SetUpFinalShot(StateSettingStep):
    def set_drone_states(self, drones: List[Drone]):
        drones[3].position = vec3(250, 250, 100)
        drones[3].orientation = euler_to_rotation(vec3(0, math.pi / 2, 0))
        drones[3].velocity = vec3(0, 3000, 0)
        drones[3].angular_velocity = vec3(0, 0, 0)
        drones[4].position = vec3(-250, 250, 100)
        drones[4].orientation = euler_to_rotation(vec3(0, math.pi / 2, 0))
        drones[4].velocity = vec3(0, 3000, 0)
        drones[4].angular_velocity = vec3(0, 0, 0)


class Shoot(BlindBehaviorStep):
    duration = 2
    target_indexes = range(3, 7)

    def set_controls(self, controls: Input):
        controls.boost = True


class Pause(BlindBehaviorStep):
    duration = 2
    target_indexes = range(0, 10)

    def set_controls(self, controls: Input):
        pass


class TheFight(Choreography):

    @staticmethod
    def get_appearances(num_bots: int) -> List[str]:
        appearances = ['default.cfg'] * num_bots
        appearances[0] = 'AirShowBlue.cfg'
        appearances[1] = 'AirShowBlue.cfg'
        appearances[2] = 'AirShowBlue.cfg'
        appearances[3] = 'AirShowBlue.cfg'
        appearances[4] = 'AirShowBlue.cfg'
        appearances[5] = 'AirShowBlue.cfg'
        appearances[6] = 'AirShowBlue.cfg'
        return appearances

    @staticmethod
    def get_teams(num_bots: int) -> List[int]:
        # Every other bot is on the orange team.
        teams = [0] * num_bots
        teams[0] = 0
        teams[1] = 1
        teams[2] = 1
        teams[3] = 0
        teams[4] = 0
        teams[5] = 1
        teams[6] = 1
        return teams

    @staticmethod
    def get_num_bots():
        return 7

    def __init__(self, game_interface: GameInterface):
        super().__init__(game_interface)

    def generate_sequence(self):
        self.sequence = [
            YeetTheBallOutOfTheUniverse(),
            SetUp(),
            Pause(),
            SetUpShot(),
            Shoot(),
            Pause(),
            SetUpFinalShot(),
            Shoot(),
            Pause(),
            Pause(),
            DoNothing(),
        ]
