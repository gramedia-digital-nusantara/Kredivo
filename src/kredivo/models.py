class SerializableMixin(object):
    """
    An instance that can return a dictionary representation of it's
    properties by calling a serialize() method.
    """
    def serialize(self):
        """
        Returns a dictionary representation of an object
        """
        rv = {}
        for key in self.__dict__:
            val = getattr(self, key)

            if hasattr(val, 'serialize'):
                rv[key] = val.serialize()
            else:
                rv[key] = val

        return rv


class TransactionDetail(SerializableMixin):

    def __init__(self, amount, order_id, items):
        self.amount = amount
        self.order_id = order_id
        self.items = items

    def serialize(self):
        rv = super(TransactionDetail, self).serialize()
        rv.update({"items": [
            item.serialize() for item in self.items
        ]})
        return rv


class ItemDetail(SerializableMixin):

    def __init__(self, id, name, price, type, quantity, url):
        self.id = id
        self.name = name
        self.price = price
        self.type = type
        self.quantity = quantity
        self.url = url


class CustomerDetail(SerializableMixin):

    def __init__(self, first_name, last_name, email, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone = phone


class Address(SerializableMixin):

    def __init__(self, first_name="", last_name="", address="", phone="", city="", country_code="", postal_code=""):
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.phone = phone
        self.city = city
        self.country_code = country_code
        self.postal_code = postal_code


class KredivoCheckoutEntity(SerializableMixin):

    def __init__(self, transaction_details, customer_details, push_uri, back_to_store_uri):
        self.transaction_details = transaction_details
        self.customer_details = customer_details
        self.billing_address = Address()
        self.shipping_address = Address()
        self.push_uri = push_uri
        self.back_to_store_uri = back_to_store_uri


class KredivoTransactionResponse(SerializableMixin):

    def __init__(self, response):
        json_response = response.json()
        self.response = self.api_response(response)
        for key in json_response:
            setattr(self, key, json_response[key])

    @staticmethod
    def api_response(response):
        return response
