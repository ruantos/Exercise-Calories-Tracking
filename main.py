import requests
import datetime as dt
import os

NUTRI_ENDPOINT = "https://trackapi.nutritionix.com/v2/natural/exercise"
NUTRI_HEADERS = {
    "x-app-id": os.environ.get("api_id"),
    "x-app-key": os.environ.get("api_key")
}
SHEETY_HEADERS = {
    "Authorization": f"Bearer {os.environ.get('sheety_token')}"
}


def get_date():
    today = dt.datetime.now()
    date = today.strftime("%d/%m/%Y")
    return date


def get_hour():
    today = dt.datetime.now()
    hour = today.strftime("%X")
    return hour


def get_info():
    PARAMETERS = {
        "query": str(input()),
        "gender": "male",
        "weight_kg": "70",
        "height_cm": "177",
        "age": "21"
    }
    response = requests.post(url=NUTRI_ENDPOINT, json=PARAMETERS, headers=NUTRI_HEADERS)
    response.raise_for_status()
    return response.json()


def post_exercise():
    results = get_info()
    print(results)
    for exercise in results["exercises"]:
        row = {
            "workout": {
                "date": get_date(),
                "time": get_hour(),
                "exercise": exercise["name"].title(),
                "duration": exercise["duration_min"],
                "calories": exercise["nf_calories"]
            }
        }

        response = requests.post("https://api.sheety.co/24b450108fe68fbd5786567c0a23a9db/workoutTracking/workouts", json=row, headers=SHEETY_HEADERS)        
        response.raise_for_status()


post_exercise()