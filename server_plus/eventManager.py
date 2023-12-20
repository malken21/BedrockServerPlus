import server_plus.events.player as player
import server_plus.events.server as server
import server_plus.events.weather as weather
from server_plus.events.default import event


def getEvents(config) -> list[event]:
    return [
        player.PlayerDisconnect(config),
        player.PlayerConnect(config),
        server.ServerStart(config),
        server.ServerStop(config),
        weather.WeatherUpdate(config)
    ]


def run(config, text: str):

    # すべてのイベントを取得
    events = getEvents(config)

    LogOutput = True
    for event in events:
        event.setLogOutput(LogOutput)
        event.run(text)
        LogOutput = event.isLogOutput()
    return LogOutput
