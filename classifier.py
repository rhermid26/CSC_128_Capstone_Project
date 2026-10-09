"""
CSC-128 Capstone Project: Intent classifier
Roberto Hermida Lujan
"""

import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


STOP_WORDS = {
    "i", "me", "my", "a", "an", "the", "is", "to",
    "for", "can", "you", "please", "it", "of", "and"
}


TRAINING = {
    "study_tips": [
        "give me study tips",
        "how can I study better",
        "help me study",
        "how do I remember information",
        "what are good study habits",
        "how should I prepare for a test"
    ],
    "study_schedule": [
        "help me make a study schedule",
        "plan my study time",
        "make a study plan",
        "how should I organize my studying",
        "help me plan my homework",
        "divide my time between subjects"
    ],
    "explain_topic": [
        "explain this topic to me",
        "help me understand this subject",
        "explain this in simple words",
        "I do not understand this lesson",
        "teach me a programming concept",
        "help me learn a difficult topic"
    ],
    "course_help": [
        "check my course number",
        "is CSC-128 a valid course number format",
        "help me with my classes",
        "I need help with a course",
        "how do I organize my coursework",
        "check my class information"
    ],
    "time_management": [
        "how much time should I study",
        "calculate my study time",
        "help me manage my time",
        "how long should my study breaks be",
        "I have limited time to study",
        "help me organize my free time"
    ]
}


RESPONSES = {
    "study_tips": "I can help you find study methods that work for your subject.",
    "study_schedule": "I can help you organize your subjects into a study schedule.",
    "explain_topic": "Tell me which topic you want explained, and I'll break it down.",
    "course_help": "I can help check a course number's format or organize your coursework.",
    "time_management": "Tell me how much time you have available, and we can plan your study time."
}


FALLBACK = (
    "I'm not sure what kind of study help you need yet. "
    "Try asking for study tips, a study schedule, a topic explanation, "
    "course help, or time management advice."
)


DEFAULT_THRESHOLD = 0.20


def normalize(text):
    """Lowercase text, remove punctuation, and drop common words."""

    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return [
        word for word in text.split()
        if word not in STOP_WORDS
    ]


class IntentClassifier:
    def __init__(self, training=None, threshold=DEFAULT_THRESHOLD):
        if training is None:
            training = TRAINING

        self.threshold = threshold
        self.phrases = []
        self.labels = []

        for intent, examples in training.items():
            for phrase in examples:
                self.phrases.append(" ".join(normalize(phrase)))
                self.labels.append(intent)

        self.vectorizer = TfidfVectorizer()
        self.training_vectors = self.vectorizer.fit_transform(self.phrases)

    def classify(self, text):
        """Return the best matching intent and its similarity score."""

        cleaned_text = " ".join(normalize(text))

        if not cleaned_text.strip():
            return None, 0.0

        user_vector = self.vectorizer.transform([cleaned_text])
        scores = cosine_similarity(
            user_vector, self.training_vectors
        )[0]

        best_index = scores.argmax()
        best_score = scores[best_index]

        if best_score < self.threshold:
            return None, best_score

        return self.labels[best_index], best_score

    def respond(self, text):
        """Return a response, intent, and similarity score."""

        intent, confidence = self.classify(text)

        if intent is None:
            return FALLBACK, None, confidence

        return RESPONSES[intent], intent, confidence