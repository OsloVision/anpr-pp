#!/usr/bin/env python3
"""
License Plate Reader using OpenAI GPT-4o-mini
Reads license plate text from an image using OpenAI's vision capabilities.
"""

import os
import sys
import base64
import argparse
from pathlib import Path
from openai import OpenAI


def encode_image(image_path):
    """Encode image to base64 string."""
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image: {e}", file=sys.stderr)
        sys.exit(1)


def read_license_plate(image_path, api_key=None):
    """
    Read license plate from image using OpenAI GPT-4o-mini.

    Args:
        image_path (str): Path to the image file
        api_key (str): OpenAI API key (optional, can use environment variable)

    Returns:
        str: License plate text
    """
    # Initialize OpenAI client
    if api_key:
        client = OpenAI(api_key=api_key)
    else:
        # Will use OPENAI_API_KEY environment variable
        client = OpenAI()

    # Encode the image
    base64_image = encode_image(image_path)

    # Determine image format
    image_ext = Path(image_path).suffix.lower()
    if image_ext in [".jpg", ".jpeg"]:
        image_format = "jpeg"
    elif image_ext == ".png":
        image_format = "png"
    elif image_ext == ".webp":
        image_format = "webp"
    else:
        image_format = "jpeg"  # Default fallback

    try:
        # Send request to OpenAI
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Read the license plate in this image. Output should just be the text on the license plate, nothing else.",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{image_format};base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=50,
            temperature=0,
        )

        # Extract and return the license plate text
        license_plate_text = response.choices[0].message.content.strip()
        return license_plate_text

    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main function to handle command line arguments and execute license plate reading."""
    parser = argparse.ArgumentParser(
        description="Read license plate text from an image using OpenAI GPT-4o-mini"
    )
    parser.add_argument(
        "image_path", help="Path to the image file containing the license plate"
    )
    parser.add_argument(
        "--api-key",
        help="OpenAI API key (optional, can use OPENAI_API_KEY environment variable)",
    )

    args = parser.parse_args()

    # Check if image file exists
    if not os.path.exists(args.image_path):
        print(f"Error: Image file '{args.image_path}' not found.", file=sys.stderr)
        sys.exit(1)

    # Check if API key is available
    api_key = args.api_key or os.getenv("OPENAI_API_KEY")
    if not api_key:
        print(
            "Error: OpenAI API key not found. Please set OPENAI_API_KEY environment variable or use --api-key argument.",
            file=sys.stderr,
        )
        sys.exit(1)

    # Read the license plate
    try:
        license_plate_text = read_license_plate(args.image_path, api_key)
        print(license_plate_text)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
