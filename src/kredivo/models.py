class SerializableMixin(object):
    """
    An instance that can return a dictionary representation of it's
    properties by calling a serialize() method.
    """
    __fields__ = []

    def __init__(self, response):
        self._original_response = response
        for key in self.__fields__:
            setattr(self, key, response.json()[key])

    def __iter__(self):
        for key in self.__fields__:
            yield (key, 'Value for {}'.format(key))

    def serialize(self):
        """
        Returns a dictionary representation of an object
        """
        rv = {}
        for key in self.__fields__:
            val = getattr(self, key)

            if hasattr(val, 'serialize'):
                rv[key] = val.serialize()
            else:
                rv[key] = val

        return rv


class TransactionDetail(SerializableMixin):

    __fields__ = ["amount", "order_id", "items"]

    def serialize(self):
        rv = super(TransactionDetail, self).serialize()
        rv.update({"items": [
            item.serialize() for item in self.items
        ]})
        return rv


class ItemDetail(SerializableMixin):
    __fields__ = ["id", "name", "price", "type", "quantity", "url"]


class CustomerDetail(SerializableMixin):
    __fields__ = ["first_name", "last_name", "email", "phone"]


class Address(SerializableMixin):

    __fields__ = ["first_name", "last_name", "address", "phone", "city", "country_code", "postal_code"]


class KredivoCheckoutEntity(SerializableMixin):
    __fields__ = ["transaction_details", "customer_details", "push_uri", "back_to_store_uri"]


class KredivoTransactionResponse(SerializableMixin):

    __fields__ = ["status", "legal_name", "fraud_status", "order_id", "transaction_time", "external_userid",
                 "amount", "payment_type", "transaction_status", "message", "transaction_id"]


class CancelPurcaseResponse(SerializableMixin):

    __fields__ = ["status", "fraud_status", "order_id", "transaction_time", "amount", "payment_type",
                  "transaction_status", "message", "transaction_id"]
