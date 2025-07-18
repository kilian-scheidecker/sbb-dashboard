from datetime import datetime

import requests

def main():

    dep_time = datetime.now().replace(minute=31).strftime('%Y-%m-%d %H:%M')

    station = 'Winterthur'

    request = (
        "https://transport.opendata.ch/v1/stationboard?"
        f"station={station}&"
        f"datetime={dep_time}"
    )

    data = requests.get("https://transport.opendata.ch/v1/stationboard?station=Winterthur&transportations=train").json()
    print("Hello from sbb-dashboard!")


if __name__ == "__main__":
    main()
