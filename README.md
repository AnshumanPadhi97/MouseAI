# MouseAI - AI at Your Fingertips 🤖✨

**MouseAI** is a powerful tool that brings AI to your fingertips, allowing you to interact with PDFs, and CSV files by simply dragging and dropping them. It uses Retrieval-Augmented Generation (RAG) to answer your questions, summarize content, and provide insights based on the documents you upload. 

MouseAI has been created with **Ollama**, a framework for building AI-powered applications.

![alt text](https://github.com/AnshumanPadhi97/MouseAI/blob/master/Screenshot%202025-02-09%20155702.png?raw=true)

---

## Features

- **Simple Chat**: Interact with AI in a seamless chat interface.
- **RAG with PDFs & CSV Files**: Upload PDF and CSV files, and talk to the AI to get relevant insights, summaries, or answer questions based on the documents.
- **Drag and Drop**: Easily drag and drop PDF or CSV files for a more interactive experience.
- **Highlight and Explain**: Highlight specific text and press `Ctrl+Space` for an explanation or a detailed response from the AI.

---

## Requirements

To run the project, make sure you have the following dependencies installed:

- Python 3.7 or higher
- `pip` for installing packages
- **Ollama**: You need to download the Ollama model files to get started.

---

## Installation

### 1. Clone the repository:

```bash
git clone https://github.com/AnshumanPadhi97/MouseAI.git
cd MouseAI
```

### 2. Install dependencies:
Make sure to install all the required dependencies by running:
```bash
pip install -r requirements.txt
```

### 3. Download Ollama Files:
To get started with the Ollama framework, you need to download the model files. 

Follow the steps below to install and set up Ollama:

Download Ollama from the official site: https://ollama.com/
```bash
ollama pull <model-name>
```
Replace <model-name> with the name of the model you want to use for your AI application.

### 3. Running the Application:
1. Start the application:
To run the tool, execute the following command:
```bash
python ./main.py
```
2. Chat Interface:
```bash
Use Ctrl+Shift+C to enter a simple chat interface.
```
3. Extract Text from PDF & CSV:
```bash
Drag and drop PDF or CSV files into the interface.
Use the AI chat to query or summarize content from these documents.
```
4. Highlight and Explain Text:
```bash
Highlight specific text within the document.
Press Ctrl+Space to have the AI explain the selected text or provide additional context or insights.
```
5. Exit the Application:
```bash
Press Ctrl+Q to exit the application.
```
