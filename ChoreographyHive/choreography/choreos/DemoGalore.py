from typing import List

from rlbot.utils.structures.game_interface import GameInterface

from choreography.choreos.StarWars import ScoreDistance
from choreography.choreography_main import Choreography
from choreography.choreos.air_show import Boost


class DemoGalore(Choreography):
    map_name = "Underpass"

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
        appearances[7] = 'AirShowBlue.cfg'
        appearances[8] = 'AirShowBlue.cfg'
        appearances[9] = 'AirShowBlue.cfg'
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
        teams[7] = 0
        teams[8] = 0
        teams[9] = 1
        return teams

    @staticmethod
    def get_num_bots():
        return 10

    def __init__(self, game_interface: GameInterface):
        super().__init__(game_interface)

    def generate_sequence(self):
        self.sequence = [
            Boost(),
            ScoreDistance(),
        ]
