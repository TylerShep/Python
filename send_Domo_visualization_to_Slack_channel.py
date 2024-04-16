import os
import random
import requests
from PIL import Image

class DomoApi:
    def __init__(self, api_token):
        self.api_token = api_token

    def get_dashboard(self, dashboard_id):
        url = f"https://api.domo.com/v1/pages/{dashboard_id}?access_token={self.api_token}"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def get_card_image(self, card_id):
        url = f"https://api.domo.com/v1/cards/{card_id}/image?access_token={self.api_token}"
        response = requests.get(url)
        response.raise_for_status()
        return response.content

class SlackApi:
    def __init__(self, api_token):
        self.api_token = api_token

    def upload_file(self, file_content, file_name):
        url = "https://slack.com/api/files.upload"
        files = {"file": (file_name, file_content, "image/png")}
        response = requests.post(url, files=files, data={"initial_comment": "Here is the card visualization:"}, headers={"Authorization": f"Bearer {self.api_token}"})
        response.raise_for_status()
        return response.json()["file"]["id"]

    def send_message(self, channel_id, message):
        url = "https://slack.com/api/chat.postMessage"
        response = requests.post(url, json={"channel": channel_id, "text": message}, headers={"Authorization": f"Bearer {self.api_token}"})
        response.raise_for_status()

def main():
    # Set up Domo API connection
    domo_api = DomoApi(os.environ["DOMO_API_TOKEN"])

    # Get all card IDs from a dashboard
    dashboard_id = "your-dashboard-id-here"
    dashboard = domo_api.get_dashboard(dashboard_id)
    card_ids = [card["id"] for card in dashboard["cards"]]

    # Get the image for a random card
    card_id = random.choice(card_ids)
    card_image = domo_api.get_card_image(card_id)

    # Set up Slack API connection
    slack_api = SlackApi(os.environ["SLACK_API_TOKEN"])

    # Upload the image to Slack
    file_id = slack_api.upload_file(card_image, "card_image.png")

    # Send a message to Slack with the file ID
    channel_id = "#your-channel-id-here"
    message = f"Here is the card visualization: <{file_id}>"
    slack_api.send_message(channel_id, message)

if __name__ == "__main__":
    main()
