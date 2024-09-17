import africastalking


class SMS():
    
    def __init__(self):
        username = 'sandbox'
        self.sender = ""
        api_key = ''
        africastalking.initialize(username, api_key)
        self.sms = africastalking.SMS

    def sending(self, number, location, meter_id,message_type):
        # Set the numbers in international format
        recipients = [number]
        # Set your message
        message = ""
        
        if message_type == 1:
            message = f"""OUTAGE ALERT:\n
            A water outage has been reported at {location}, affecting meter number {meter_id}.\n
            Please investigate and take immediate action.\n
            For more details, contact {number}."""
        elif message_type == 2:
            message = f"""LEAKAGE ALERT:\n
            A water outage has been reported at {location}, affecting meter number {meter_id}.\n
            Please investigate and take immediate action.\n
            For more details, contact {number}.
            """
        
        try:
            response = self.sms.send(message, recipients, self.sender)
            print (response)
        except Exception as e:
            print (f'Houston, we have a problem: {e}')