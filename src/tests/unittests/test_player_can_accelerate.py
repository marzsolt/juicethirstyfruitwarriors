import unittest
import math
from unittest.mock import Mock, patch
from src.Server.Player.PlayerLogic import PlayerLogic
from src.utils.Vector2D import Vector2D

# Mock requests to control its behavior
requests = Mock()


def get_holidays():
    r = requests.get('http://localhost/api/holidays')
    if r.status_code == 200:
        return r.json()
    return None


class TestCanAccelerate(unittest.TestCase):
    @patch.multiple(PlayerLogic, __abstractmethods__=set())  # so that we can instantiate our abstract class
    def setUp(self):
        terrain = Mock()
        game = Mock()
        terrain.get_angle_rad.side_effect = [-math.pi / 6, 0, math.pi / 6]
        self.player = PlayerLogic(0, terrain, game)

    def test_can_accelerate_normal(self):
        self.player._vel = Vector2D.mag_ang_init(3.1, 0)  # over BASE_MAX_VEL, but downwards
        self.assertTrue(self.player.can_accelerate(1))
        self.player._vel = Vector2D.mag_ang_init(2.3, 0)  # normal speed
        self.assertTrue(self.player.can_accelerate(1))
        self.player._vel = Vector2D.mag_ang_init(3.1, math.pi)  # other direction
        self.assertTrue(self.player.can_accelerate(-1))

    def test_can_accelerate_backwards(self):
        self.player._vel = Vector2D.mag_ang_init(31, 0)  # Backwards? Any time!
        self.assertTrue(self.player.can_accelerate(-1))
        self.player._vel = Vector2D.mag_ang_init(2.3, math.pi-1)  # other direction
        self.assertTrue(self.player.can_accelerate(1))
        self.player._vel = Vector2D.mag_ang_init(0.5, 0)  # normal speed
        self.assertTrue(self.player.can_accelerate(-1))

    def test_can_accelerate_negative(self):
        self.player._vel = Vector2D.mag_ang_init(31, 0)  # Are you an aeroplane?
        self.assertFalse(self.player.can_accelerate(1))
        self.player._vel = Vector2D.mag_ang_init(31, math.pi - 1)  # No, you can't race into the other direction either.
        self.assertFalse(self.player.can_accelerate(-1))
        self.player._vel = Vector2D.mag_ang_init(1.6, 0)  # Angle is important you know...
        self.assertFalse(self.player.can_accelerate(1))