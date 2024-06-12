document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const micButton = document.getElementById('micButton');
    const languageOptions = document.querySelectorAll('#languageOptions .dropdown-item');
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    let chosenLanguage = 'en-IN'; // Default language

    languageOptions.forEach(option => {
        option.addEventListener('click', function() {
            chosenLanguage = this.getAttribute('data-lang');
            document.getElementById('languageDropdown').textContent = this.textContent;
        });
    });

    micButton.addEventListener('click', function() {
        recognition.lang = chosenLanguage;
        recognition.start();
        console.log('Speech recognition started.');

        recognition.onresult = function(event) {
            const speechResult = event.results[0][0].transcript;
            console.log('Detected language:', recognition.lang);
            searchInput.value = speechResult;

            // Make a POST request to Flask backend for translation
            fetch('/translate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: speechResult })
            })
            .then(response => response.json())
            .then(data => {
                searchInput.value = data.translated_text;
            })
            .catch(error => {
                console.error('Translation error:', error);
            });
        };

        recognition.onend = function() {
            console.log('Speech recognition ended.');
        };
    });
});
