from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "ACff6ea5d45217ab52e2494a65a87bf649"
# Your Auth Token from twilio.com/console
auth_token  = "6b3aa15c548396b92f5d7317026e081f"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+61497453506", 
    from_="+19035056257",
    body="Hello from Python!")

print(message.sid)