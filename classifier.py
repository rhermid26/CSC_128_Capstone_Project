"""
CSC-128 Assignment 3 starter: Intent classifier
Roberto Hermida Lujan
"""
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# TODO 1: build a stop word list. Do not include "not" or "no".
STOP_WORDS = set({"i", "me", "my", "a", "an", "the", "is", "to", "for", "can", "you", "please", "it", "of", "and"})

# TODO 2: five intents, at least six example phrasings each
TRAINING = {
    "password_reset": [
        "reset my password",
        "forgot my login",
        "cannot get into my account",
        "password help",
        "locked out of my account",
        "help logging in"
    ],
    "wifi_help": [
        "connect to wifi",
        "internet is not working",
        "cannot get online",
        "wireless network problem",
        "wifi password",
        "i need help with wifi"
    ],
    "hours": [
        "when are you open",
        "what are your hours",
        "are you open on saturday",
        "closing time",
        "how long are you open",
        "when do you close"
    ],
     "account_help": [
        "help with my account",
        "i have a problem with my account",
        "my account is not working",
        "i need help with my account",
        "something is wrong with my account",
        "can you help with my account"
    ],
    "student_help": [
        "i need help with my classes",
        "where can i find my class schedule",
        "how do i register for classes",
        "i need help registering for a class",
        "where can i find my grades",
        "how do i drop a class"
    ],
    "contact_support": [
        "how do i contact support",
        "i need to talk to support",
        "can i speak with someone",
        "where can i get support",
        "i need customer service",
        "how can i reach support"
    ]

}

RESPONSES = {
    "password_reset": "Reset your password at password.cpcc.edu.",
    "wifi_help": "For help connecting to wifi, check your wireless settings and make sure you are connected to the correct network.",
    "hours": "Our hours are Monday through Friday from 8am to 5pm.",
    "account_help": "For help with your account, please contact customer support.",
    "student_help": "Please check online through Brightspace for ongoing coursework or MyCollege for official final grades ",
    "contact_support": "You can contact customer support for additional help.",
}

FALLBACK = "I am unable to help you with that. I can help you with your password, wifi, hours, account, or with your student info."

# TODO 6: set this using the evidence your tests print out
DEFAULT_THRESHOLD = 0.0


def normalize(text):
    """TODO 3: lowercase, remove punctuation, drop stop words."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)   # punctuation to spaces
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS]


class IntentClassifier:
    def __init__(self, training=None, threshold=DEFAULT_THRESHOLD):
        if training is None:
            training = TRAINING

        self.threshold = threshold

        # Store all training phrases and their corresponding intents
        self.phrases = []
        self.labels = []

        for intent, examples in training.items():
            for phrase in examples:
                # Here's a trick, normalize them BEFORE adding them to the phrases
                words = normalize(phrase)
                normalized_phrase = " ".join(words)

                self.phrases.append(normalized_phrase)
                self.labels.append(intent)

        # Create the TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer()

        # Convert the training phrases into TF-IDF vectors
        self.training_vectors = self.vectorizer.fit_transform(self.phrases)

    def classify(self, text):
        """
        Return (intent, confidence).

        Transform the text, take cosine similarity against every training
        phrase, find the best score, and return None for the intent when
        that score is below the threshold.
        """

        user_vector = self.vectorizer.transform([text])
        scores = cosine_similarity(user_vector, self.training_vectors)[0]

        best_index = scores.argmax()
        best_score = scores[best_index]

        if best_score < self.threshold:
            return None, best_score
        return self.labels[best_index], best_score

    def respond(self, text):
        """Return (reply, intent, confidence)."""
        intent, confidence = self.classify(text)

        if intent is None:
            return FALLBACK, None, confidence

        return RESPONSES[intent], intent, confidence