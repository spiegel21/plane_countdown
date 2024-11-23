from datetime import datetime
import pytz

def get_next_flights(departures, arrivals, now):
    """Get the next departure and arrival"""
    next_departure = None
    next_arrival = None
    
    if departures and "scheduled_departures" in departures:
        # Find next departure
        for flight in departures["scheduled_departures"]:
            if flight.get("estimated_off") and not flight.get("actual_off"):
                est_time = datetime.fromisoformat(flight["estimated_off"].replace('Z', '+00:00'))
                if est_time > now:
                    if next_departure is None or est_time < datetime.fromisoformat(next_departure["estimated_off"].replace('Z', '+00:00')):
                        next_departure = flight

    if arrivals and "scheduled_arrivals" in arrivals:
        # Find next arrival
        for flight in arrivals["scheduled_arrivals"]:
            if flight.get("estimated_on") and not flight.get("actual_on"):
                est_time = datetime.fromisoformat(flight["estimated_on"].replace('Z', '+00:00'))
                if est_time > now:
                    if next_arrival is None or est_time < datetime.fromisoformat(next_arrival["estimated_on"].replace('Z', '+00:00')):
                        next_arrival = flight
                    
    return next_departure, next_arrival

def format_countdown(seconds):
    """Format seconds into HH:MM:SS"""
    if seconds < 0:
        return "Departed/Arrived"
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

def format_flight_info(flight, flight_type):
    """Format flight information for display"""
    if flight_type == "departure":
        return (f"Flight: {flight['ident_iata']} to {flight['destination']['city']}\n"
                f"Gate: {flight['gate_origin'] or 'N/A'}\n"
                f"Terminal: {flight['terminal_origin'] or 'N/A'}\n"
                f"Status: {flight['status']}")
    else:
        return (f"Flight: {flight['ident_iata']} from {flight['origin']['city']}\n"
                f"Gate: {flight['gate_destination'] or 'N/A'}\n"
                f"Terminal: {flight['terminal_destination'] or 'N/A'}\n"
                f"Status: {flight['status']}")