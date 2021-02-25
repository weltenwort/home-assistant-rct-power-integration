"""Sample API Client."""
from asyncio import StreamReader, StreamWriter, open_connection, TimeoutError
from asyncio.locks import Lock
from dataclasses import dataclass
from datetime import datetime
import logging
import socket
from typing import Dict, Generic, List, Optional, Tuple, TypeVar, Union

import async_timeout
from homeassistant.helpers.update_coordinator import UpdateFailed
from rctclient.exceptions import FrameCRCMismatch
from rctclient.frame import ReceiveFrame, SendFrame
from rctclient.registry import REGISTRY
from rctclient.types import Command, DataType, EventEntry, FrameType
from rctclient.utils import decode_value

CONNECTION_TIMEOUT = 20
READ_TIMEOUT = 20

_LOGGER: logging.Logger = logging.getLogger(__package__)

INVERTER_SN_OID = 0x7924ABD9

ApiResponseValue = Union[
    bool,
    bytes,
    float,
    int,
    str,
    Tuple[datetime, Dict[datetime, int]],
    Tuple[datetime, Dict[datetime, EventEntry]],
]
DefaultResponseValue = TypeVar("DefaultResponseValue")


@dataclass
class BaseApiResponse:
    object_id: int
    time: datetime


@dataclass
class ValidApiResponse(BaseApiResponse):
    type: DataType
    value: ApiResponseValue


@dataclass
class InvalidApiResponse(BaseApiResponse):
    cause: str


ApiResponse = Union[ValidApiResponse, InvalidApiResponse]
RctPowerData = Dict[int, ApiResponse]


def get_valid_response_value_or(
    response: Optional[ApiResponse],
    defaultValue: DefaultResponseValue,
) -> Union[ApiResponseValue, DefaultResponseValue]:
    if isinstance(response, ValidApiResponse):
        return response.value
    else:
        return defaultValue


class RctPowerApiClient:
    def __init__(self, hostname: str, port: int) -> None:
        """Sample API Client."""
        self._hostname = hostname
        self._port = port

        # ensure only one connection at a time is established because the
        # inverter's firmware doesn't handle it well at the time of writing
        self._connection_lock = Lock()

    async def get_serial_number(self) -> Optional[str]:
        inverter_data = await self.async_get_data([INVERTER_SN_OID])

        inverter_sn_response = inverter_data.get(INVERTER_SN_OID)

        if isinstance(inverter_sn_response, ValidApiResponse) and isinstance(
            inverter_sn_response.value, str
        ):
            return inverter_sn_response.value
        else:
            return None

    async def async_get_data(self, object_ids: List[int]) -> RctPowerData:
        async with self._connection_lock:
            async with async_timeout.timeout(CONNECTION_TIMEOUT):
                reader, writer = await open_connection(
                    host=self._hostname, port=self._port
                )

                try:
                    if reader.at_eof():
                        raise UpdateFailed("Read stream closed")

                    return {
                        object_id: await self._read_object(
                            reader=reader, writer=writer, object_id=object_id
                        )
                        for object_id in object_ids
                    }
                finally:
                    writer.close()

    async def _read_object(
        self, reader: StreamReader, writer: StreamWriter, object_id: int
    ):
        read_command_frame = SendFrame(command=Command.READ, id=object_id)
        response_frame = ReceiveFrame()

        _LOGGER.debug("Requesting RCT Power data for object %x...", object_id)
        request_time = datetime.now()

        try:
            async with async_timeout.timeout(READ_TIMEOUT):
                await writer.drain()
                writer.write(read_command_frame.data)

                while not response_frame.complete() and not reader.at_eof():
                    raw_response = await reader.read(1)

                    if len(raw_response) > 0:
                        response_frame.consume(raw_response)

            if response_frame.is_complete():
                data_type = REGISTRY.type_by_id(object_id)
                decoded_value = decode_value(data_type, response_frame.data)

                return ValidApiResponse(
                    object_id=object_id,
                    time=request_time,
                    type=data_type,
                    value=decoded_value,
                )
            else:
                return InvalidApiResponse(
                    object_id=object_id, time=request_time, cause="INCOMPLETE"
                )

        except TimeoutError:
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="OBJECT_READ_TIMEOUT"
            )
        except FrameCRCMismatch:
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="CRC_ERROR"
            )
