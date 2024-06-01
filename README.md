# Server (pi) instructions
1. Clone the repository onto your pi with the command `git clone https://github.com/Dragon863/Bookshelf-AI`
2. Run `cd Bookshelf-AI`
3. Install dependencies with `pip3 install requests isbnlib pyzbar google-books-api-wrapper python-dotenv` and `sudo apt install -y opencv-python`
4. Go to the [huggingface profile settings](https://huggingface.co/settings/tokens) and create a new token. Keep it for the next step.
5. Create a `.env` file with the contents `API_TOKEN=` followed by your token
6. You can now start the system by running `sh start.sh`

# Client (app) instructions
1. Clone the repository in the same way as before
2. [Install flutter](https://docs.flutter.dev/get-started/install)
3. In the app/lib/main.dart file, change line 43 (`await http.get(Uri.parse('http://192.168.1.67:5000/books'));`), replacing `192.168.1.67` with the IP of your raspberry pi.
4. You can now compile the app for android by running `flutter build apk --release` in the app/ folder
5. Install the APK on any device on your network, and it will connect to the pi
