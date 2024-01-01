import requests, datetime, magic

def get_session(username: str, app_password: str) -> dict|None:
    """
    Attempt to authenticate to Bluesky given the specified username and app password.

    Args:
        username: The username of the account to sign in to.
        app_password: An app password for the account.

    Returns:
        A session dict if authentication was successful and None otherwise.
    """
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.server.createSession",
        json={"identifier": username, "password": app_password},
    )

    if resp.status_code != 200:
        return None
    return resp.json()

def construct_post(img_blob: dict, date: str) -> dict:
    """
    Construct a Bluesky post for the given image, but does not post it.

    Args:
        image: The image to post to Bluesky.

    Returns:
        The post represented as a dict.
    """

    now = datetime.datetime.now(datetime.timezone.utc).isoformat().replace("+00:00", "Z")
    return {
        "$type": "app.bsky.feed.post",
        "text": f"Daily Loss for {date}",
        "createdAt": now,
        "embed": {
            "$type": "app.bsky.embed.images",
            "images": [{
                "alt": "",
                "image": img_blob
            }]
        }
    }

def upload_image(image: str, accessJwt: str):
    """
    Upload the specified image to Bluesky.

    Args:
        image: The path to the image that is going to be uploaded.
        accessJwt: The JWT for the current session.
    """
    # Get the MIME type of the image
    mime = magic.Magic(mime=True)
    mime_type = mime.from_file(image)

    with open(image, "rb") as f:
        img_bytes = f.read()

    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.uploadBlob",
        headers={
            "Content-Type": mime_type,
            "Authorization": "Bearer " + accessJwt
        },
        data=img_bytes
    )
    return resp.json()["blob"]

def run(image: str, secrets: dict, date: str):
    # Sign in
    session = get_session(secrets["username"], secrets["password"])

    # Upload the image
    img_blob = upload_image(image, session["accessJwt"])

    # Construct the post
    post = construct_post(img_blob, date)

    # Actually post it
    resp = requests.post(
        "https://bsky.social/xrpc/com.atproto.repo.createRecord",
        headers={"Authorization": "Bearer " + session["accessJwt"]},
        json={
            "repo": session["did"],
            "collection": "app.bsky.feed.post",
            "record": post
        }
    )