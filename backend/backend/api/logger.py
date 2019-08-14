from websocket import create_connection


class Logger:
    msg_placeholder = "{\"message\": \"%s\"}"

    def __init__(self, channel):
        self.ws = create_connection("ws://alpharithmic.herokuapp.com/ws/logs/%s/" % channel)

    def __del__(self):
        self.ws.close()

    def log(self, msg):
        self.ws.send(Logger.msg_placeholder % msg)

    def close(self):
        self.ws.close()
