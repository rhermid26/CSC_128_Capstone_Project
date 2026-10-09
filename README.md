# Study Buddy Chatbot

## About the Project

Study Buddy is a chatbot that helps students with studying. It can give study tips, explain topics, and help students plan their study time.

I made this project using Python and a language model. Python handles tasks that need exact answers, while the AI helps answer questions and explain things.

## What It Can Do

* Give study tips.
* Help explain difficult topics.
* Make a study schedule.
* Check the format of a course number like CSC-128.
* Calculate study time after breaks.
* Find helpful study information.

## Project Files

* **app.py:** Shows the chatbot on the screen.
* **agent.py:** Connects everything and controls how the chatbot works.
* **classifier.py:** Tries to figure out what kind of help the student needs.
* **retriever.py:** Searches for study tips related to the question.
* **tools.py:** Contains Python functions for checking course numbers, calculating time, and making schedules.
* **test_retriever.py:** Tests the search feature.
* **test_tools.py:** Tests the Python functions.
* **requirements.txt:** Lists the libraries needed for the project.

## How It Works

1. The student types a question.
2. The classifier tries to identify the type of question.
3. The retriever looks for related study information.
4. The AI uses the question and any useful information to create an answer.
5. If needed, the AI can use a Python function to calculate something or make a schedule.
6. The answer appears in the chat.

## Programs and Libraries

* Python
* Streamlit
* Groq
* scikit-learn

## How to Run It

Make sure your Groq API key is set up. Then run:

```bash
streamlit run app.py
```

The chatbot should open in your browser.

## Testing

I tested the chatbot with different questions to see if it could give study tips, check course number formats, calculate study time, and make schedules.

I also used pytest to test the Python functions and the search feature.

## Limitations

The chatbot can make mistakes, so students should check important information. The course number checker only checks the format. It does not check if the course actually exists.

## Conclusion

This project helped me learn how Python and AI can work together. Python handles tasks with clear rules, and the AI helps answer questions in a more natural way. I wanted to make something that could help students with their schoolwork.
