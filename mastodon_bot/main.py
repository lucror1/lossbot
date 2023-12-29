from mastodon import Mastodon

def run(image: str, secrets: dict):
    client = Mastodon(api_base_url="https://mastodon.social", access_token=secrets["access-token"])

    media = client.media_post(image, focus=(0,0))
    client.status_post("Testing randomized images", media_ids=[media["id"]])
