from Server import Server
import server_message_constants as sermess
import client_message_constants as climess
from BaseMessage import BaseMessage
from Vector2D import Vector2D

import math


class PlayerLogic:
    X_MIN = 20
    X_MAX = 780  # TODO use screen sizes, Terrain normal functions...
    Y_MIN = 0
    Y_MAX = 600
    G = -1
    C_AIR = 0.005

    def __init__(self, player_id, terrain):
        self._id = player_id
        self._terrain = terrain
        self._mobility = 1
        # self._x = 100+player_id*100  # for testing
        # self._y = 100+player_id*100
        self._mass = 1
        self._pos = Vector2D(50+player_id*100, 300)
        self._vel = Vector2D(0, 0)
        self._forces = []
        self._is_flying = True

        self.initial_pos_sending = True

    def update(self):
        messages = Server.get_instance().get_targets_messages(climess.Target.PLAYER_LOGIC+str(self._id))
        position_messages = list(filter(lambda x: x.type == climess.MessageType.PLAYER_MOVEMENT, messages))
        self._process_requests(position_messages)
        self._do_physics()
        # if position_messages or self.initial_pos_sending:
        self._send_updated_pos()
        self.initial_pos_sending = False

    def get_id(self):
        return self._id

    def _add_force(self, force2d):
        self._forces.append(force2d)

    def _add_ground_directed_force(self, force_mag):
        ang = self._terrain.get_angle_rad(self._pos.x)
        force = Vector2D.mag_ang_init(force_mag, ang)
        self._add_force(force)

    def _process_requests(self, network_messages):
        for m in network_messages:
            for mess in m.movement_list:
                if mess == climess.ActionRequest.MOVE_LEFT:
                    self._move_left()
                elif mess == climess.ActionRequest.MOVE_RIGHT:
                    self._move_right()

    def _move_left(self):
        self._add_ground_directed_force(-self._mobility)
        # self._x = self._x - self._speed

        # self._x = min(max(self._x, self.X_MIN), self.X_MAX)
        # self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

    def _move_right(self):
        self._add_ground_directed_force(self._mobility)
        # self._x = self._x + self._speed

        # self._x = min(max(self._x, self.X_MIN), self.X_MAX)
        # self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

    def _send_updated_pos(self):
        msg = BaseMessage(mess_type=sermess.MessageType.PLAYER_POSITION, target=sermess.Target.PLAYER + str(self._id))
        msg.player_id = self._id
        msg.x = self._pos.x
        msg.y = self._pos.y
        Server.get_instance().send_all(msg)

    def _do_physics(self):
        if self._is_flying:
            self._forces = []
            mg = self.G * self._mass
            self._add_force(Vector2D(0, mg))
        else:
            mgx = self.G * self._mass * math.sin(self._terrain.get_angle_rad(self._pos.x))
            self._add_ground_directed_force(mgx)
            air_resistance = self._vel
            print(air_resistance)
            air_resistance.scalar_mult(-self.C_AIR)
            print(air_resistance)
            self._add_force(air_resistance)

        resultant_force = Vector2D.sum(self._forces)
        # print(self._forces)
        self._forces = []
        res_acc = resultant_force.scalar_div(self._mass)
        # print(res_acc)
        self._vel += res_acc
        # print(self._vel)
        self._pos += self._vel

        if self._pos.x < self.X_MIN:
            self._pos.x = self.X_MIN
            self._vel = Vector2D.zero()
        elif self._pos.x > self.X_MAX:
            self._pos.x = self.X_MAX
            self._vel = Vector2D.zero()



        threshold = 0.1
        if self._pos.y > self._terrain.get_level(self._pos.x) + threshold:
            self._is_flying = True
        else:
            self._is_flying = False
            self._pos.y = self._terrain.get_level(self._pos.x)
            if self._vel.mag() > 0:
                loss = self._vel.dot_product(self._terrain.slope_grad(self._pos.x)) / self._vel.mag()
                self._vel.change_dir(self._terrain.get_angle_rad(self._pos.x))
                self._vel.scalar_mult(loss)

