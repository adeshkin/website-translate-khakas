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



## Back-end (Microservices)

The project uses a microservices architecture to handle translation and text-to-speech tasks. These services are located in the `translator_tts` directory and communication is orchestrated via a gateway service.

### Services Overview
1.  **Gateway Service** (`translator_tts/app.py`):
    -   **Port**: `13000`
    -   **Role**: Acts as the main entry point for translation requests. It routes traffic to the appropriate specific translation service (Khakas-Russian or Russian-Khakas) or the TTS service.
2.  **Khakas -> Russian Translation Service** (`translator_tts/translator/kjh_to_ru.py`):
    -   **Port**: `13001`
    -   **Role**: Uses a Transformer-based Neural Machine Translation (NMT) model to translate Khakas text to Russian.
3.  **Russian -> Khakas Translation Service** (`translator_tts/translator/ru_to_kjh.py`):
    -   **Port**: `13002`
    -   **Role**: Uses a Transformer-based NMT model to translate Russian text to Khakas.
4.  **Text-to-Speech Service** (`translator_tts/text_to_speech/kjh.py`):
    -   **Port**: `13003`
    -   **Role**: Uses a Silero-based TTS model to synthesize Khakas speech from text.

### Important Note on Models
The translation and TTS scripts currently reference hardcoded paths to model checkpoints (e.g., `.pt` files). You **must** update these paths in the respective Python files (`kjh_to_ru.py`, `ru_to_kjh.py`, `kjh.py`) to point to the actual location of your trained models on your local machine.

---

## Getting Started

### Prerequisites

-   Python 3.8+
-   Flask
-   SQLite3
-   **Model Checkpoints**: You need the pre-trained PyTorch models for translation and TTS.

### Installation & Setup

#### 1. Main Web Application
1.  Clone the repository:
    ```bash
    git clone https://github.com/adeshkin/website-translate-khakas.git
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

#### 2. Translation Services
Due to potential dependency conflicts (different PyTorch versions), it is recommended to use separate virtual environments.

**Khakas <-> Russian Translators:**
1.  Navigate to the translator directory:
    ```bash
    cd translator_tts/translator
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Update Model Paths**: Edit `kjh_to_ru.py` and `ru_to_kjh.py` to point to your local model files.
5.  Run the services (you may need to run them in separate terminals or background processes):
    ```bash
    python kjh_to_ru.py &
    python ru_to_kjh.py &
    ```

#### 3. Text-to-Speech Service
1.  Navigate to the TTS directory:
    ```bash
    cd ../text_to_speech  # from translator directory
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the service:
    ```bash
    python kjh.py
    ```

#### 4. Gateway Service
1.  Navigate to the main `translator_tts` directory:
    ```bash
    cd ../..  # back to translator_tts root
    ```
2.  Create and activate a virtual environment:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the gateway app:
    ```bash
    python app.py
    ```

## License

[MIT License](LICENSE)

