import configparser

from twilio.rest import Client


config = configparser.ConfigParser()
config.read("config.ini")

twilio_account_sid = config["Twilio"]["twilio_account_sid"]
twilio_auth_token = config["Twilio"]["twilio_auth_token"]
twilio_bin_url = config["Twilio"]["twilio_bin_url"]
twilio_phone_number = config["Twilio"]["twilio_phone_number"]
personal_phone_number = config["Twilio"]["personal_phone_number"]

client = Client(
    username=twilio_account_sid,
    password=twilio_auth_token
)


def perform_call():
    client.calls.create(
        from_=twilio_phone_number,
        to=personal_phone_number,
        url=twilio_bin_url
    )
