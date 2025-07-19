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
        departure_time_str = now.replace(minute=next_departure).strftime('%Y-%m-%d %H:%M')
    except StopIteration :
        next_departure = DATA_TABLE[departure][destination][0]
        departure_time_str = now.replace(hour= now.hour+1, minute=next_departure).strftime('%Y-%m-%d %H:%M')

    # Generate the next departure time as str
    

    # Request to transport API
    first_train = requests.get(
        url = "https://transport.opendata.ch/v1/stationboard",
        params = {
            'station': DATA_TABLE[departure],
            'datetime': departure_time_str,
            'transportations': 'train',
            'limit': '2'
        }
    ).json()['stationboard'][0]

    # Return the train information
    NextTrain = TrainInfo(
        category = first_train['category'],
        number = first_train['number'],
        destination = first_train['to'],
        departure_time = first_train['stop']['departureTimestamp'],
        platform = first_train['stop']['platform'],
        delay = first_train['stop']['delay'],
    )

    return APIResponse.from_delay(delayed=(NextTrain.delay != 0), message=NextTrain.to_str())

