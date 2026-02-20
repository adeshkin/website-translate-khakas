# Website Translate Khakas (TranslateKhak)

A web-based translation application for the Khakas language (Khakas ↔ Russian). This project provides a user-friendly interface for translating words and sentences, complete with a virtual keyboard for specific Khakas characters and text-to-speech capabilities.

## Features

- **Bidirectional Translation**: Translate text from Russian to Khakas and vice versa.
- **Virtual Keyboard**: On-screen keyboard for entering specific Khakas characters (`ғ`, `і`, `ң`, `ӧ`, `ӱ`, `ҷ`).
- **Responsive Design**: Works seamlessly on desktop and mobile devices.
- **Text-to-Speech**: Audio playback support for translations (WAV format).
- **Dictionary Lookup**: Efficient word lookup using a local SQLite database.
- **Smart Input**: Automatic resizing text areas, character counting, and copy-to-clipboard functionality.

## Tech Stack

- **Backend**: Python (Flask), SQLite
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Deployment**: Compatible with standard WSGI servers (Passenger) or Serverless environments (AWS Lambda/Yandex Cloud Functions).

## Project Structure

- `hello.py`: Main Flask application entry point. Handles HTTP requests and translation logic.
- `index.py`: Serverless handler (e.g., for AWS Lambda) for the translation logic.
- `index1.html`: Main HTML template file.
- `jsapp.js`: Client-side JavaScript for UI interactivity and AJAX calls.
- `styles.css`: CSS styles for the application.
- `translate.db`: SQLite database containing the translation dictionary.
- `static/`: Directory for static assets (images, SVGs).

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- SQLite3

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/website-translate-khakas.git
    cd website-translate-khakas
    ```

2.  Install dependencies:
    ```bash
    pip install flask requests
    ```

3.  Run the application locally:
    ```bash
    python hello.py
    ```

4.  Open your browser and navigate to `http://localhost:5000`.

## License

[MIT License](LICENSE)
