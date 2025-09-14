# License Plate Reader

A Python script that uses OpenAI's GPT-4o-mini to read license plate text from images.

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## Usage

Basic usage:

```bash
python license_plate_reader.py path/to/license_plate_image.jpg
```

With API key argument:

```bash
python license_plate_reader.py path/to/license_plate_image.jpg --api-key your-api-key
```

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- WebP (.webp)

## Output

The script outputs only the license plate text, making it easy to use in automation scripts or pipelines.

## Examples

```bash
# Example with a license plate image
python license_plate_reader.py license_plate.jpg
# Output: ABC123

# Using in a script
PLATE_TEXT=$(python license_plate_reader.py image.jpg)
echo "Detected plate: $PLATE_TEXT"
```

## Error Handling

The script includes error handling for:

- Missing image files
- Invalid API keys
- Network/API errors
- Unsupported image formats

All errors are printed to stderr, while the license plate text is printed to stdout.
