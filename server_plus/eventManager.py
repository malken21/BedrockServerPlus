import server_plus.events.player as player
import server_plus.events.server as server
import server_plus.events.weather as weather

from server_plus.events.default import event

import server_plus.process as process


class events:
    def __init__(self, config, process: process.server):
        self.events = [
            player.PlayerDisconnect(config),
            player.PlayerConnect(config),
            server.ServerStart(config),
            server.ServerStop(config),
            weather.WeatherUpdate(config, process)
        ]

    def get(self) -> list[event]:
        return vars(self).values()


def run(events: list[event], text: str):
    LogOutput = True
    for event in events:
        event.setLogOutput(LogOutput)
        event.run(text)
        LogOutput = event.isLogOutput()
    return LogOutput
