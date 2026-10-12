import argparse
import sys
from pathlib import Path

try:
    import gemma_client
except ImportError:
    sys.exit(
        "Could not import gemma_client. Run this script from the project folder "
        "with the project virtual environment."
    )


OCR_PROMPT = (
    "Transcribe all readable text in this image. Preserve the original language, "
    "spelling, punctuation, and paragraph breaks. Do not translate, summarize, "
    "or add commentary. Mark text you cannot read as [illegible]. Return only "
    "the transcription."
)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Extract and transcribe text from an image with Gemma 4."
    )
    parser.add_argument(
        "image",
        nargs="?",
        help="path to an image file (prompted for if omitted)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="path for the extracted .txt file (defaults to <image-name>_notes.txt)",
    )
    args = parser.parse_args(argv)

    try:
        image_name = args.image
        if not image_name:
            image_name = input("Image path (or q to quit): ").strip().strip("\"'")
        if not image_name or image_name.lower() in {"q", "quit", "exit"}:
            print("No image selected.")
            return 0

        image_path = Path(image_name).expanduser()
        if not image_path.is_file():
            print(f"Image file not found: {image_path}")
            return 2
        output_path = (
            Path(args.output).expanduser()
            if args.output
            else image_path.with_name(f"{image_path.stem}_notes.txt")
        )
        if output_path.resolve() == image_path.resolve():
            print("Output file must not be the same as the input image.")
            return 2

        print(f"Extracting text from {image_path.name} with Gemma 4...")
        text = gemma_client.ask_with_image(
            image_path,
            OCR_PROMPT,
            system="You are an accurate OCR assistant. Follow the transcription instructions exactly.",
        )
        try:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(text.rstrip() + "\n", encoding="utf-8")
        except OSError as error:
            print(f"\nCould not save the transcription: {error}")
            return 1

        print("\nExtracted text:\n")
        print(text)
        print(f"\nSaved transcription to: {output_path}")
        return 0
    except (EOFError, KeyboardInterrupt):
        print("\nExtraction cancelled.")
        return 130
    except Exception as error:
        print(f"\nCould not extract text: {gemma_client.describe_error(error)}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
