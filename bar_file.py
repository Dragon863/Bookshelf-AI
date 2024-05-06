import os
import json
from random import randint
from pyzbar import pyzbar
import cv2
import time
import isbnlib
import requests
from dotenv import load_dotenv
from google_books_api_wrapper.api import GoogleBooksAPI

load_dotenv()

API_URL = (
    "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
)
API_TOKEN = os.getenv("API_TOKEN")
headers = {"Authorization": f"Bearer {API_TOKEN}"}

bookClient = GoogleBooksAPI()


def llm(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


def load_or_create_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            return json.load(file)
    else:
        return {}


def write_to_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


# Initialize the JSON file path
json_file_path = "books.json"

# Load or create the JSON file
books_data = load_or_create_json(json_file_path)

vs = cv2.VideoCapture(0)
time.sleep(2)

while True:
    _status, image = vs.read()
    barcodesList = pyzbar.decode(image)
    for barcode in barcodesList:
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        if isbnlib.is_isbn10(barcodeData) or isbnlib.is_isbn13(barcodeData):
            meta = isbnlib.meta(barcodeData, "openl")
            print(meta)
            title = meta["Title"]
            author = meta["Authors"][0]
            print(f"Detected: {title} by {author}")

            # Check if the book is already in the JSON file
            if title not in books_data:
                output = llm(
                    {
                        "inputs": f"[INST] Random seed: {randint(1, 255)} You are a helpful assistant which provides a book recommendation based on the title given. Do not give any extra information. Do not give the context again in your response\nAlways ensure your recommendations are real books\n\nTitle: Ready Player One by Ernest Cline\nRecommendation: The Maze Runner by James Dashner\n\nTitle: {title} by {author}\nRecommendation:  [/INST]",
                        "parameters": {"return_full_text": False},
                        "wait_for_model": True,
                    }
                )
                recommendation = str(output[0]["generated_text"]).split("\n")[0]
                print(recommendation)
                recommendation_object = bookClient.get_book_by_title(recommendation)
                print(recommendation_object.title)
                print(recommendation_object.description)
                print(recommendation_object.authors)
                print(recommendation_object.large_thumbnail)

                books_data = {
                    "title": title,
                    "author": author,
                    "recommendation": recommendation,
                    "recommendation_object": {
                        "title": recommendation_object.title,
                        "description": recommendation_object.description,
                        "authors": recommendation_object.authors,
                        "large_thumbnail": recommendation_object.large_thumbnail,
                    },
                }

                if "title" in load_or_create_json("books.json").keys():
                    if load_or_create_json("books.json")["title"] == title:
                        pass
                    else:
                        write_to_json(json_file_path, books_data)
                else:
                    write_to_json(json_file_path, books_data)

    cv2.imshow("Image", image)
    cv2.waitKey(10)
