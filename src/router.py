from datetime import datetime

import requests
from fastapi import APIRouter

from structs import DATA_TABLE, TrainInfo, APIResponse


next_departure_router = APIRouter()


@next_departure_router.get(
    '/get/next/departure/{departure}/{destination}',
    response_model=APIResponse
)
def get_next_departure(
        departure: str,
        destination: str
    ) -> APIResponse :

    if departure not in DATA_TABLE.keys() :
        raise NotImplementedError(f'Departure from {departure} is not supported yet. Please add it to the configuration file "config_files/data_table.yaml".')
    if destination not in DATA_TABLE[departure].keys() :
        raise NotImplementedError(f'Destination {destination} is not supported yet with departure from {departure}. Please add it to the configuration file "config_files/data_table.yaml".')

    now = datetime.now()

    # Find the next departure time for the departure - destination tuple
    try :
        next_departure = next(x for x in DATA_TABLE[departure][destination] if x > now.minute)
        departure_time_str = now.replace(minute=next_departure).strftime('%H:%M')
    except StopIteration :
        next_departure = DATA_TABLE[departure][destination][0]
        departure_time_str = now.replace(hour= now.hour+1, minute=next_departure).strftime('%H:%M')

    # Generate the next departure time as str
    complete_str = f'{datetime.now().strftime('%Y-%m-%d')}T{departure_time_str}'

    # Request to transport API
    journeys = requests.get(
        url = "https://transport.opendata.ch/v1/stationboard",
        params = {
            'station': departure,
            'datetime': departure_time_str,
        }
    ).json()['stationboard']

    # Find the correct train in the list of journeys
    for journey in journeys :
        if complete_str in journey['stop']['departure'] and destination in [d['station']['name'] for d in journey['passList']]:
            break

    # Return the train information
    NextTrain = TrainInfo(
        category = journey['category'],
        number = journey['number'],
        destination = journey['to'],
        departure_time = journey['stop']['departureTimestamp'],
        platform = journey['stop']['platform'],
        delay = journey['stop']['delay'],
    )


    return APIResponse.from_delay(
        delayed = (NextTrain.delay != 0),
        message = NextTrain.to_str())

