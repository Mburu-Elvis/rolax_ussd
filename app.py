import os
from flask import Flask, request, jsonify, Response
from urllib import parse
import psycopg2
from payment import pay_water_bill
from messaging import SMS

app = Flask(__name__)

pwd = parse.quote("")
conn = psycopg2.connect(f"postgresql://rolax:{pwd}@localhost:5432/")
cur = conn.cursor()

@app.route("/ussd", methods = ['POST'])
def ussd():
    # Read the variables sent via POST from our API
    session_id   = request.values.get("sessionId", None)
    serviceCode  = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text         = request.values.get("text", "default")
    unit_price   = 100

    if text == '':
        # This is the first request. Note how we start the response with CON
        response  = "CON Welcome to NAWASCO.\n"
        response += "1. Meter Reading \n"
        response += "2. Pay Water Bill\n"
        response += "3. Report Issue\n"
        response += "0. Exit"
    elif text == '0':
        response = "END Bye"
    elif text == '1':
        # Business logic for first level response
        usage = meter_reading(phone_number)
        response  = f"END Your meter reading is {usage['usage']:0.2f} units \n"
    elif text == '2':
        # This is a terminal request. Note how we start the response with END
        usage = meter_reading(phone_number)
        amount = unit_price * usage['usage']
        pay_water_bill(phone_number=phone_number, amount=amount)
        response = "END payment completed"
    elif text == "3":
        response = "CON Which issue are you reporting:\n"
        response += "1. Water outage\n"
        response += "2. Pipe leakage\n"
    elif text == '1*1':
        # This is a second level response where the user selected 1 in the first instance
        accountNumber  = "ACC1001"
        # This is a terminal request. Note how we start the response with END
        response = "END Your account number is " + accountNumber
    elif text == '3*1':
        sms = SMS()
        sms.sending(number=phone_number, location="Juja", meter_id="541", message_type=1)
        response = "END Issue reported."
    elif text == '3*2':
        sms = SMS()
        sms.sending(number=phone_number, location="Juja", meter_id="541", message_type=1)
        response = "END Issue reported."
    else :
        response = "END Invalid choice"

    # Send the response back to the API
    return response

@app.route("/incoming-messages", methods=['POST'])
def incoming_messages():
    data = request.get_json(force=True)
    print(f'Incoming message...\n ${data}')
    return Response(status=200)


def meter_reading(phone_number):
    query = """
    SELECT usage FROM usages
    INNER JOIN users ON usages.meter_id = users.meter_id
    WHERE users.phone_number = %s
    """
    cur.execute(query, (phone_number,))

    row = cur.fetchone()
    
    colnames = [desc[0] for desc in cur.description]
    usage = dict(zip(colnames, row))
    
    return usage

if __name__ == '__main__':
    app.run(debug=True)