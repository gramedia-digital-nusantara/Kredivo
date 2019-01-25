checkout_success_response = {
    "status": "OK",
    "message": "Checkout URL is created successfully.",
    "redirect_url": "https://sandbox.kredivo.com/kredivo/v2/signin?tk=uwBAsQVCKeA4NGCXOWUPfk+bCA39VPmilZrIugLjl2rB8tY+eZbGdq3Z8r7EUhikuv3hn1GECfsOZ2tZU9w/uX2nFLAtjGwK6lwkncKBeY4="
}

checkout_request_body = {
    "server_key": "123",
    "payment_type": "30_days",
    "transaction_details": {
        "amount": 6505000,
        "order_id": "12345",
        "items": [
            {
                "id": "BB12345678",
                "name": "iPhone 5S",
                "price": 6000000,
                "type": "Smartphone",
                "url": "http://merchant.com/cellphones/iphone5s_64g",
                "quantity": 1
            },
            {
                "id": "AZ14565678",
                "name": "Hailee Sneakers Blink Silver",
                "price": 250000,
                "url": "http://merchant.com/fashion/shoes/sneakers-blink-shoes",
                "type": "Sneakers",
                "quantity": 2,
                "parent_type": "SELLER",
                "parent_id": "SELLER456"
            },
            {
                "id": "taxfee",
                "name": "Tax Fee",
                "price": 1000,
                "quantity": 1
            },
            {
                "id": "shippingfee",
                "name": "Shipping Fee",
                "price": 9000,
                "quantity": 1,
                "parent_type": "SELLER",
                "parent_id": "SELLER456"
            },
            {
                "id": "discount",
                "name": "Discount",
                "price": 5000,
                "quantity": 1
            }
        ]
    },
    "customer_details": {
        "first_name": "Oemang",
        "last_name": "Tandra",
        "email": "alie@satuduatiga.com",
        "phone": "081513114262"
    },
    "billing_address": {
        "first_name": "Oemang",
        "last_name": "Tandra",
        "address": "Jalan Teknologi Indonesia No. 25",
        "city": "Jakarta",
        "postal_code": "12960",
        "phone": "081513114262",
        "country_code": "IDN"
    },
    "shipping_address": {
        "first_name": "Oemang",
        "last_name": "Tandra",
        "address": "Jalan Teknologi Indonesia No. 25",
        "city": "Jakarta",
        "postal_code": "12960",
        "phone": "081513114262",
        "country_code": "IDN"
    },
    "push_uri": "https://api.merchant.com/push",
    "back_to_store_uri": "https://merchant.com"
}

optional_data = {
    "sellers": [
        {
            "id": "SELLER123",
            "name": "Sunrise",
            "email": "sunrise@gmail.com",
            "url": "https://onlineshop/seller/sunrise",
            "address": {
                "first_name": "Irfan",
                "last_name": "Sutandro",
                "address": "Jalan Tentara Pelajar no 49",
                "city": "Jakarta Utara",
                "postal_code": "12960",
                "phone": "08123456789",
                "country_code": "IDN"
            }
        },
        {
            "id": "SELLER456",
            "name": "Toko Bagus",
            "email": "tokobagus@gmail.com",
            "url": "https://onlineshop/seller/tokobagus",
            "address": {
                "first_name": "Toto",
                "last_name": "Wahyuni",
                "address": "Jalan Krici raya IX",
                "city": "Jakarta Selatan",
                "postal_code": "12960",
                "phone": "08123456789",
                "country_code": "IDN"
            }
        }
    ],
}

# https://sandbox.kredivo.com/kredivo/v2/transaction/status
transaction_status = {
    "status": "OK",
    "legal_name": "",
    "fraud_status": "accept",
    "order_id": "KD14721",
    "transaction_time": 1547448500,
    "external_userid": "",
    "amount": "6505000.00",
    "payment_type": "30_days",
    "transaction_status": "pending",
    "message": "Transaction is pending",
    "transaction_id": "4a95f337-f15d-4e4c-b0ac-2fefa47dbf63"
}


# https://doc.kredivo.com/#cancel-purchase
cancel_transaction = {
    "server_key": "123",
    "order_id": "KD14721",
    "transaction_id": "6febc2b2-ac4f-462c-9e7e-56fc5da05d91",
    "cancellation_reason": "Out of stock",
    "cancelled_by": "Althea",
    "cancellation_date": "1501844808"
}

cancel_transaction_success = {
    "status": "OK",
    "fraud_status": "accept",
    "order_id": "KD14721",
    "transaction_time": 1542951231,
    "amount": "1500000.00",
    "payment_type": "30_days",
    "transaction_status": "settlement",
    "message": "Succes cancelling transaction by amount",
    "transaction_id": "69fe07ca-e055-4877-828a-a201a6729163"
}

cancel_transaction_failed = {
    "status": "ERROR",
    "message": "Transaction is already cancelled.",
    "fraud_status": "deny"
}


response_transaction_status = {
    "status": "OK",
    "legal_name": "TANDRA",
    "fraud_status": "accept",
    "order_id": "KD14721",
    "transaction_time": 1501846094,
    "amount": "1500100.00",
    "payment_type": "30_days",
    "transaction_status": "settlement",
    "message": "Confirmed order status. Valid!",
    "transaction_id": "fadee4e5-99a2-48d6-952d-007f3fa508e8",
    "merchant_id": "KFC",
    "outlet_id": "KFCSenayan"
}
