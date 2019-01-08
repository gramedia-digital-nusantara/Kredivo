

class KredivoGateway:
    def __init__(self, server_key, use_sandbox=False):
        self.server_key = server_key
        self.use_sandbox = use_sandbox

    @property
    def base_url(self):
        return "https://sandbox.kredivo.com/kredivo/" if self.use_sandbox \
            else "https://api.kredivo.com/kredivo"

