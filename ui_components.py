import streamlit as st
from datetime import datetime
from flight_processor import format_countdown, format_flight_info

def display_next_flight(flight, flight_type, now):
    """Display the next flight information with countdown"""
    if flight:
        if flight_type == "departure":
            est_time = datetime.fromisoformat(flight["estimated_off"].replace('Z', '+00:00'))
        else:
            est_time = datetime.fromisoformat(flight["estimated_on"].replace('Z', '+00:00'))
        
        time_until = int((est_time - now).total_seconds())
        countdown = format_countdown(time_until)
        
        st.markdown(f"<h2 style='font-family: monospace;'>{countdown}</h2>", unsafe_allow_html=True)
        st.text(format_flight_info(flight, flight_type))
        
        progress = 1.0 - min(1.0, max(0.0, (est_time - now).total_seconds() / 3600))
        st.progress(progress)
    else:
        st.write(f"No upcoming {flight_type}s")

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