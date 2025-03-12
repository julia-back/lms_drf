import requests
from config.settings import PAYMENT_STRIPE_API_KEY


class PaymentLink:

    def __init__(self, product_obj, user_obj=None):
        self.user_obj = user_obj
        self.product_obj = product_obj
        self.api_token = PAYMENT_STRIPE_API_KEY
        self.headers = {"Authorization": f"Bearer {self.api_token}"}

    def get_payment_link(self):
        if self.user_obj:
            customer_id = self.create_customer()
        else:
            customer_id = None
        product_id = self.create_product()
        price_id = self.create_price(product_id)
        payment_link = self.create_payment_session(price_id, customer_id=customer_id)
        return payment_link

    def create_customer(self):
        url = "https://api.stripe.com/v1/customers"
        data = {"email": self.user_obj.email, "name": self.user_obj.username, "phone": self.user_obj.phone_number}
        response = requests.post(url, headers=self.headers, data=data)
        customer_id = response.json().get("id")
        return customer_id

    def create_product(self):
        url = "https://api.stripe.com/v1/products"
        data = {"name": self.product_obj.name, "description": self.product_obj.description}
        response = requests.post(url, headers=self.headers, data=data)
        product_id = response.json().get("id")
        return product_id

    def create_price(self, product_id):
        url = "https://api.stripe.com/v1/prices"
        data = {"currency": "usd", "product": product_id, "unit_amount": int(self.product_obj.price * 100)}
        response = requests.post(url, headers=self.headers, data=data)
        price_id = response.json().get("id")
        return price_id

    def create_payment_session(self, price_id, customer_id=None):
        url = "https://api.stripe.com/v1/checkout/sessions"
        data = {"customer": customer_id,
                "line_items[0][price]": price_id,
                "line_items[0][quantity]": 1,
                "mode": "payment",
                "success_url": "https://example.com/success"}
        response = requests.post(url, headers=self.headers, data=data)
        payment_link = response.json().get("url")
        return payment_link


def get_payment_link(user=None, product=None):
    # проверка наличия пользователя
    # создание пользователя
    url = "https://api.stripe.com/v1/customers"
    headers = {"Authorization": f"Bearer {PAYMENT_STRIPE_API_KEY}"}
    data = {"email": user.email, "name": user.username, "phone": user.phone_number}
    response = requests.post(url, headers=headers, data=data)
    ret_user = response.json().get("id")
    # создание продукта
    url = "https://api.stripe.com/v1/products"
    data = {"name": product.name, "description": product.description}
    response = requests.post(url, headers=headers, data=data)
    ret_product = response.json().get("id")
    # создание цены
    url = "https://api.stripe.com/v1/prices"
    data = {"currency": "usd", "product": ret_product, "unit_amount": int(product.price * 100)}
    response = requests.post(url, headers=headers, data=data)
    ret_price = response.json().get("id")
    # создание сессии
    url = "https://api.stripe.com/v1/checkout/sessions"
    data = {"customer": ret_user,
            "line_items[0][price]": ret_price,
            "line_items[0][quantity]": 1,
            "mode": "payment",
            "success_url": "https://example.com/success"}
    response = requests.post(url, headers=headers, data=data)
    ret_session = response.json().get("url")
    # получение ссылки на оплату
    return ret_session
