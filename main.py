import streamlit as st
from datetime import datetime
import time
import pytz
from data_fetcher import fetch_flight_data
from flight_processor import get_next_flights, format_countdown
from ui_components import display_next_flight, display_flight_tables

def main():
    st.set_page_config(
        page_title="SAN Airport Flight Tracker",
        page_icon="✈️",
        layout="wide"
    )
    
    # Initialize session state
    if 'last_fetch_time' not in st.session_state:
        st.session_state.last_fetch_time = None
        st.session_state.flight_data = None
    
    st.title("✈️ San Diego International Airport")
    st.subheader("Real-time Flight Countdown")
    
    # Get current time in UTC
    now = datetime.now(pytz.UTC)
    
    # Check if we need to fetch new data (every hour)
    if (st.session_state.last_fetch_time is None or 
        (now - st.session_state.last_fetch_time).total_seconds() >= 3600):
        
        # Fetch new data
        departures, arrivals = fetch_flight_data()
        if departures and arrivals:
            st.session_state.flight_data = (departures, arrivals)
            st.session_state.last_fetch_time = now
    
    # Create placeholder for countdown displays
    if st.session_state.flight_data:
        departures, arrivals = st.session_state.flight_data
        next_departure, next_arrival = get_next_flights(departures, arrivals, now)
        
        # Create two columns for departure and arrival
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Next Departure")
            departure_update = display_next_flight(next_departure, "departure", now)
        
        with col2:
            st.markdown("### Next Arrival")
            arrival_update = display_next_flight(next_arrival, "arrival", now)
        
        # Display flight tables
        st.markdown("### Upcoming Flights")
        display_flight_tables(departures, arrivals)
        
        # Update countdowns
        if departure_update or arrival_update:
            placeholder = st.empty()
            while True:
                if departure_update:
                    departure_update()
                if arrival_update:
                    arrival_update()
                time.sleep(1)
                placeholder.empty()  # This triggers a silent refresh without full page reload

if __name__ == "__main__":
    main()