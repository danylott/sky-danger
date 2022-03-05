import traceback
import time
import datetime

import configparser

# import pygame
# from pygame import mixer
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import MessageMediaPhoto

from call import perform_call
from check_danger import check_text_is_danger, check_image_is_danger


CHANNEL_LINK = "https://t.me/test_sky_danger"  # https://t.me/slavutych_mr for production
TICK_SECONDS = 5  # 60 for production
# REPEAT_ALARM_TIMES = 1  # use >5 for production


config = configparser.ConfigParser()
config.read("config.ini")

api_id = int(config["Telegram"]["api_id"])
api_hash = config["Telegram"]["api_hash"]

api_hash = str(api_hash)

phone = config["Telegram"]["phone"]
username = config["Telegram"]["username"]


def get_client():
    # Create the client and connect
    client = TelegramClient(username, api_id, api_hash)
    client.start()
    print("Client Created")
    # Ensure you're authorized
    if not client.is_user_authorized():
        client.send_code_request(phone)
        try:
            client.sign_in(phone, input("Enter the code: "))
        except SessionPasswordNeededError:
            client.sign_in(password=input("Password: "))

    return client


def get_last_message(client, channel):
    history = client(
        GetHistoryRequest(
            peer=channel,
            offset_id=0,
            offset_date=None,
            add_offset=0,
            limit=1,
            max_id=0,
            min_id=0,
            hash=0,
        )
    )
    messages = history.messages
    return messages[0]


def check_message_is_danger(client, message, datetime_str):
    text_message = message.message
    print("New message received:")
    print(text_message[:100] + "...(cut)")
    is_sky_danger = check_text_is_danger(text_message)
    print("Is sky danger text:", is_sky_danger)

    if message.media and isinstance(message.media, MessageMediaPhoto):
        print("Message is with image!")
        image_path = f"images/{datetime_str}.jpg"
        client.download_media(message.media, image_path)
        is_sky_danger_image = check_image_is_danger(image_path)
        print("Is sky danger image:", is_sky_danger_image)
        is_sky_danger = is_sky_danger or is_sky_danger_image

    return is_sky_danger


# def play_alarm():
#     for _ in range(REPEAT_ALARM_TIMES):
#         mixer.init()
#         mixer.music.load("sounds/siren.mp3")
#         mixer.music.play()
#         while mixer.music.get_busy():
#             pygame.time.Clock().tick(10)


def main():
    client = get_client()

    channel = client.get_entity(CHANNEL_LINK)

    last_message_id = None

    while True:
        try:
            datetime_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            print("Tick", datetime_str)

            message = get_last_message(client, channel)

            if last_message_id != message.id:
                last_message_id = message.id

                if check_message_is_danger(client, message, datetime_str):
                    perform_call()  # ALARM Call!
                    # play_alarm()  # ALARM!!! if needed

            time.sleep(TICK_SECONDS)
        except Exception as e:
            traceback.print_exc()
            print("Unexpected error!!!", e)


if __name__ == '__main__':
    main()
