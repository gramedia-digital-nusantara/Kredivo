
class KredivoCheckoutError(Exception):
    def __init__(self, message, kind, **kwargs):
        self.message = message if len(message) else "An unknown error occurred"
        self.kind = kind
        self.additional_error_attrs = kwargs

    def __str__(self):
        return "<KredivoCheckoutError(message={message}, kind={kind})>".format(**vars(self))


class KredivoUnexpectedError(Exception):
    def __init__(self, status_code, **kwargs):
        self.message = "Kredivo doesn't response our checkout request"
        self.status_code = status_code

    def __str__(self):
        return "<KredivoUnexpectedError(message={message}, status_code={status_code})>".format(**vars(self))


class KredivoCancelOrderException(Exception):

    def __init__(self, json_response, **kwargs):
        if json_response.get("error"):
            self.message = json_response.get("error").get("message")
        else:
            self.message = json_response.get("message")
        self.status = json_response.get("status")

    def __str__(self):
        return "<KredivoCancelOrderException(message={message}, kind={kind})>".format(**vars(self))
