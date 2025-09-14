# ANPR (Automatic Number Plate Recognition) with Database Integration

A comprehensive Python-based license plate recognition system that uses OpenAI's GPT-4o-mini for image analysis and includes Norwegian vehicle registry lookup with SQLite database integration.

## 🚀 Features

- **AI-Powered OCR**: Uses OpenAI GPT-4o-mini for accurate license plate text extraction
- **Norwegian Registry Integration**: Real-time lookup against Norwegian vehicle registry
- **Database Tracking**: Automatic SQLite database for all registry checks with timestamps
- **Smart Upsert**: Automatically insert new plates or update existing records
- **Comprehensive CLI**: Full command-line interface for database management
- **Multiple Image Formats**: Support for JPEG, PNG, and WebP images
- **Robust Error Handling**: Comprehensive error handling and logging

## 📋 Requirements

- Python 3.7+
- OpenAI API key
- Internet connection (for registry lookups)

## 🛠 Installation

1. **Clone the repository:**

```bash
git clone https://github.com/OsloVision/anpr-pp.git
cd anpr-pp
```

2. **Install dependencies:**

```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key:**

```bash
export OPENAI_API_KEY="your-api-key-here"
```

## 📖 Usage

### Basic License Plate Reading

Read license plate text from an image:

```bash
python license_plate_reader.py path/to/image.jpg
```

**Output:**

```
ABC123
```

### With Norwegian Registry Check + Database Integration

Check license plate against Norwegian registry and automatically save to database:

```bash
python license_plate_reader.py --check-registry path/to/image.jpg
```

**Output:**

```
EF49617
hitting url: https://rettsstiftelser.brreg.no/nb/oppslag/motorvogn/EF49617
Pattern found in response.
Norwegian registry: yes
📝 Updated database: EF49617 -> yes
```

### Advanced Options

```bash
# Custom API key
python license_plate_reader.py --api-key your-key image.jpg

# Custom database path
python license_plate_reader.py --check-registry --db-path custom.db image.jpg

# Full help
python license_plate_reader.py --help
```

## 🗄 Database Management

The system automatically creates a SQLite database to track all registry lookups.

### Database Schema

```sql
CREATE TABLE loan_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numberplate TEXT NOT NULL,
    loan TEXT NOT NULL,                    -- "yes" or "no" for registry status
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### Command Line Database Operations

```bash
# View all records
python loan_db_utils.py list

# Get specific license plate
python loan_db_utils.py get "EF49617"

# Add manual record
python loan_db_utils.py add "ABC123" "yes"

# Update existing record
python loan_db_utils.py update "ABC123" "no"

# Delete record
python loan_db_utils.py delete "ABC123"

# Check if plate exists in database
python loan_db_utils.py exists "ABC123"

# Create database manually (auto-created when needed)
python loan_db_utils.py create
```

### Programmatic Database Usage

```python
from loan_db_utils import LoanStatusDB

# Initialize database connection
db = LoanStatusDB()

# Add or update records
db.add_loan_status("EF49617", "yes")
db.update_loan_status("EF49617", "no")

# Query records
record = db.get_loan_status("EF49617")
all_records = db.list_all_records()

# Check existence
exists = db.check_numberplate_exists("EF49617")
```

## 🔍 Norwegian Registry Integration

The system can check license plates against the Norwegian vehicle registry:

- **Registry URL**: `https://rettsstiftelser.brreg.no/nb/oppslag/motorvogn/{numberplate}`
- **Pattern Matching**: Uses regex to extract registration count
- **Results**:
  - `"yes"` - Plate is registered (count > 0)
  - `"no"` - Plate not found or not registered
- **Database Storage**: All lookups are automatically saved with timestamps

### Registry Check Only

For standalone registry checking without image processing:

```python
from license_plate_reader import check_plate_only

result = check_plate_only("EF49617")  # Returns "yes" or "no"
```

## 📁 File Structure

```
anpr-pp/
├── license_plate_reader.py    # Main ANPR script
├── loan_db_utils.py          # Database utility class and CLI
├── create_database.py        # Database creation script
├── test_regex.py             # Norwegian registry regex tests
├── test_integration.py       # Integration tests
├── test_workflow.py          # Workflow simulation tests
├── requirements.txt          # Python dependencies
├── loan_status.db           # SQLite database (auto-created)
├── DATABASE_INTEGRATION.md  # Detailed integration docs
└── README.md                # This file
```

## 🧪 Testing

The project includes comprehensive tests:

```bash
# Test Norwegian registry regex
python test_regex.py

# Test database integration
python test_integration.py

# Test full workflow simulation
python test_workflow.py
```

## 📷 Supported Image Formats

- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **WebP** (.webp)

## 📊 Example Workflows

### 1. Process Multiple Images

```bash
#!/bin/bash
for image in *.jpg; do
    echo "Processing $image..."
    python license_plate_reader.py --check-registry "$image"
done
```

### 2. Batch Processing with Results

```bash
#!/bin/bash
for image in *.jpg; do
    PLATE=$(python license_plate_reader.py "$image")
    echo "$image: $PLATE"
done
```

### 3. Database Analysis

```python
from loan_db_utils import LoanStatusDB

db = LoanStatusDB()
records = db.list_all_records()

# Count registered vs unregistered
registered = len([r for r in records if r[2] == "yes"])
unregistered = len([r for r in records if r[2] == "no"])

print(f"Registered: {registered}, Unregistered: {unregistered}")
```

## ⚡ API Rate Limits

- **OpenAI API**: Respects OpenAI's rate limits
- **Norwegian Registry**: Includes appropriate delays and User-Agent headers
- **Timeouts**: 10-second timeout for registry requests

## 🔧 Configuration

### Environment Variables

```bash
export OPENAI_API_KEY="your-openai-api-key"
```

### Default Settings

- **Database Path**: `loan_status.db` (in current directory)
- **Request Timeout**: 10 seconds
- **Image Processing**: Temperature 0 for consistent results
- **Max Tokens**: 50 (sufficient for license plates)

## 🐛 Error Handling

The system includes comprehensive error handling:

- **Missing Files**: Clear error messages for missing images
- **API Errors**: Graceful handling of OpenAI API issues
- **Network Issues**: Timeout handling for registry requests
- **Database Errors**: SQLite error handling with rollback
- **Image Format**: Automatic format detection and fallback

## 🔒 Privacy & Security

- **No Image Storage**: Images are processed in memory only
- **API Key Security**: Support for environment variables
- **Database**: Local SQLite storage, no external data transmission
- **Registry Lookups**: Anonymous requests to public registry

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:

1. Check the [Issues](https://github.com/OsloVision/anpr-pp/issues) page
2. Review the test files for usage examples
3. Check `DATABASE_INTEGRATION.md` for detailed integration docs

## 🏗 Architecture

```
Image Input → OpenAI GPT-4o-mini → License Plate Text
                                        ↓
Norwegian Registry Check ← Regex Pattern Matching
                                        ↓
Database Upsert ← Timestamp Tracking ← Result Processing
```

## 📈 Roadmap

- [ ] Support for additional vehicle registries
- [ ] Batch processing improvements
- [ ] Web interface
- [ ] Docker containerization
- [ ] API endpoint wrapper
- [ ] Enhanced image preprocessing
