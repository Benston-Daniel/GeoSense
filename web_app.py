from flask import Flask, request, render_template, jsonify
import torch
from transformers import DistilBertTokenizer, DistilBertForTokenClassification
from transformers import pipeline
import csv
from fuzzywuzzy import fuzz
from urllib.parse import quote
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Load NER model (safetensor)
model_dir = 'DistilBert_conll03'
tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
model = DistilBertForTokenClassification.from_pretrained(model_dir)
ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer)

# For Fuzzy
similarity_threshold = 80

def load_dataset(file_path):
    dataset = []
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['other-names'] = [name.strip() for name in row['other-names'].split(',')]
            dataset.append(row)
    return dataset

# Load the validation dataset
dataset = load_dataset('Datasets\place_name.csv')

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/results", methods=["GET", "POST"])
def show_results():
    if request.method == "POST":
        text = request.form.get("searchInput")  # Update to match the input name from the HTML
        if text:
            print("Inside Results", text)
            return process_text(text)
    return render_template("results.html", results=[])


# @app.route("/results", methods=["GET", "POST"])
def process_text(text):
    # Run NER
        # if request.method == "POST":
        # text = request.form.get("text")
    ner_results = ner_pipeline(text)
    print("ner_results::::::",ner_results)
    # Function to aggregate subwords
    def aggregate_subwords(current_entity, final_entities):
        if current_entity:
            entity_word = ''.join([word.replace('##', '') for word in current_entity["words"]])
            final_entities.append(entity_word)

    current_entity = {}
    final_entities = []
    previous_entity = None

    for entity in ner_results:
        if entity['entity'] in ['B-LOC', 'I-LOC']:
            word = entity['word'].replace('##', '')
            if entity['word'].startswith('##') or entity['word'].endswith('-') or (current_entity.get("words") and current_entity["words"][-1].endswith('-')):
                current_entity["words"].append(word)
            elif previous_entity == 'B-LOC' and entity['entity'] == 'I-LOC':
                current_entity["words"].append(word)
            else:
                aggregate_subwords(current_entity, final_entities)
                current_entity = {"words": [word]}
            previous_entity = entity['entity']
        else:
            previous_entity = None

    aggregate_subwords(current_entity, final_entities)

    # Perform fuzzy matching for each extracted entity and add links
    results = []
    for extracted_name in final_entities:
        best_match = perform_fuzzy_matching(extracted_name, dataset)
        if best_match:
            canonical_name = best_match["canonical name"]
            place_type = best_match["place-type"]
            other_names = ', '.join(best_match["other-names"])

            # Create links to Google Maps and Wikipedia
            google_maps_link = f"https://www.google.com/maps?q={quote(canonical_name)}"
            wikipedia_link = f"https://en.wikipedia.org/wiki/{quote(canonical_name)}"

            results.append({
                "Token": extracted_name,
                "Canonical name": canonical_name,
                "Place Type": place_type,
                "Google Maps Link": google_maps_link,
                "Wikipedia Link": wikipedia_link
            })
        else:
            results.append(f"Token: {extracted_name}, No matching canonical name found")

    return render_template("results.html", results=results)

# Function to perform fuzzy matching
def perform_fuzzy_matching(extracted_name, dataset):
    best_match = None
    highest_similarity = 0
    for row in dataset:

        similarity = fuzz.ratio(extracted_name.lower(), row["canonical name"].lower())
        if similarity > similarity_threshold and similarity > highest_similarity:
            best_match = row
            highest_similarity = similarity
            
        for other_name in row['other-names']:
            if other_name:
                similarity = fuzz.ratio(extracted_name.lower(), other_name.lower())
                if similarity > similarity_threshold and similarity > highest_similarity:
                    best_match = row
                    highest_similarity = similarity
    return best_match

@app.route('/translate', methods=['POST'])
def translate_text():
    data = request.get_json()
    to_translate = data.get('text')
    translated = GoogleTranslator(source='auto', target='en').translate(to_translate)
    return jsonify({'translated_text': translated})

if __name__ == "__main__":
    app.run(debug=True)
