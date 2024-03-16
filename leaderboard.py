import requests
import logging


def get(scoreGetURL: str):
    try:
        response = requests.get(scoreGetURL)
        response.raise_for_status()

    except requests.RequestException as e:
        logging.warning(f"Error getting score kapow: {e}")
        if hasattr(e, "response") and e.response is not None:  # Fixing the typo here
            logging.warning(f"Server response: \n{e.response.text}")

    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)

    except requests.exceptions.Timeout as e:
        print("Request timeout:", e)

    else:
        return response.json()


def parse(data) -> str:
    if data is None:
        logging.warning(
            "Data for parse_leaderboard was None. Check for errors from get_leaderboard"
        )
        return "Was unable to connect to server\n Check the console for errors"
    outStr = ""

    for i in range(0, min(len(data), 10)):
        name = data[i].get("name")
        score = data[i].get("score")
        row = f"{(i+1)}. {name:<10} {score:>20}"
        outStr += row + "\n"

    return outStr


def submit_score(scorePosURL: str, name: str, score: float, uuid: str):
    try:
        json_data = {
            "name": name,
            "score": str(score),
            "UUID": uuid,
        }
        response = requests.post(
            scorePosURL, json=json_data, timeout=5
        )  # Set timeout to 5 seconds
        response.raise_for_status()  # Raise an error for bad response status codes (4xx or 5xx)
        logging.info("Score submitted successfully!")

    except requests.RequestException as e:
        logging.warning(f"Error submitting score kapow: {e}")
        if hasattr(e, "response") and e.response is not None:  # Fixing the typo here
            logging.warning(f"Server response: \n{e.response.text}")

    except requests.exceptions.ConnectionError as e:
        print("Connection error:", e)

    except requests.exceptions.Timeout as e:
        print("Request timeout:", e)

