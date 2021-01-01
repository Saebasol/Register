import requests
import argparse
import os

parser = argparse.ArgumentParser("register")

comment = parser.add_argument("--comment", type=str)

args = parser.parse_args()

user_id = args.comment.replace("/approve ", "")

response = requests.post("https://doujinshiman.ga/v3/api/register", json={"user_id": user_id }, headers={"Verification": os.environ["VERIFI"]})

if response.status_code == 201:
    print("Success Register")