# GeoSense - Geospatial Query System

## Project Description
**GeoSense** is a system designed to identify geospatial names using DistilBERT for Named Entity Recognition (NER) and FuzzyWuzzy for spelling correction. It supports multilingual speech-to-text input and integrates with APIs for geospatial data access and processing. The results are displayed on a user-friendly web interface built with Flask.

### Key Features
- Identifies geospatial names using DistilBERT
- Corrects spelling using FuzzyWuzzy
- Supports multilingual speech-to-text input
- Integrates with APIs for geospatial data access
- Displays results on a map in a web interface

## Installation

### Prerequisites
- Python 3.7 or higher
- Flask
- Torch
- Transformers
- FuzzyWuzzy
- DeepTranslator

### Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/Benston-Daniel/GeoSense.git
   cd GeoSense
   ```

2. **Install the required Python packages:**

3. **Run the Flask application:**
   ```bash
   python web_app.py
   ```

## Usage

1. **Open the web application:**
   Open your web browser and go to `http://127.0.0.1:5000/`.

2. **Enter your query:**
   You can either type your query or use the microphone to input your query via speech.

3. **Select the language:**
   Choose the appropriate language from the dropdown menu.

4. **View the results:**
   The system will display the identified geospatial names along with their canonical names, place types, and links to Google Maps and Wikipedia.

### Example

![Home Page](static/homepage.jpeg)
*Home Page of GeoSense*

![Results Page](static/result.jpeg)
*Results Page displaying identified geospatial names*

## Project Structure

- `app.py`: Main Flask application
- `templates/`: HTML templates for the web pages
  - `index.html`: Home page
  - `results.html`: Results page
- `static/`: Static files (CSS, JavaScript, images, video)
  - `style.css`: Custom styles for the web pages
  - `script.js`: JavaScript for handling dropdown and speech recognition
- `Datasets/`: Directory containing the place names dataset
  - `place_name.csv`: CSV file with place names and their details

## How It Works

1. **Named Entity Recognition (NER):**
   - The user inputs a query.
   - The DistilBERT model identifies geospatial names in the query.

2. **Spelling Correction:**
   - The system uses FuzzyWuzzy to correct any spelling mistakes in the identified names.

3. **Multilingual Support:**
   - The system supports speech-to-text input in multiple languages.
   - It uses Google Translator to translate the input to English if needed.

4. **Data Access and Processing:**
   - The system integrates with APIs to access and process geospatial data.
   - It links the identified names to Google Maps and Wikipedia for more information.
