class PlayerLogic:
    X_MIN = 0
    X_MAX = 800  # todo AUTOMATICALLY GET SCREEN SIZES
    Y_MIN = 0
    Y_MAX = 600

    def __init__(self, player_id):
        self._id = player_id
        self._speed = 5
        self._x = 100+player_id*100
        self._y = 100+player_id*100

    def process_requests(self, network_messages, player):
        # TODO load messages from Network by id
        for mess in network_messages:
            if mess == "LEFT":
                self._x = self._x - self._speed
            elif mess == "RIGHT":
                self._x = self._x + self._speed

        self._x = min(max(self._x, self.X_MIN), self.X_MAX)
        self._y = min(max(self._y, self.Y_MIN), self.Y_MAX)

        player.pos_update(self._x, self._y)

    def update(self, pressed_keys, events):
        pass


# FOR testing
test_player = PlayerLogic(0)
test_player2 = PlayerLogic(1)
test_player3 = PlayerLogic(2)
players = [test_player, test_player2, test_player3]
