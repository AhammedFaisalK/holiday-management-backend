# Holiday Management Backend

This is the backend service for the Holiday Management Application, built with Django and Django REST Framework. It integrates with the Calendarific API to fetch and manage public holidays.

## Features
- Fetch holidays from the Calendarific API.
- Cache holiday data using Django's core caching system.
- Filter holidays by country, year, month, query, and type.
- Paginated API responses.
- Uses Django Query Counter for debugging and optimizing database queries.

## Tech Stack
- **Framework**: Django, Django REST Framework
- **Database**: SQLite (default, can be changed to PostgreSQL or others)
- **Caching**: Django Core Cache
- **External API**: Calendarific API

## Installation

### Prerequisites
- Python 3.11+
- Virtual environment (recommended)

### Setup
```sh
# Clone the repository
git clone <repo-url>
cd holiday-management

# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp config/.env.example config/.env
# Update `.env` with required values (see Environment Variables section)

# Apply migrations
python manage.py migrate

# Run the development server
python manage.py runserver
```

## Environment Variables
Create a `.env` file inside the `config` directory with the following variables:
```ini
DJANGO_SECRET_KEY=your_secret_key
DEBUG=True
CALENDARIFIC_API_KEY=your_calendarific_api_key
CALENDARIFIC_BASE_URL=https://calendarific.com/api/v2
```

## API Endpoints

### Get Holidays
```http
GET /api/v1/holidays/
```
#### Query Parameters:
| Parameter    | Type   | Description                        |
|-------------|--------|------------------------------------|
| country_code | string | Country code (ISO 3166-1 alpha-2) |
| year        | int    | Year of holidays                   |
| month       | int    | (Optional) Filter by month         |
| query       | string | (Optional) Search for holiday name |
| holiday_type | string | (Optional) Filter by holiday type  |

#### Example Request:
```http
GET /api/v1/holidays/?country_code=US&year=2025&month=12
```

## Caching
This project uses Django's core caching system to optimize performance. Holidays are cached in memory and stored in the database.

## Debugging Queries
The project includes `django-query-counter` to monitor and optimize queries. Logs will display the number of queries executed per request.

## Running Tests
```sh
python manage.py test
```

## License
MIT License

