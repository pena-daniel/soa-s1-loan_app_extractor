import requests

def post(payload: dict, url: str) -> dict:
    """
    Post api call

    Args:
        payload (dict): _payload to send
        url (str): _url of the api

    Returns:
        dict: _response from the api
    """
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json()
        else:
            return {"erreur": f"Problem to reach the service with status {response.status_code}"}
    except Exception as e:
        return {"erreur": str(e)}