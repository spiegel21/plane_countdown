import streamlit as st
from datetime import datetime
import time
from flight_processor import format_countdown, format_flight_info
from data_fetcher import fetch_flight_data
from flight_processor import get_next_flights

def display_next_flight(flight, flight_type, now):
    """Display the next flight information with countdown"""
    if flight:
        # Get the target time based on flight type
        if flight_type == "departure":
            est_time = datetime.fromisoformat(flight["estimated_off"].replace('Z', '+00:00'))
        else:
            est_time = datetime.fromisoformat(flight["estimated_on"].replace('Z', '+00:00'))
        
        # Create empty containers
        countdown_container = st.empty()
        progress_container = st.empty()
        
        # Update the countdown and progress
        def update_countdown():
            """Update the countdown value and progress bar in the containers"""
            current_time = datetime.now(est_time.tzinfo)
            seconds_remaining = int((est_time - current_time).total_seconds())
            
            # Check if flight has departed/arrived
            if seconds_remaining < 0:
                # Fetch new flight data
                departures, arrivals = fetch_flight_data()
                if departures and arrivals:
                    st.session_state.flight_data = (departures, arrivals)
                    st.session_state.last_fetch_time = current_time
                    # Force a rerun to update the display
                    st.rerun()
                return 0
            
            # Update countdown display
            countdown_container.markdown(
                f"<h2 style='font-family: monospace;'>{format_countdown(seconds_remaining)}</h2>",
                unsafe_allow_html=True
            )
            
            # Update progress bar
            progress = 1.0 - min(1.0, max(0.0, seconds_remaining / 300))
            progress_container.progress(progress)
            
            return seconds_remaining
        
        # Display initial countdown
        seconds_left = update_countdown()
        
        # Display flight information
        st.text(format_flight_info(flight, flight_type))
        
        # Return the update function so it can be called from the main loop
        return update_countdown
    else:
        st.write(f"No upcoming {flight_type}s")
        return None
    

def display_flight_tables(departures, arrivals):
    """Display the departure and arrival tables"""
    tab1, tab2 = st.tabs(["🛫 Departures", "🛬 Arrivals"])
    now = datetime.now().astimezone()
    
    with tab1:
        if departures and "scheduled_departures" in departures:
            departure_data = []
            for flight in departures["scheduled_departures"][:10]:
                if flight.get("estimated_off"):
                    estimated_time = datetime.fromisoformat(flight["estimated_off"].replace('Z', '+00:00')).astimezone()
                    departure_data.append({
                        "Flight": flight["ident_iata"],
                        "Destination": flight["destination"]["city"],
                        "Estimated Time": estimated_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        "Gate": flight["gate_origin"] or "N/A",
                        "Status": flight["status"]
                    })
            departure_data = [flight for flight in departure_data if datetime.strptime(flight["Estimated Time"], '%Y-%m-%d %H:%M:%S %Z').astimezone() > now]
            departure_data.sort(key=lambda x: x["Estimated Time"])
            st.dataframe(departure_data, use_container_width=True)
        else:
            st.write("No departure data available")
    
    with tab2:
        if arrivals and "scheduled_arrivals" in arrivals:
            arrival_data = []
            for flight in arrivals["scheduled_arrivals"][:10]:
                if flight.get("estimated_on"):
                    estimated_time = datetime.fromisoformat(flight["estimated_on"].replace('Z', '+00:00')).astimezone()
                    arrival_data.append({
                        "Flight": flight["ident_iata"],
                        "Origin": flight["origin"]["city"],
                        "Estimated Time": estimated_time.strftime('%Y-%m-%d %H:%M:%S %Z'),
                        "Gate": flight["gate_destination"] or "N/A",
                        "Status": flight["status"]
                    })
            arrival_data = [flight for flight in arrival_data if datetime.strptime(flight["Estimated Time"], '%Y-%m-%d %H:%M:%S %Z').astimezone() > now]
            arrival_data.sort(key=lambda x: x["Estimated Time"])
            st.dataframe(arrival_data, use_container_width=True)
        else:
            st.write("No arrival data available")