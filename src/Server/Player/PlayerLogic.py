import math
import logging
from enum import Enum
import abc

from src.Server.Network_communication.Server import Server
from src.utils.Vector2D import Vector2D
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage
from src.utils.Timer import Timer


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


class PlayerLogic(abc.ABC):
    """ Server side player. Processes movement/attack/... request, handles physics and more! :) """
    SCREEN_WIDTH = 800  # TODO use general constant
    RADIUS = 25
    X_MIN = RADIUS
    X_MAX = SCREEN_WIDTH-RADIUS  # TODO use screen sizes
    G = -1
    C_AIR = 0.3

    def __init__(self, player_id, terrain, game):
        self.logger = logging.getLogger('Domi.PlayerLogic')
        self._id = player_id
        self._terrain = terrain
        self._game = game
        self._mobility = 0.3  # acceleration force, for max velocity check can_accelerate function
        self.mu = 0.1  # friction constant
        self._mass = 1  # effects how fast player can accelerate/decelerate (shouldn't be much different than 1)
        self.pos = Vector2D(50+player_id*100, 300)
        self._vel = Vector2D.zero()
        self._forces = []
        self._is_flying = True
        self._attack_on_cooldown = False
        self._is_attacking = False
        self.can_get_hurt = True
        self.max_hp = 100
        self.hp = self.max_hp

    def update(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.PLAYER_LOGIC+str(self._id))
        self._process_requests(messages)
        self._do_physics()  # main physic computations
        self._send_updated_pos_hp()

    def get_id(self):
        return self._id

    def _process_movement_messages(self, pos_mess):
        for m in pos_mess:
            for mess in m.movement_list:
                if mess == climess.ActionRequest.MOVE_LEFT:
                    self._move_left()
                elif mess == climess.ActionRequest.MOVE_RIGHT:
                    self._move_right()

    def _process_requests(self, network_messages):
        """ Basic movement requests are filtered and delegated to _process_movement_messages.
        As of the other type of requests, derivations shall process them (after super!)."""
        pos_mess = []
        for mess in reversed(network_messages):  # reverse looping is needed because we remove elements
            if mess.type == climess.MessageType.PLAYER_MOVEMENT:
                pos_mess.append(mess)
                network_messages.remove(mess)
        self._process_movement_messages(pos_mess)

    def _send_updated_pos_hp(self):
        """ Sends player's updated data to all clients. """
        msg = BaseMessage(mess_type=sermess.MessageType.PLAYER_POS_HP, target=sermess.Target.PLAYER + str(self._id))
        msg.player_id = self._id
        msg.x = self.pos.x
        msg.y = self.pos.y
        msg.dir = self.my_dir().value
        msg.hp = self.hp
        Server.get_instance().send_all(msg)  # all clients shall know the data of all players

    @abc.abstractmethod
    def can_attack(self, **kwargs):
        """ Returns whether the payer can attack now, based on cooldown.
        Derivations may add extra conditions."""
        return not self._attack_on_cooldown

    def _attack(self):
        self._is_attacking = True
        self._attack_on_cooldown = True
        self.can_get_hurt = False
        Timer.sch_fun(100, self.restore_attack_ability, ())

    def _finish_attack(self):
        self._is_attacking = False
        self.can_get_hurt = True
        self._stop()

    def restore_attack_ability(self):
        self._attack_on_cooldown = False

    def _add_force(self, force2d):
        """ Base of physics. By adding a force, you accelerate the player a little bit. """
        self._forces.append(force2d)

    def _add_ground_directed_force(self, force_mag, direction):
        """ Adds force which is parallel with terrain, so that it's
        enough to set magnitude and direction: right/left  1/-1. """
        ang = self._terrain.get_angle_rad(self.pos.x)
        force = Vector2D.mag_ang_init(force_mag*direction.value, ang)
        self._add_force(force)

    def my_dir(self):
        """ Determines whether the player moves right (1) or left (-1).
        Zero velocity is considered left directed. """
        if self._vel.x > 0:
            return Direction.RIGHT
        return Direction.LEFT

    def can_accelerate(self, direction=1):
        """ Determines if player can accelerate int he given direction.
         This is for basic left/right movement, other forces doesn't use this."""
        if direction*self._vel.x < 0:  # it can always decelerate
            return True
        BASE_MAX_VEL = 3.0  # can accelerate until this amount without angle
        ANGLE_DEPENDENCY = 3.0  # how much terrain's angle effects max velocity
        angle_bonus = -direction * math.sin(self._terrain.get_angle_rad(self.pos.x)) * ANGLE_DEPENDENCY
        return self._vel.mag() < BASE_MAX_VEL + angle_bonus

    def _move_left(self):
        if self.can_accelerate(-1):
            self._add_ground_directed_force(self._mobility, Direction.LEFT)

    def _move_right(self):
        if self.can_accelerate(1):
            self._add_ground_directed_force(self._mobility, Direction.RIGHT)

    def _stop(self):
        self._vel = Vector2D.zero()

    def _put_to_ground_level(self):
        """ Sets y position so that the player will be on ground. """
        self.pos.y = self._terrain.get_level(self.pos.x)+self.RADIUS

    def _get_y_to_ground_level(self):
        """ Difference of y position and ground level."""
        return self.pos.y - (self._terrain.get_level(self.pos.x)+self.RADIUS)

    def _impact(self):
        """ Called when player hits ground after flying. """
        pass

    def _do_physics(self):
        """ Physics engine... coputes environmental forces, resultant force, acceleration,
        velocity, position. It also checks for flying and may make position corrections. """
        # Add some environmental forces
        if self._is_flying:
            # add gravitation
            mg = self.G * self._mass
            self._add_force(Vector2D(0, mg))
        else:
            # add friction
            friction = self._mass * self.mu  # yes it's not perfectly accurate physics
            friction = min(self._vel.mag()*self._mass, friction)  # shouldn't accelerate to the opposite direction
            self._add_ground_directed_force(-friction, self.my_dir())

        # Compute main properties!
        resultant_force = Vector2D.sum(self._forces)
        self._forces = []
        res_acc = resultant_force.scalar_div(self._mass)
        self._vel += res_acc
        self.pos += self._vel

        # Check if it flies
        # minimum velocity angle difference (to ground grad) which is considered flying with pos diff threshold together
        threshold_ang = 2*3.14/180.0
        # minimum y difference to ground level which is considered flying with angle threshold together
        threshold_pos = 2
        # minimum y difference to ground level which alone is considered flying
        threshold_big_pos = 5
        vel_angle_diff = math.fabs(self._vel.domi_ang() - self._terrain.get_angle_rad(self.pos.x))
        pos_diff = self._get_y_to_ground_level()
        if (vel_angle_diff > threshold_ang and pos_diff > threshold_pos)\
                or pos_diff > threshold_big_pos:
            # if not self._is_flying:
            #    self._add_force(Vector2D(0, 10))  # a little jump for fun :)
            self._is_flying = True

        # Check if it's under ground, make corrections
        if self._get_y_to_ground_level() < 0:
            # player is under ground -> move up, doesn't fly, set velocity direction
            if self._is_flying:
                self._impact()
            self._is_flying = False
            self._put_to_ground_level()
            if self._vel.mag() > 0:
                loss = self._vel.dot_product(self._terrain.slope_grad(self.pos.x)) / self._vel.mag()  # projection
                self._vel.change_dir(self._terrain.get_angle_rad(self.pos.x))
                self._vel.scalar_mult(loss)

        # Check if it's in screen, make corrections
        if self.pos.x < self.X_MIN:
            self.pos.x = self.X_MIN
            self._vel.x = -self._vel.x
        elif self.pos.x > self.X_MAX:
            self.pos.x = self.X_MAX
            self._vel.x = -self._vel.x

    def is_moving(self):
        return self._vel.mag() > 0.001
