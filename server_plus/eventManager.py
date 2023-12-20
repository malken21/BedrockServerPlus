from server_plus.events.default import event


class events:
    def get(self) -> list[event]:
        return vars(self).values()


def run(events: list[event], text: str):
    LogOutput = True
    for event in events:
        event.setLogOutput(LogOutput)
        event.run(text)
        LogOutput = event.isLogOutput()
    return LogOutput
