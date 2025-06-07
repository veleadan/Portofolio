# HYROX Events Crawler

This is a web crawler designed to extract event information from the HYROX website (https://hyrox.com/find-my-race/).

## Features

- Extracts event information including title, date, location, and URL
- Saves data in both CSV and JSON formats
- Includes error handling and logging
- Respects website's robots.txt and includes proper headers

## Installation

1. Clone this repository
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the crawler:
```bash
python hyrox_crawler.py
```

The script will:
1. Fetch the HYROX events page
2. Parse the event information
3. Save the results to both `hyrox_events.csv` and `hyrox_events.json`

## Output Format

The crawler generates two files:

1. `hyrox_events.csv`: Comma-separated values file containing all events
2. `hyrox_events.json`: JSON file containing the same information in a structured format

Each event contains the following information:
- Title
- Date
- Location
- URL

## Notes

- The crawler includes proper headers and respects website policies
- Error handling and logging are implemented for better debugging
- The script can be modified to extract additional information as needed

## License

MIT License 