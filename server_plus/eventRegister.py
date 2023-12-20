from server_plus.eventManager import events


import server_plus.events.player as player
import server_plus.events.server as server
import server_plus.events.weather as weather


class EventList(events):
    def __init__(self, config, process):

        self.WeatherUpdate = weather.WeatherUpdate(config, process)
        self.PlayerDisconnect = player.PlayerDisconnect(config)
        self.PlayerConnect = player.PlayerConnect(config)
        self.ServerStart = server.ServerStart(config)
        self.ServerStop = server.ServerStop(config)
