class PlayerLogic:
    def __init__(self, player_id):
        self._id = player_id
        self._speed = 5
        self._x = 100
        self._y = 100

    def process_requests(self, network_messages, player):
        # TODO load messages from Network by id
        for mess in network_messages:
            if mess == "LEFT":
                self._x = self._x - self._speed
            elif mess == "RIGHT":
                self._x = self._x + self._speed

        player.pos_update(self._x, self._y)

    def update(self, pressed_keys, events):
        pass


# FOR testing
test_player = PlayerLogic(0)
