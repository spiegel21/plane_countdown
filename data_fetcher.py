import requests
import os
import json
import streamlit as st
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

def fetch_flight_data():
    """Fetch flight data from FlightAware AeroAPI""" 
    # Load environment variables
    load_dotenv()
    api_key = os.getenv("FLIGHTAWARE_API_KEY")
    
    if not api_key:
        st.error("FlightAware API key not found. Please check your .env file.")
        return None, None
    
    # FlightAware AeroAPI configuration
    base_url = "https://aeroapi.flightaware.com/aeroapi"
    airport_code = "KSAN"
    headers = {
        "x-apikey": api_key,
        "Content-Type": "application/json"
    }

    try:
        # Fetch arrivals
        arrivals_endpoint = f"/airports/{airport_code}/flights/scheduled_arrivals"
        now_time = (datetime.now(pytz.UTC) - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S')
        later_time = (datetime.now(pytz.UTC) + timedelta(hours=3)).strftime('%Y-%m-%dT%H:%M:%S')
        arrivals_response = requests.get(
            f"{base_url}{arrivals_endpoint}",
            headers=headers,
            params={
                "start": now_time,
                "end": later_time
            }
        )
        arrivals_response.raise_for_status()
        
        # Fetch departures
        departures_endpoint = f"/airports/{airport_code}/flights/scheduled_departures"
        departures_response = requests.get(
            f"{base_url}{departures_endpoint}",
            headers=headers,
            params={
                "start": now_time,
                "end": later_time
            }
        )
        departures_response.raise_for_status()
        
        return departures_response.json(), arrivals_response.json()
    
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching flight data: {str(e)}")
        return None, None