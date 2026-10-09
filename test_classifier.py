
from classifier import IntentClassifier

classifier = IntentClassifier()

questions = [
    "Give me study tips",
    "Help me make a study schedule",
    "Explain Python loops in simple words",
    "Check my course number CSC-128",
    "How much time should I spend studying?",
    "What is the weather today?"
]

for question in questions:
    intent, score = classifier.classify(question)
    print(f"Question: {question}")
    print(f"Intent: {intent}")
    print(f"Similarity: {score:.2f}")
    print()