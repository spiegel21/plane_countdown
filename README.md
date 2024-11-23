# San Diego Airport Flight Tracker

A real-time flight tracking application for San Diego International Airport (SAN) built with Streamlit and the FlightAware AeroAPI.

![Airport Tracker Demo](https://via.placeholder.com/800x400.png?text=SAN+Flight+Tracker+Demo)

## Features

- Real-time flight tracking for arrivals and departures
- Live countdown timers for upcoming flights
- Runway usage highlighting (Runway 9 arrivals and Runway 27 departures)
- Automatic removal of completed flights
- Gate and terminal information
- Flight status updates every 30 seconds
- Detailed flight information tables
- Progress bars for flight timing
- Mobile-responsive design

## Prerequisites

Before running this application, you'll need:

- Python 3.8 or higher
- A FlightAware AeroAPI key ([Get one here](https://flightaware.com/commercial/aeroapi/))
- pip package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/san-flight-tracker.git
cd san-flight-tracker
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your FlightAware API key:
```env
FLIGHTAWARE_API_KEY=your_api_key_here
```

## Project Structure

```
flight_tracker/
├── src/
│   ├── __init__.py
│   ├── data_fetcher.py    # Handles API communication
│   ├── flight_processor.py # Core business logic
│   ├── ui_components.py   # Streamlit UI components
│   └── main.py           # Application entry point
├── .env
├── requirements.txt
└── README.md
```

## Usage

Run the application using Streamlit:
```bash
streamlit run src/main.py
```

The application will be available at `http://localhost:8501` by default.

## Features in Detail

### Real-time Tracking
- Updates flight information every 30 seconds
- Removes completed flights automatically
- Shows countdown timers for upcoming flights

### Runway Highlights
- Highlights flights arriving on Runway 9
- Highlights flights departing from Runway 27
- Visual indicators for runway usage

### Flight Information
- Flight number
- Origin/Destination city
- Gate assignments
- Terminal information
- Estimated arrival/departure times
- Flight status
- Progress indicators

## Contributing

1. Fork the repository
2. Create a feature branch:
```bash
git checkout -b feature/YourFeatureName
```
3. Commit your changes:
```bash
git commit -m 'Add some feature'
```
4. Push to the branch:
```bash
git push origin feature/YourFeatureName
```
5. Open a Pull Request

## Technical Details

### Components

- **data_fetcher.py**: Handles all API communication with FlightAware and local JSON storage
- **flight_processor.py**: Contains core business logic for flight data processing
- **ui_components.py**: Manages all Streamlit UI components and display logic
- **main.py**: Orchestrates the application flow and manages state

### Data Refresh Strategy

- API calls are made every 30 seconds to update flight information
- Local JSON files are used as a cache between API calls
- Session state manages data persistence between Streamlit reruns

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- FlightAware for providing the AeroAPI
- Streamlit team for the excellent framework
- San Diego International Airport

## Support

For support, please open an issue in the GitHub repository or contact [your contact information].
