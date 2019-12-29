import math
from typing import List

from rlbot.utils.structures.game_data_struct import GameTickPacket
from rlbot.utils.structures.game_interface import GameInterface

from choreography.choreography import Choreography
from choreography.drone import Drone
from choreography.group_step import BlindBehaviorStep, DroneListStep, StepResult, PerDroneStep, StateSettingStep

from rlutilities.linear_algebra import vec3, rotation, dot, vec2, look_at, mat3, norm, cross
from rlutilities.simulation import Ball, Input

from choreography.img_to_shape import convert_img_to_shape


class YeetTheBallOutOfTheUniverse(StateSettingStep):
    def set_ball_state(self, ball: Ball):
        ball.position = vec3(0, 0, 3000)
        ball.velocity = vec3(0, 0, 0)
        ball.angular_velocity = vec3(0, 0, 0)


class FormACircle(StateSettingStep):
    radius = 2000
    center = vec3(0, 0, 0)

    def set_drone_states(self, drones: List[Drone]):
        for i, drone in enumerate(drones):
            angle = i * math.pi * 2 / len(drones)
            rot = rotation(angle)
            v = vec3(dot(rot, vec2(1, 0)))
            drone.position = v * self.radius + self.center
            drone.orientation = look_at(v * -1, vec3(0, 0, 1))
            drone.velocity = vec3(0, 0, 0)
            drone.angular_velocity = vec3(0, 0, 0)


class LurchForward(BlindBehaviorStep):
    duration = 0.6

    def set_controls(self, controls: Input):
        controls.jump = True
        controls.pitch = 0.2
        controls.boost = True


class Spiral(DroneListStep):
    duration = 1.5

    def step(self, packet: GameTickPacket, drones: List[Drone]):
        a = 1.0 / len(drones)
        for i, drone in enumerate(drones):
            drone.controls.throttle = a*i


class HexSetup(StateSettingStep):
    radius = 300
    center = vec3(-2000, 0, 100)

    def set_drone_states(self, drones: List[Drone]):
        for i, drone in enumerate(drones):
            angle = i * math.pi * 2 / len(drones)
            rot = rotation(angle)
            v = vec3(dot(rot, vec2(1, 0)))
            drone.position = v * self.radius + self.center
            drone.orientation = look_at(vec3(2,0,3), vec3(1,0,0))
            drone.velocity = vec3(0, 0, 500)
            drone.angular_velocity = vec3(0, 0, 0)


class BoostUntilFast(DroneListStep):
    def step(self, packet: GameTickPacket, drones: List[Drone]):
        self.finished = norm(drones[0].velocity) > 1000

        for drone in drones:
            drone.controls.pitch = 0
            drone.controls.boost = True


class BackflipBoostyThing(BlindBehaviorStep):
    duration = 6.0

    def set_controls(self, controls: Input):
        controls.pitch = 0.5
        controls.boost = True



class Drawing(StateSettingStep):

    def __init__(self, image, origin=vec3(0,0,18), duration=2.0):
        super().__init__()
        self.duration = duration
        self.origin = origin
        self.shape = convert_img_to_shape(image)
    
    def set_drone_states(self, drones: List[Drone]):
        for i, drone in enumerate(drones):
            if i < len(self.shape):
                drone.position = self.origin + self.shape[i]
                drone.orientation = mat3(1,0,0,0,1,0,0,0,1)
                drone.velocity = vec3(0, 0, 0)
            else:
                drone.position = vec3(0, 0, 3000)



class Test(Choreography):

    @staticmethod
    def get_num_bots():
        return 6

    def __init__(self, game_interface: GameInterface):
        super().__init__(game_interface)

    def generate_sequence(self):
        self.sequence = [
            YeetTheBallOutOfTheUniverse(),
            HexSetup(),
            BoostUntilFast(),
            BackflipBoostyThing()
        ]
