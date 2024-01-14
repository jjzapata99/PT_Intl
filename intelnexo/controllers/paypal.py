from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest
from os import getenv
client_id = getenv("CLIENT_ID")
client_secret = getenv("CLIENT_SECRET")
env= SandboxEnvironment(client_id=client_id, client_secret=client_secret)
client = PayPalHttpClient(env)

# Genera la orden de pago, simplemente se agrego el monto dinamico

def create_url(mount: float):
    try:
        order = OrdersCreateRequest()
        order.prefer('return=representation')
        order.request_body({
            "intent": "CAPTURE",
            "purchase_units": [
                {
                    "amount": {
                        "currency_code": "USD",
                        "value": str(mount)
                    }
                }
            ]
        })
        response = client.execute(order)
        return {"id": response.result.id, "url":response.result.links[1].href}
    except Exception as e:
        print(f'{e}')
        return "Ocurrio un Error"