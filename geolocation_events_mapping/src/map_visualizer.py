import pandas as pd
import folium
from folium.plugins import MarkerCluster
import logging
from folium import Icon, DivIcon
from pathlib import Path

# Get the logger from the main module
logger = logging.getLogger(__name__)

class MapVisualizer:
    def __init__(self, center_lat: float = 20, center_lon: float = 0, zoom_start: int = 2):
        """Initialize the map with default center and zoom level."""
        self.map = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=zoom_start,
            tiles='CartoDB positron'  # Using a clean, light map style
        )
        self.marker_cluster = MarkerCluster().add_to(self.map)
        
        # Define marker colors based on event type
        self.marker_colors = {
            'World Championships': 'red',
            'Open': 'blue',
            'Championships': 'purple',
            'default': 'green'
        }

    def _get_marker_color(self, title: str) -> str:
        """Determine marker color based on event title."""
        for event_type, color in self.marker_colors.items():
            if event_type.lower() in title.lower():
                return color
        return self.marker_colors['default']

    def _create_custom_icon(self, color: str) -> Icon:
        """Create a custom icon for the marker."""
        return Icon(
            color=color,
            icon='info-sign',  # Using Font Awesome icon
            prefix='fa',  # Font Awesome prefix
            icon_color='white'
        )

    def add_event_markers(self, events_file: str) -> None:
        """Add markers for each event from the CSV file."""
        try:
            # Check if file exists
            events_path = Path(events_file)
            if not events_path.exists():
                logger.error(f"Events file not found: {events_file}")
                logger.info("Please run the city_geocoder.py script first to generate the coordinates file.")
                return

            # Read the events file
            df = pd.read_csv(events_file)
            
            # Check if required columns exist
            required_columns = ['latitude', 'longitude', 'title', 'date', 'city_name', 'url']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                logger.error(f"Missing required columns in CSV: {missing_columns}")
                return
            
            # Filter out rows without coordinates
            df = df.dropna(subset=['latitude', 'longitude'])
            
            if len(df) == 0:
                logger.warning("No events with valid coordinates found in the file.")
                return
            
            # Add markers for each event
            for _, row in df.iterrows():
                # Create popup content with styling
                popup_content = f"""
                <div style='font-family: Arial, sans-serif;'>
                    <h3 style='color: #333; margin-bottom: 10px;'>{row['title']}</h3>
                    <p style='margin: 5px 0;'><strong>Date:</strong> {row['date']}</p>
                    <p style='margin: 5px 0;'><strong>Location:</strong> {row['city_name']}</p>
                    <a href="{row['url']}" target="_blank" 
                       style='display: inline-block; 
                              background-color: #007bff; 
                              color: white; 
                              padding: 5px 10px; 
                              text-decoration: none; 
                              border-radius: 3px; 
                              margin-top: 10px;'>
                        Event Details
                    </a>
                </div>
                """
                
                # Get marker color based on event type
                marker_color = self._get_marker_color(row['title'])
                
                # Create marker with custom icon
                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_content, max_width=300),
                    tooltip=row['city_name'],
                    icon=self._create_custom_icon(marker_color)
                ).add_to(self.marker_cluster)
                
            logger.info(f"Added {len(df)} event markers to the map")
            
        except Exception as e:
            logger.error(f"Error adding markers: {e}")

    def save_map(self, output_file: str = 'output/map/hyrox_events_map.html') -> None:
        """Save the map to an HTML file."""
        try:
            self.map.save(output_file)
            logger.info(f"Map saved to {output_file}")
        except Exception as e:
            logger.error(f"Error saving map: {e}")

def main():
    # Create the map
    visualizer = MapVisualizer()
    
    # Add event markers
    visualizer.add_event_markers('output/data/hyrox_events_with_coordinates.csv')
    
    # Save the map
    visualizer.save_map()

if __name__ == "__main__":
    main() 