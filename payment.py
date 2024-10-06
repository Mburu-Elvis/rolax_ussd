from intasend import APIService

publishable_key = ""
token = ""

service = APIService(token=token, publishable_key=publishable_key, test=True)

def pay_water_bill(phone_number, amount):
    number = phone_number.strip("+")
    amount = round(amount, 2)
    print(amount)
    response = service.collect.mpesa_stk_push(phone_number=number, email="", amount=amount, narrative="")
    print(response)