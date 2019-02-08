Quickstart
==========

Before using this library, you need a merchant account with `Kredivo <https://kredivo.com>`_.

After you have an account, if you want create order with Kredivo payment.
you want write code like this..

.. code-block:: python

    from kredivo import KredivoGateway
    from kredivo.models import KredivoStatus

    kredivo = KredivoGateway(
        server_key='s3cr3t',
        use_sandbox=True
    )

    kredivo_requests = {
        "payment_type":"30_days",
        "tokenize_user": False,
        "user_token" : "XXXX-XXXX",
        "transaction_details": {
            "amount":6505000,
            "order_id":"KD14721",
            "items": [
                {
                    "id":"BB12345678",
                    "name":"iPhone 5S",
                    "price":6000000,
                    "type":"Smartphone",
                    "url":"http://merchant.com/cellphones/iphone5s_64g",
                    "quantity":1
                },
                {
                    "id":"shippingfee",
                    "name":"Shipping Fee",
                    "price":9000,
                    "quantity":1,
                    "parent_type":"SELLER",
                    "parent_id":"SELLER456"
                },
                {
                    "id":"discount",
                    "name":"Discount",
                    "price":5000,
                    "quantity":1
                }
            ]
        },
        "customer_details":{
            "first_name":"Oemang",
            "last_name":"Tandra",
            "email":"alie@satuduatiga.com",
            "phone":"081513114262"
        },
        "shipping_address": {
            "first_name":"Oemang",
            "last_name":"Tandra",
            "address":"Jalan Teknologi Indonesia No. 25",
            "city":"Jakarta",
            "postal_code":"12960",
            "phone":"081513114262",
            "country_code":"IDN"
        },
        "push_uri":"https://api.merchant.com/push",
        "back_to_store_uri":"https://merchant.com"
    }

    kredivo_response = kredivo.checkout(kredivo_request)

    if kredivo_response.status == KredivoStatus.OK:
        url_payment = kredivo_response.redirect_url
        # send redirect url to the browser so the client can be redirected

