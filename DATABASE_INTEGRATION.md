# License Plate Reader with Database Integration

## Overview

The license plate reader now automatically saves all registry lookups to a SQLite database when using the `--check-registry` option.

## Features Added ✅

### 1. **Automatic Database Creation**

- Database and table are created automatically if they don't exist
- No manual setup required

### 2. **Smart Upsert Functionality**

- **INSERT**: New license plates are added to the database
- **UPDATE**: Existing license plates are updated with new status
- **Timestamps**: Automatic `created_at` and `updated_at` tracking

### 3. **Database Schema**

```sql
CREATE TABLE loan_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numberplate TEXT NOT NULL,
    loan TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Unique constraint prevents duplicates
CREATE UNIQUE INDEX idx_numberplate_unique ON loan_status(numberplate);

-- Auto-update trigger for updated_at
CREATE TRIGGER update_loan_status_updated_at...
```

## Usage Examples

### Basic License Plate Reading (no database)

```bash
python license_plate_reader.py image.png
```

### With Registry Check + Database Integration

```bash
python license_plate_reader.py --check-registry image.png
```

### Custom Database Path

```bash
python license_plate_reader.py --check-registry --db-path custom.db image.png
```

## Database Management

### Command Line Utilities

```bash
# View all records
python loan_db_utils.py list

# Get specific record
python loan_db_utils.py get EF49617

# Add manual record
python loan_db_utils.py add "ABC123" "yes"

# Update existing record
python loan_db_utils.py update "ABC123" "no"

# Delete record
python loan_db_utils.py delete "ABC123"

# Check if exists
python loan_db_utils.py exists "ABC123"
```

### Programmatic Usage

```python
from loan_db_utils import LoanStatusDB

db = LoanStatusDB()
db.add_loan_status("EF49617", "yes")
record = db.get_loan_status("EF49617")
```

## Workflow

1. **Image Processing**: Read license plate from image using OpenAI
2. **Registry Check**: Check Norwegian vehicle registry (if `--check-registry`)
3. **Database Upsert**: Automatically save/update result in database
4. **Timestamp Tracking**: Track when records are created and last updated

## Example Output

```
$ python license_plate_reader.py --check-registry tesla.png
EF49617
hitting url: https://rettsstiftelser.brreg.no/nb/oppslag/motorvogn/EF49617
Pattern found in response.
Norwegian registry: yes
📝 Updated database: EF49617 -> yes
```

## Database Record Types

- **"yes"**: License plate is registered in Norwegian registry
- **"no"**: License plate is not registered or not found
- **Custom values**: Can be manually set via utility functions

## Files Created

1. **`create_database.py`** - Database setup script
2. **`loan_db_utils.py`** - Database utility class and CLI
3. **`license_plate_reader.py`** - Updated with database integration
4. **`test_regex.py`** - Regex testing for Norwegian registry
5. **`test_integration.py`** - Integration testing
6. **`test_workflow.py`** - Workflow simulation testing

## Benefits

- ✅ **No manual database setup** required
- ✅ **Automatic tracking** of all registry checks
- ✅ **Duplicate prevention** via unique constraints
- ✅ **Timestamp tracking** for audit trails
- ✅ **Easy data management** via CLI utilities
- ✅ **Flexible database paths** for different projects
- ✅ **Robust error handling** and logging

The system is now production-ready for tracking license plate registry lookups! 🚀
