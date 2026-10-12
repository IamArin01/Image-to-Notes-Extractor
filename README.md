# Image to Notes Extractor

This project extracts and transcribes text from an image using Google Gemini's Gemma 4 model in Python. It includes a shared `gemma_client.py` helper and a sample image for experimentation.

## Model

- Model: `gemma-4-26b-a4b-it`
- API provider: Google GenAI / Gemini API
- Environment variable: `GEMINI_API_KEY`

## Features

- Centralized Gemini/Gemma client helper
- API key validation and safe retry handling
- Optional caching for repeated prompts
- Sample image included for testing image-based workflows
- Command-line image transcription, with an interactive path prompt when no image is specified

## Project structure

- `gemma_client.py` — shared helper for calling the Gemma model
- `image_to_notes.py` — extracts text from an image supplied as a command-line argument or interactive prompt
- `requirements.txt` — Python dependencies
- `Text_entropy.png` — sample input image
- `.env` — local environment variables (not committed)

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Create or edit a `.env` file in the project root with your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
GEMMA_MODEL=gemma-4-26b-a4b-it
```

Important:
- Keep `.env` local and do not commit it to Git.
- If you do not have a key, create one in Google AI Studio and paste it into `.env`.

## Run

From the project root:

```powershell
python image_to_notes.py .\Text_entropy.png
```

The transcription is saved as `Text_entropy_notes.txt` beside the image. Open it in Notepad with:

```powershell
notepad .\Text_entropy_notes.txt
```

Choose a different output file with `-o` or `--output`:

```powershell
python image_to_notes.py .\Text_entropy.png --output .\notes\transcription.txt
```

To enter the image path interactively instead, run:

```powershell
python image_to_notes.py
```

The image is uploaded to Google's Gemini API for transcription. The script makes one Gemma generation request per run and saves the text response as a UTF-8 `.txt` file.

## Screenshot

![Sample image](./Text_entropy.png)

## Notes

- The project uses the `google-genai` package from `requirements.txt`.
- The client helper reads `.env` automatically when `python-dotenv` is available.
- Separately from the `.txt` transcription output, cached prompts and responses are saved as UTF-8 JSON text in `.cache/responses.txt` to avoid repeating API calls. The cache can be opened with `notepad .cache\responses.txt`; `.cache/` is ignored by Git because it may contain private prompts and extracted text.
- The model and behavior are easy to tune in `gemma_client.py` via environment variables such as `GEMMA_MODEL`, `GEMMA_CACHE`, and `MIN_SECONDS_BETWEEN_CALLS`.
