let speaking = false;
let utteranceQueue = [];

function toggleSpeech() {
    if (!speaking) {
        startSpeech();
    } else {
        stopSpeech();
    }
}

function startSpeech() {
    const elements = document.querySelectorAll(
        'h1:not(.visually-hidden), span, label, a, button, p, b1, b2, strong, small, div.mb-1.small, input[type="text"][placeholder]'
    );
    elements.forEach(element => {
        if (
            !element.matches('.bd-mode-toggle *, .dropdown-menu *') &&
            !element.querySelector('a') &&
            !(element.tagName.toLowerCase() === 'button' &&
                element.parentElement.tagName.toLowerCase() === 'a') &&
            !(element.tagName.toLowerCase() === 'a' &&
                element.querySelector('img')) &&
            !(element.tagName.toLowerCase() === 'span' && element.classList.contains('text-padding')) &&
            !(element.tagName.toLowerCase() === 'p' &&
                element.querySelector('img'))
        ) {
            const text = element.tagName.toLowerCase() === 'input' ? element.getAttribute('placeholder') : element.textContent.trim();
            utteranceQueue.push({
                element: element,
                text: text
            });
        }
    });
    speaking = true;
    speakNext();
}

function speakNext() {
    if (utteranceQueue.length > 0 && speaking) {
        const { element, text } = utteranceQueue.shift();
        if (
            text === "Sign in" ||
            text === "Return Home" ||
            text === "Login" ||
            text === "Pricing" ||
            text === "About Us" ||
            text === "Home" ||
            text === "Send Invoice" ||
            text === "Communication Reports" ||
            text === "External APIs" ||
            text === "Search" ||
            text === "Remove Filters" ||
            text === "Send an Invoice" ||
            text === "Recipients" ||
            text === "Subject" ||
            text === "Upload XML file" ||
            text === "Send" ||
            text === "Search by Subject" ||
            text === "Search by Sender's Address" ||
            text === "Search by Invoice ID" ||
            text === "Invoice ID"
        ) {
            element.style.backgroundColor = 'yellow';
        } else {
            element.classList.add('highlight');
        }
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.onend = function () {
            if (
                text === "Sign in" ||
                text === "Return Home" ||
                text === "Login" ||
                text === "Pricing" ||
                text === "About Us" ||
                text === "Home" ||
                text === "Send Invoice" ||
                text === "Communication Reports" ||
                text === "External APIs" ||
                text === "Search" ||
                text === "Remove Filters" ||
                text === "Send an Invoice" ||
                text === "Recipients" ||
                text === "Subject" ||
                text === "Upload XML file" ||
                text === "Send" ||
                text === "Search by Subject" ||
                text === "Search by Sender's Address" ||
                text === "Search by Invoice ID" ||
                text === "Invoice ID"
            ) {
                element.style.backgroundColor = '';
                element.classList.remove('highlight');
            } else {
                element.classList.remove('highlight');
            }
            speakNext();
        };
        speechSynthesis.speak(utterance);
    } else {
        speaking = false;
    }
}

function stopSpeech() {
    const elements = document.querySelectorAll(
        'h1:not(.visually-hidden), span, label, a, button, p, b1, b2, strong, small, div.mb-1.small, input[type="text"][placeholder]'
    );
    elements.forEach(element => {
        if (
            !element.matches('.bd-mode-toggle *, .dropdown-menu *') &&
            !element.querySelector('a') &&
            !(element.tagName.toLowerCase() === 'button' &&
                element.parentElement.tagName.toLowerCase() === 'a') &&
            !(element.tagName.toLowerCase() === 'a' &&
                element.querySelector('img')) &&
            !(element.tagName.toLowerCase() === 'span' && element.classList.contains('text-padding')) &&
            !(element.tagName.toLowerCase() === 'p' &&
                element.querySelector('img'))
        ) {
            const text = element.tagName.toLowerCase() === 'input' ? element.getAttribute('placeholder') : element.textContent.trim();
            if (
                text === "Sign in" ||
                text === "Return Home" ||
                text === "Login" ||
                text === "Pricing" ||
                text === "About Us" ||
                text === "Home" ||
                text === "Send Invoice" ||
                text === "Communication Reports" ||
                text === "External APIs" ||
                text === "Search" ||
                text === "Remove Filters" ||
                text === "Send an Invoice" ||
                text === "Recipients" ||
                text === "Subject" ||
                text === "Upload XML file" ||
                text === "Send" ||
                text === "Search by Subject" ||
                text === "Search by Sender's Address" ||
                text === "Search by Invoice ID" ||
                text === "Invoice ID"
            ) {
                element.style.backgroundColor = '';
                element.classList.remove('highlight');
            }
        }
    });

    speaking = false;
    speechSynthesis.cancel();
    utteranceQueue = [];
    const highlightedElements = document.querySelectorAll('.highlight');
    highlightedElements.forEach(element => {
        element.classList.remove('highlight');
    });
}
