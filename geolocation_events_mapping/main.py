import os
import sys

def run_script(script_name):
    print(f"\nRunning {script_name}...")
    script_path = os.path.join('src', script_name)
    os.system(f'python {script_path}')

def main():
    print("Starting HYROX crawler process...")
    
    # Run scripts in order
    run_script('hyrox_crawler.py')
    run_script('city_geocoder.py')
    run_script('map_visualizer.py')
    
    print("\nProcess completed! Check the output folder for results.")

if __name__ == "__main__":
    main() 