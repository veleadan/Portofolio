import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time
from typing import Dict, Tuple, Optional
import json
from pathlib import Path
import re
import logging

# Get the logger from the main module
logger = logging.getLogger(__name__)

class CityGeocoder:
    def __init__(self, cache_file: str = 'output/data/city_coordinates.json'):
        """Initialize the geocoder with a cache file for storing coordinates."""
        self.geolocator = Nominatim(user_agent="src/hyrox_crawler")
        self.cache_file = cache_file
        self.coordinates_cache = self._load_cache()

    def _load_cache(self) -> Dict[str, Dict[str, float]]:
        """Load the coordinates cache from file."""
        try:
            if Path(self.cache_file).exists():
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Error loading cache: {e}")
            return {}

    def _save_cache(self) -> None:
        """Save the coordinates cache to file."""
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.coordinates_cache, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving cache: {e}")

    def _extract_city_from_title(self, title: str) -> str:
        """Extract city name from the event title."""
        # Remove common prefixes
        prefixes = ['HYROX', 'F45', 'AIA', 'Cigna Healthcare', 'Smart Fit', 'Sports World', 
                   'Adrenalin', 'Intersport', 'LET\'S GO FITNESS', 'FITNESS PARK', 'Sports Direct']
        
        for prefix in prefixes:
            title = title.replace(prefix, '').strip()
        
        # Remove any remaining special characters and extra spaces
        city = re.sub(r'[^\w\s]', '', title).strip()
        
        # Handle special cases
        special_cases = {
            'Ciudad de México': 'Mexico City',
            'Roma': 'Rome',
            'Gdansk': 'Gdańsk',
            'Poznan': 'Poznań'
        }
        
        return special_cases.get(city, city)

    def get_coordinates(self, city: str, country: str = '') -> Optional[Tuple[float, float]]:
        """
        Get coordinates for a city, using cache if available.
        Returns (latitude, longitude) or None if not found.
        """
        # Create a cache key
        cache_key = f"{city.lower()},{country.lower()}" if country else city.lower()
        
        # Check cache first
        if cache_key in self.coordinates_cache:
            coords = self.coordinates_cache[cache_key]
            return coords['lat'], coords['lon']

        # If not in cache, geocode the city
        try:
            # Add a small delay to respect rate limits
            time.sleep(1)
            
            # Prepare the query
            query = f"{city}, {country}" if country else city
            
            # Get location
            location = self.geolocator.geocode(query)
            
            if location:
                # Cache the result
                self.coordinates_cache[cache_key] = {
                    'lat': location.latitude,
                    'lon': location.longitude
                }
                self._save_cache()
                return location.latitude, location.longitude
            else:
                logger.warning(f"Could not find coordinates for: {query}")
                return None
                
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            logger.error(f"Geocoding error for {city}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error for {city}: {e}")
            return None

    def process_events_file(self, input_file: str, output_file: str) -> None:
        """
        Process the events CSV file and add coordinates for each city.
        """
        try:
            # Read the CSV file
            df = pd.read_csv(input_file)
            
            # Add new columns for coordinates
            df['latitude'] = None
            df['longitude'] = None
            df['city_name'] = None
            
            # Process each row
            for idx, row in df.iterrows():
                # Extract city name from title
                city_name = self._extract_city_from_title(row['title'])
                df.at[idx, 'city_name'] = city_name
                
                logger.info(f"Processing city: {city_name}")
                coords = self.get_coordinates(city_name)
                
                if coords:
                    lat, lon = coords
                    df.at[idx, 'latitude'] = lat
                    df.at[idx, 'longitude'] = lon
            
            # Save the updated dataframe
            df.to_csv(output_file, index=False, encoding='utf-8')
            logger.info(f"Updated events saved to {output_file}")
            
        except Exception as e:
            logger.error(f"Error processing events file: {e}")

def main():
    # Example usage
    geocoder = CityGeocoder()
    geocoder.process_events_file('output/data/hyrox_events.csv', 'output/data/hyrox_events_with_coordinates.csv')

if __name__ == "__main__":
    main() 