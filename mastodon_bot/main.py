from mastodon import Mastodon

def run(image: str, secrets: dict, date: str):
    client = Mastodon(api_base_url="https://mastodon.social", access_token=secrets["access-token"])

    media = client.media_post(image, focus=(0,0))
    client.status_post(f"Daily Loss for {date}", media_ids=[media["id"]])
