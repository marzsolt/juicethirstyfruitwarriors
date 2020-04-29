import math
from enum import Enum

from src.Server.Network_communication.Server import Server
from src.utils.Vector2D import Vector2D
import src.Server.Network_communication.server_message_constants as sermess

import src.Client.Network_communication.client_message_constants as climess

from src.utils.BaseMessage import BaseMessage
from src.utils.Timer import Timer


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


class PlayerLogic:
    SCREEN_WIDTH = 800  # TODO use general constant
    RADIUS = 25
    X_MIN = RADIUS
    X_MAX = SCREEN_WIDTH-RADIUS  # TODO use screen sizes
    G = -1
    C_AIR = 0.3

    def __init__(self, player_id, terrain):
        self._id = player_id
        self._terrain = terrain
        self._mobility = 0.3  # acceleration force, for max velocity check can_accelerate function
        self.mu = 0.1  # friction constant
        self._mass = 1
        self._pos = Vector2D(50+player_id*100, 300)
        self._vel = Vector2D.zero()
        self._forces = []
        self._is_flying = True
        self._can_attack = True
        self.hp = 100

    def update(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.PLAYER_LOGIC+str(self._id))
        self._process_requests(messages)
        self._do_physics()
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
        pos_mess = []
        for mess in reversed(network_messages):  # reverse looping is needed because we remove elements
            if mess.type == climess.MessageType.PLAYER_MOVEMENT:
                pos_mess.append(mess)
                network_messages.remove(mess)
        # position_messages = list(filter(lambda x: x.type == climess.MessageType.PLAYER_MOVEMENT, network_messages))
        self._process_movement_messages(pos_mess)

    def _send_updated_pos_hp(self):
        msg = BaseMessage(mess_type=sermess.MessageType.PLAYER_POS_HP, target=sermess.Target.PLAYER + str(self._id))
        msg.player_id = self._id
        msg.x = self._pos.x
        msg.y = self._pos.y
        msg.dir = self.my_dir().value
        msg.hp = self.hp
        Server.get_instance().send_all(msg)

    def _attack(self):
        #if self._can_attack:
        self._can_attack = False
        Timer.sch_fun(100, self.restore_attackaibility, ())

    def restore_attackaibility(self):
        self._can_attack = True

    def _add_force(self, force2d):
        self._forces.append(force2d)

    def _add_ground_directed_force(self, force_mag, direction):
        ang = self._terrain.get_angle_rad(self._pos.x)
        force = Vector2D.mag_ang_init(force_mag*direction.value, ang)
        self._add_force(force)

    def my_dir(self):
        if self._vel.x > 0:
            return Direction.RIGHT
        return Direction.LEFT

    def can_accelerate(self, direction=1):
        if direction*self._vel.x < 0:  # it can always decelerate
            return True
        BASE_MAX_VEL = 3.0
        ANGLE_DEPENDENCY = 3.0
        angle_bonus = -direction * math.sin(self._terrain.get_angle_rad(self._pos.x)) * ANGLE_DEPENDENCY
        return self._vel.mag() < BASE_MAX_VEL + angle_bonus

    def _move_left(self):
        if self.can_accelerate(-1):
            self._add_ground_directed_force(self._mobility, Direction.LEFT)

    def _move_right(self):
        if self.can_accelerate(1):
            self._add_ground_directed_force(self._mobility, Direction.RIGHT)

    def _stop(self): # TODO: this seems to benevr used
        self._vel = Vector2D.zero()

    def _put_to_ground_level(self):
        self._pos.y = self._terrain.get_level(self._pos.x)+self.RADIUS

    def _get_y_to_ground_level(self):
        return self._pos.y - (self._terrain.get_level(self._pos.x)+self.RADIUS)

    def _impact(self):
        pass  # BUMM!

    def _do_physics(self):
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
        self._pos += self._vel

        # Check if it flies
        # minimum velocity angle difference (to ground grad) which is considered flying with pos diff threshold together
        threshold_ang = 2*3.14/180.0
        # minimum y difference to ground level which is considered flying with angle threshold together
        threshold_pos = 2
        # minimum y difference to ground level which alone is considered flying
        threshold_big_pos = 5
        vel_angle_diff = math.fabs(self._vel.domi_ang()-self._terrain.get_angle_rad(self._pos.x))
        pos_diff = self._get_y_to_ground_level()
        if (vel_angle_diff > threshold_ang and pos_diff > threshold_pos)\
                or pos_diff > threshold_big_pos:
            if not self._is_flying:
                self._add_force(Vector2D(0, 10))  # a little jump for fun :)
            self._is_flying = True

        # Check if it's under ground, make corrections
        if self._get_y_to_ground_level() < 0:
            # player is under ground -> move up, doesn't fly, set velocity direction
            if self._is_flying:
                self._impact()
            self._is_flying = False
            self._put_to_ground_level()
            if self._vel.mag() > 0:
                loss = self._vel.dot_product(self._terrain.slope_grad(self._pos.x)) / self._vel.mag()  # projection
                self._vel.change_dir(self._terrain.get_angle_rad(self._pos.x))
                self._vel.scalar_mult(loss)

        # Check if it's in screen, make corrections
        if self._pos.x < self.X_MIN:
            self._pos.x = self.X_MIN
            self._vel.x = -self._vel.x
        elif self._pos.x > self.X_MAX:
            self._pos.x = self.X_MAX
            self._vel.x = -self._vel.x
