import os
import tomllib
from typing import Union, Literal
from datetime import datetime

from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv(override=True)





with open(os.environ['DATA_TABLE_PATH'], 'rb') as f :
    DATA_TABLE = tomllib.load(f)



class TrainInfo:

    def __init__(
            self,
            category: str,
            number: int,
            destination: str,
            departure_time: int,
            platform: Union[str, int],
            delay: int
        ) :
        self.name = f"{category} {number}"
        self.destination = destination
        self.departure_time = datetime.fromtimestamp(departure_time).strftime('%H:%M')
        self.platform = int(platform)
        self.delay = int(delay)


    def to_str(self) :
        if self.delay == 0 :
            return (
                f"The {self.name} to {self.destination} leaving at {self.departure_time} "
                f"from platform {self.platform} is on time."
            )

        return (
                f"The {self.name} to {self.destination} leaving at {self.departure_time} "
                f"from platform {self.platform} is delayed by {self.delay} minutes."
            )


class APIResponse(BaseModel):
    status: str
    message: str

    @classmethod
    def from_delay(cls, delayed: bool, message: str) -> "APIResponse":
        return cls(
            status="delayed" if delayed else "on_time",
            message=message
        )