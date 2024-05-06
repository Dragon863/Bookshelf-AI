from flask import Flask, jsonify
import json
import os

app = Flask(__name__)

json_file_path = "books.json"


def load_books_data():
    """
    Load the books data from the JSON file.
    """
    if os.path.exists(json_file_path):
        with open(json_file_path, "r") as file:
            return json.load(file)
    else:
        return {}


@app.route("/books", methods=["GET"])
def get_books():
    """
    Route to get the books data from the JSON file.
    """
    books_data = load_books_data()
    return jsonify(books_data)


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0")
