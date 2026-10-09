
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


DEFAULT_THRESHOLD = 0.15
DEFAULT_TOP_K = 3


# Study information the chatbot can search
DOCUMENTS = [
    {
        "id": "study_1",
        "source": "Study Tips",
        "text": "Use active recall by closing your notes and trying to remember what you learned."
    },
    {
        "id": "study_2",
        "source": "Study Tips",
        "text": "Use spaced repetition by reviewing information over several days instead of cramming."
    },
    {
        "id": "study_3",
        "source": "Study Tips",
        "text": "Break large assignments into smaller tasks so they are easier to finish."
    },
    {
        "id": "study_4",
        "source": "Time Management",
        "text": "Create a study schedule that lists subjects, tasks, and the time you have available."
    },
    {
        "id": "study_5",
        "source": "Study Breaks",
        "text": "Take short breaks during long study sessions to give yourself time to rest."
    },
    {
        "id": "study_6",
        "source": "Reading Tips",
        "text": "Read a short section, identify the main idea, and explain it in your own words."
    },
    {
        "id": "study_7",
        "source": "Programming Tips",
        "text": "Practice programming by writing small programs, testing them, and fixing errors."
    },
    {
        "id": "study_8",
        "source": "Test Preparation",
        "text": "Prepare for tests by practicing questions and reviewing topics you find difficult."
    }
]


def stem(word):
    """Remove a few common word endings."""

    if word.endswith("ation"):
        return word[:-5]
    if word.endswith("ing"):
        return word[:-3]
    if word.endswith("ed"):
        return word[:-2]
    if word.endswith("s") and len(word) > 3:
        return word[:-1]

    return word


def analyze(text):
    """Lowercase, tokenize, stem, and add bigrams."""

    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)

    words = [stem(word) for word in text.split()]

    bigrams = [
        words[i] + "_" + words[i + 1]
        for i in range(len(words) - 1)
    ]

    return words + bigrams


class Retriever:
    def __init__(self, documents=DOCUMENTS, threshold=DEFAULT_THRESHOLD):
        self._documents = documents
        self._threshold = threshold

        texts = [document["text"] for document in documents]

        self._vectorizer = TfidfVectorizer(
            analyzer=analyze,
            stop_words=None
        )

        self._doc_vectors = self._vectorizer.fit_transform(texts)

    def search(self, question, top_k=DEFAULT_TOP_K):
        """Return the most relevant documents above the threshold."""

        question_vector = self._vectorizer.transform([question])
        scores = cosine_similarity(
            question_vector, self._doc_vectors
        )[0]

        ranked = sorted(
            enumerate(scores),
            key=lambda pair: pair[1],
            reverse=True
        )

        hits = []

        for index, score in ranked[:top_k]:
            if score >= self._threshold:
                hits.append({
                    "id": self._documents[index]["id"],
                    "source": self._documents[index]["source"],
                    "text": self._documents[index]["text"],
                    "score": float(score)
                })

        return hits

    def build_context(self, hits):
        """Format retrieved information for the language model."""

        if not hits:
            return ""

        context = []

        for hit in hits:
            context.append(
                f"Source: {hit['source']}\n"
                f"Fact: {hit['text']}"
            )

        return "\n\n".join(context)