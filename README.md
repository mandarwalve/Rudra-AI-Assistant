# RUDRA --- Personal AI Desktop Assistant

RUDRA is a locally running Windows desktop AI assistant. The project
combines a Python desktop interface, a local language model through
Ollama, speech recognition, text-to-speech, and filename-based file
search.

> **Project status:** The local AI foundation, desktop interface, and
> basic file search have been implemented and tested. Document reading,
> Windows automation, persistent memory, and packaging are planned next.

## Current capabilities

-   **Local AI responses:** Uses Qwen 2.5 3B through Ollama.
-   **Speech recognition:** Uses Vosk for microphone input.
-   **Voice output:** Uses Windows text-to-speech.
-   **Desktop interface:** Built with PySide6.
-   **Text chat:** Send messages through the RUDRA desktop window.
-   **Voice interaction:** Start voice input using the microphone
    control.
-   **Background processing:** Runs AI work in a worker thread to keep
    the interface responsive.
-   **Filename search:** Select a folder or drive, enter a filename or
    keyword, and display matching file paths in the chat.

## Technology stack

  Component             Technology
  --------------------- ------------------
  Language              Python
  Desktop GUI           PySide6
  Local model runtime   Ollama
  Language model        Qwen 2.5 3B
  Speech-to-text        Vosk
  Text-to-speech        Windows speech
  File search           Python `os.walk`

## Project structure

``` text
C:\jarvis\
├── jarvis.py              # Existing AI, speech recognition and voice-output logic
├── jarvis_desktop.py      # RUDRA desktop application
├── file_manager.py        # Filename-based file search
├── model/                 # Local speech model files, if stored here
└── venv/                  # Python virtual environment (do not commit)
```

Your actual project may contain additional files. Update this tree to
match your repository before publishing.

## Prerequisites

-   Windows
-   Python installed
-   Ollama installed and running
-   Qwen 2.5 3B downloaded in Ollama
-   Project's Vosk model files available locally
-   Microphone and speakers/headphones
-   Git installed (for version control)

## Setup

Open PowerShell in the project directory:

``` powershell
cd C:\jarvis
```

Create and activate a virtual environment if you do not already have
one:

``` powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the packages used by the desktop application:

``` powershell
python -m pip install PySide6
```

Install the additional dependencies required by your existing
`jarvis.py` implementation. For example, if it imports `requests` or
`vosk`, install those packages in this same environment:

``` powershell
python -m pip install requests vosk
```

Make sure Ollama is running and that the Qwen model name configured in
`jarvis.py` matches the model installed on your computer.

Launch RUDRA:

``` powershell
python jarvis_desktop.py
```

## Using file search

1.  Open RUDRA.
2.  Select **SEARCH FILES**.
3.  Choose a folder or drive you are allowed to access.
4.  Enter a filename or keyword.
5.  Review the matching file paths shown in the chat.

The current implementation searches **filenames**, not the text inside
PDFs, Word documents, or other files. It lists results and does not edit
or delete files.

## Roadmap

-   [x] Local Qwen + Ollama foundation
-   [x] Vosk speech recognition foundation
-   [x] Windows voice output foundation
-   [x] PySide6 desktop interface
-   [x] Text chat connected to the existing AI engine
-   [x] Microphone interaction through the desktop interface
-   [x] Filename-based file search
-   [ ] Read PDF, DOCX, and TXT documents
-   [ ] Summarize and explain selected documents with Qwen
-   [ ] Add controlled Windows application launching
-   [ ] Add persistent local memory
-   [ ] Add browser automation and multi-step task execution
-   [ ] Package the application as a Windows executable

## Security and privacy

RUDRA is intended to work locally on the user's Windows PC, but local
execution does not automatically mean unrestricted access to every file.

-   File access is limited by the permissions of the Windows account
    running RUDRA.
-   Windows-protected files and inaccessible locations may not be
    searchable.
-   Ask for clear first-time consent before enabling broad file access.
-   Require confirmation before creating, editing, or overwriting files.
-   Always require explicit confirmation before deleting or overwriting
    files.
-   Keep API keys, passwords, tokens, personal documents, and private
    configuration out of Git.

## Before pushing to GitHub

Do **not** commit your virtual environment, model weights, secrets, or
private data. Add a `.gitignore` file similar to this:

``` gitignore
# Python
__pycache__/
*.py[cod]
.venv/
venv/
.env
.env.*

# Local models and large model files
model/
models/
*.bin
*.pt
*.pth
*.onnx

# Local data and logs
*.log
data/
logs/

# Editor and operating-system files
.vscode/
.idea/
.DS_Store
Thumbs.db
```

Review the ignore rules before committing. If your Vosk model is
required for another user to run RUDRA, document how to obtain it rather
than committing large model files without checking their license and
repository limits.

## Current status

The working milestone is the RUDRA desktop interface with local AI/voice
integration and filename-based file search. The next planned feature is
document reading for PDF, DOCX, and TXT files.

------------------------------------------------------------------------

Built as a personal local AI assistant project.
