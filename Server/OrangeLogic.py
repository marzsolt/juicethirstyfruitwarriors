import PlayerLogic
import client_message_constants as climess


class OrangeLogic(PlayerLogic.PlayerLogic):
    def __init__(self, player_id, terrain):
        super(OrangeLogic, self).__init__(player_id, terrain)

    def _process_requests(self, network_messages):
        super()._process_requests(network_messages)
        for mess in network_messages:
            if mess.type == climess.MessageType.APPLE_ATTACK:
                self._attack()

    def _attack(self):
        if super()._attack():
            # TODO
            return True
        return False
