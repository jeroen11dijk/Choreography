from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.game_interface import GameInterface

from choreography.choreography_main import Choreography
from choreography.drone import Drone
from choreography.group_step import BlindBehaviorStep, StateSettingStep, ParallelStep, DroneListStep
from choreography.paths.AirShowPath import get_paths
from choreography.utils.vector_math import direction
from rlutilities.linear_algebra import vec3, look_at, cross, normalize
from rlutilities.simulation import Ball, Input, Curve


class Pause(BlindBehaviorStep):
    duration = 8
    target_indexes = range(0, 2)

    def set_controls(self, controls: Input):
        pass


class BlueTouchesTHeBall(StateSettingStep):

    def set_drone_states(self, drones: List[Drone]):
        drones[1].position = vec3(0, -5000, 250)
        drones[1].velocity = vec3(0, 0, 0)
        drones[1].angular_velocity = vec3(0, 0, 0)

    def set_ball_state(self, ball: Ball):
        ball.position = vec3(0, -5000, 100)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class YeetTheBallOutOfTheUniverse(StateSettingStep):
    def set_ball_state(self, ball: Ball):
        ball.position = vec3(0, 0, 3000)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class Score(StateSettingStep):
    def set_ball_state(self, ball: Ball):
        ball.position = vec3(0, 5120, 300)
        ball.velocity = vec3(0, 5000, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class DoNothing(StateSettingStep):
    pass


class SetupHover(StateSettingStep):

    def set_drone_states(self, drones: List[Drone]):
        drone = drones[1]
        drone.position = vec3(-1500, 500, 800)
        drone.velocity = vec3(0, 0, 0)
        drone.angular_velocity = vec3(0, 0, 0)
        drone.orientation = look_at(vec3(0, 0, 500), vec3(0, 0, 1))


class Fly(StateSettingStep):
    duration = 5
    distance_between_body_parts = 300
    curve: Curve = None

    def set_drone_states(self, drones: List[Drone]):
        for drone in drones:
            t = self.time_since_start / self.duration * self.curve.length
            t -= self.distance_between_body_parts * (drone.id - self.target_indexes[0])
            t = self.curve.length - t

            pos = self.curve.point_at(t)
            pos_ahead = self.curve.point_at(t - 500)
            pos_behind = self.curve.point_at(t + 30)

            facing_direction = direction(pos_behind, pos)
            target_left = cross(facing_direction, direction(pos, pos_ahead))
            target_up = cross(target_left, facing_direction)
            up = drone.up() + target_up * 0.9 + vec3(0, 0, 0.1)
            target_orientation = look_at(facing_direction, up)

            drone.position = pos
            drone.velocity = facing_direction * (self.curve.length / self.duration)
            drone.angular_velocity = vec3(0, 0, 0)
            drone.orientation = target_orientation
            drone.boost = True


class Hover(DroneListStep):
    def step(self, packet: GameTickPacket, drones: List[Drone]):
        drone = drones[1]
        drone.hover.up = normalize(drone.position)
        drone.hover.target = drone.position
        drone.hover.step(self.dt)
        drone.controls = drone.hover.controls


class bot0(Fly):
    curve = Curve(get_paths()[0].to_points(1000))
    target_indexes = range(0, 1)


class bot1(Fly):
    curve = Curve(get_paths()[1].to_points(1000))
    target_indexes = range(1, 2)


class bot2(Fly):
    curve = Curve(get_paths()[2].to_points(1000))
    target_indexes = range(2, 3)


class bot3(Fly):
    curve = Curve(get_paths()[3].to_points(1000))
    target_indexes = range(3, 4)


class bot4(Fly):
    curve = Curve(get_paths()[4].to_points(1000))
    target_indexes = range(4, 5)


class bot5(Fly):
    curve = Curve(get_paths()[5].to_points(1000))
    target_indexes = range(5, 6)


class bot6(Fly):
    curve = Curve(get_paths()[6].to_points(1000))
    target_indexes = range(6, 7)


class bot7(Fly):
    curve = Curve(get_paths()[7].to_points(1000))
    target_indexes = range(7, 8)


class bot8(Fly):
    curve = Curve(get_paths()[8].to_points(1000))
    target_indexes = range(8, 9)


class Boost(BlindBehaviorStep):
    duration = 10
    target_indexes = range(0, 10)

    def set_controls(self, controls: Input):
        controls.boost = True


class AirShow(Choreography):

    @staticmethod
    def get_appearances(num_bots: int) -> List[str]:
        appearances = ['default.cfg'] * num_bots
        appearances[0] = 'AirShowBlue.cfg'
        appearances[1] = 'AirShowBlue.cfg'
        return appearances

    @staticmethod
    def get_teams(num_bots: int) -> List[int]:
        # Every other bot is on the orange team.
        teams = [0] * num_bots
        teams[0] = 0
        teams[1] = 0
        return teams

    @staticmethod
    def get_num_bots():
        return 2

    def __init__(self, game_interface: GameInterface):
        super().__init__(game_interface)

    def generate_sequence(self):
        self.sequence = [
            Pause(),
            BlueTouchesTHeBall(),
            bot0(),
            Score(),
            DoNothing(),
        ]
