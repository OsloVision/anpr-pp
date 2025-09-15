# Norwegian Vehicle Data API Client

A Python client for the Norwegian Vehicle Data API (Statens Vegvesen) that allows you to look up vehicle information by license plate or VIN number.

## Features

- Look up vehicle data by license plate (kjennemerke)
- Look up vehicle data by VIN/chassis number (understellsnummer)
- Comprehensive error handling and retry logic
- Rate limiting and quota management
- Type-safe responses with Pydantic models
- Simple high-level API and raw data access
- Context manager support for proper resource cleanup

## Installation

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Copy the example environment file and configure your settings:

```bash
cp .env.example .env
```

3. Edit `.env` file and add your API key if required:

```bash
VEHICLE_API_KEY=your_api_key_here
```

## Quick Start

### Simple lookup by license plate

```python
from norwegian_vehicle_api import lookup_vehicle_by_plate

# Look up a vehicle by license plate
vehicle_info = lookup_vehicle_by_plate("AB12345")

if vehicle_info.feilmelding:
    print(f"Error: {vehicle_info.feilmelding}")
else:
    print(f"Vehicle found: {vehicle_info.kjennemerke}")
    print(f"VIN: {vehicle_info.understellsnummer}")
    print(f"First registered: {vehicle_info.registrert_forstgang}")
```

### Simple lookup by VIN

```python
from norwegian_vehicle_api import lookup_vehicle_by_vin

# Look up a vehicle by VIN
vehicle_info = lookup_vehicle_by_vin("1HGBH41JXMN109186")

if vehicle_info.feilmelding:
    print(f"Error: {vehicle_info.feilmelding}")
else:
    print(f"License plate: {vehicle_info.kjennemerke}")
    print(f"KUID: {vehicle_info.kuid}")
```

### Using the API class

```python
from norwegian_vehicle_api import NorwegianVehicleAPI, VehicleAPIError

# Use context manager for proper cleanup
with NorwegianVehicleAPI() as api:
    try:
        vehicle_info = api.lookup_by_license_plate("AB12345")
        print(f"Vehicle: {vehicle_info.kjennemerke}")
    except VehicleAPIError as e:
        print(f"API Error: {e.message}")
```

### Getting raw API data

```python
with NorwegianVehicleAPI() as api:
    # Get the complete raw response
    raw_data = api.get_raw_data(license_plate="AB12345")
    print(raw_data)
```

## API Reference

### VehicleInfo Class

The simplified vehicle information object returned by lookups:

```python
@dataclass
class VehicleInfo:
    kuid: Optional[str] = None                    # Vehicle unique ID
    understellsnummer: Optional[str] = None       # VIN/chassis number
    kjennemerke: Optional[str] = None            # License plate
    merke: Optional[str] = None                  # Brand
    modell: Optional[str] = None                 # Model
    arsmodell: Optional[str] = None              # Year model
    egenvekt: Optional[int] = None               # Curb weight (kg)
    totalvekt: Optional[int] = None              # Total weight (kg)
    drivstoff: Optional[str] = None              # Fuel type
    eier_navn: Optional[str] = None              # Owner name
    eier_adresse: Optional[str] = None           # Owner address
    registrert_forstgang: Optional[str] = None   # First registration date
    kontrollfrist: Optional[str] = None          # Inspection due date
    feilmelding: Optional[str] = None            # Error message if any
```

### NorwegianVehicleAPI Class

Main API client class:

```python
class NorwegianVehicleAPI:
    def __init__(self, api_key=None, base_url=None, timeout=30, enable_logging=False)

    def lookup_by_license_plate(self, license_plate: str) -> VehicleInfo
    def lookup_by_vin(self, vin: str) -> VehicleInfo
    def get_raw_data(self, license_plate=None, vin=None) -> Dict[str, Any]
    def test_connection(self) -> bool
```

### Convenience Functions

```python
def lookup_vehicle_by_plate(license_plate: str, api_key: Optional[str] = None) -> VehicleInfo
def lookup_vehicle_by_vin(vin: str, api_key: Optional[str] = None) -> VehicleInfo
```

## Error Handling

The client includes comprehensive error handling:

```python
from norwegian_vehicle_api import VehicleAPIError

try:
    vehicle_info = lookup_vehicle_by_plate("INVALID")
except VehicleAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
    print(f"Details: {e.details}")
```

Common error scenarios:

- **400**: Bad request (invalid parameters)
- **422**: Quota exceeded (retry after midnight Norwegian time)
- **429**: Rate limited (retry after specified time)
- **500+**: Server errors

## Configuration

### Environment Variables

| Variable               | Description                | Default                                         |
| ---------------------- | -------------------------- | ----------------------------------------------- |
| `VEHICLE_API_KEY`      | API key for authentication | None                                            |
| `VEHICLE_API_BASE_URL` | Base URL for the API       | https://akfell-datautlevering.atlas.vegvesen.no |
| `VEHICLE_API_TIMEOUT`  | Request timeout in seconds | 30                                              |
| `LOG_LEVEL`            | Logging level              | INFO                                            |
| `ENABLE_DEBUG_LOGGING` | Enable debug logging       | false                                           |

## Examples

Run the example script to see the API in action:

```bash
python example_vehicle_lookup.py
```

The example script includes:

- License plate lookup
- VIN lookup
- Raw data access
- Connection testing
- Interactive mode for manual testing

## API Documentation

This client is based on the official Swagger documentation:
https://akfell-datautlevering.atlas.vegvesen.no/swagger-ui/index.html

## Rate Limiting and Quotas

The Norwegian Vehicle API has rate limits and daily quotas:

- Respect the `Retry-After` header for rate limiting
- Daily quotas reset at midnight Norwegian time
- The client automatically handles retry logic

## Data Models

The client includes comprehensive Pydantic models for type safety:

- `KjoretoydataResponse`: Main response model
- `EnkeltOppslagKjoretoydata`: Individual vehicle data
- `KjoretoyIdentitetBegrenset`: Vehicle identity
- `Kjennemerke`: License plate information
- `EierskapBegrenset`: Ownership information
- And many more detailed technical data models

## Integration with Existing Project

This API client can be easily integrated with your existing ANPR (Automatic Number Plate Recognition) system:

```python
# Example integration with license plate detection
from license_plate_reader import extract_license_plate
from norwegian_vehicle_api import lookup_vehicle_by_plate

def process_vehicle_image(image_path):
    # Extract license plate from image
    license_plate = extract_license_plate(image_path)

    if license_plate:
        # Look up vehicle information
        vehicle_info = lookup_vehicle_by_plate(license_plate)

        if not vehicle_info.feilmelding:
            return {
                'license_plate': license_plate,
                'vehicle_info': vehicle_info
            }

    return None
```

## Dependencies

- `requests`: HTTP client library
- `pydantic`: Data validation and parsing
- `python-dotenv`: Environment variable management (optional)

## License

This implementation is for educational and development purposes. Make sure to comply with the terms of service of the Norwegian Vehicle Data API and any applicable data protection regulations.

## Support

For issues with the API itself, refer to the official Statens Vegvesen documentation. For issues with this client implementation, please check the error messages and ensure your API credentials are correctly configured.
