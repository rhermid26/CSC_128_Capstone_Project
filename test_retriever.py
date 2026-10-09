
from retriever import Retriever

retriever = Retriever()

questions = [
    "How can I remember what I study?",
    "How should I prepare for a test?",
    "How can I get better at Python?",
    "How do I organize my homework?",
    "Tell me about cooking dinner"
]

for question in questions:
    print(f"\nQuestion: {question}")

    hits = retriever.search(question)

    if hits:
        for hit in hits:
            print(f"Source: {hit['source']}")
            print(f"Score: {hit['score']:.2f}")
            print(f"Information: {hit['text']}")
    else:
        print("No matching study information found.")