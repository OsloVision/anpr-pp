#!/usr/bin/env python3
"""
License Plate Reader using OpenAI GPT-4o-mini
Reads license plate text from an image using OpenAI's vision capabilities.
"""

import os
import sys
import base64
import argparse
import re
import requests
from pathlib import Path
from openai import OpenAI
from loan_db_utils import LoanStatusDB


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
        # remove whitespace
        license_plate_text = re.sub(r"\s+", "", license_plate_text)
        return license_plate_text

    except Exception as e:
        print(f"Error calling OpenAI API: {e}", file=sys.stderr)
        sys.exit(1)


def check_norwegian_registry(numberplate):
    """
    Check if a license plate is registered in the Norwegian vehicle registry.

    Args:
        numberplate (str): The license plate number to check

    Returns:
        str: "yes" if registered (x > 0), "no" if not registered or error
    """
    try:
        # Format the URL with the license plate number
        url = f"https://rettsstiftelser.brreg.no/nb/oppslag/motorvogn/{numberplate}"

        # Make GET request with proper headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        }

        print("hitting url:", url)
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # print(response.text)

        # Search for the pattern in the response text
        pattern = r"Det er (\d+) oppføring på registreringsnummer"
        match = re.search(pattern, response.text)

        if match:
            print("Pattern found in response.")
            count = int(match.group(1))
            return "yes" if count > 0 else "no"
        else:
            print("Pattern not found in response.")
            # Pattern not found, assume not registered
            return "no"

    except requests.exceptions.RequestException as e:
        print(f"Error checking Norwegian registry: {e}", file=sys.stderr)
        return "no"
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        return "no"


def check_plate_only(numberplate):
    """
    Standalone function to check if a license plate is registered in Norwegian registry.

    Args:
        numberplate (str): The license plate number to check

    Returns:
        str: "yes" if registered (x > 0), "no" if not registered or error
    """
    return check_norwegian_registry(numberplate)


def upsert_loan_status(numberplate, loan_status, db_path="loan_status.db"):
    """
    Insert or update loan status in the database.
    
    Args:
        numberplate (str): License plate number
        loan_status (str): Loan status ("yes" for registered, "no" for not registered)
        db_path (str): Path to the SQLite database file
    
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        import sqlite3
        import os
        
        # Check if database file exists, if not create it with proper schema
        if not os.path.exists(db_path):
            print(f"📁 Creating database: {db_path}")
            # Create the database with the schema
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Create table
            cursor.execute("""
                CREATE TABLE loan_status (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    numberplate TEXT NOT NULL,
                    loan TEXT NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create unique index
            cursor.execute("""
                CREATE UNIQUE INDEX idx_numberplate_unique 
                ON loan_status(numberplate)
            """)
            
            # Create trigger
            cursor.execute("""
                CREATE TRIGGER update_loan_status_updated_at
                AFTER UPDATE ON loan_status
                FOR EACH ROW
                BEGIN
                    UPDATE loan_status SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
                END
            """)
            
            conn.commit()
            conn.close()
            print(f"✅ Database created: {db_path}")
        
        db = LoanStatusDB(db_path)
        
        # Check if record exists
        existing_record = db.get_loan_status(numberplate)
        
        if existing_record:
            # Update existing record
            success = db.update_loan_status(numberplate, loan_status)
            if success:
                print(f"📝 Updated database: {numberplate} -> {loan_status}")
            return success
        else:
            # Insert new record
            success = db.add_loan_status(numberplate, loan_status)
            if success:
                print(f"💾 Added to database: {numberplate} -> {loan_status}")
            return success
            
    except Exception as e:
        print(f"❌ Database error: {e}", file=sys.stderr)
        return False


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
    parser.add_argument(
        "--check-registry",
        action="store_true",
        help="Also check if the license plate is registered in Norwegian vehicle registry",
    )
    parser.add_argument(
        "--db-path",
        default="loan_status.db",
        help="Path to the SQLite database file (default: loan_status.db)",
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

        # Check Norwegian registry if requested
        if args.check_registry:
            registry_result = check_norwegian_registry(license_plate_text)
            print(f"Norwegian registry: {registry_result}")
            
            # Upsert into database
            upsert_loan_status(license_plate_text, registry_result, args.db_path)

    except KeyboardInterrupt:
        print("\nOperation cancelled by user.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
