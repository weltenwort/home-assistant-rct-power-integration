"""Sample API Client."""

from __future__ import annotations

import asyncio
import logging
import struct
from asyncio import StreamReader, StreamWriter, open_connection
from asyncio.locks import Lock
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar

from homeassistant.helpers.update_coordinator import UpdateFailed
from rctclient.exceptions import FrameCRCMismatch, FrameLengthExceeded, InvalidCommand
from rctclient.frame import ReceiveFrame, SendFrame
from rctclient.registry import REGISTRY
from rctclient.types import Command, EventEntry
from rctclient.utils import decode_value

CONNECTION_TIMEOUT = 20
READ_TIMEOUT = 2
INVERTER_SN_OID = 0x7924ABD9
_LOGGER: logging.Logger = logging.getLogger(__package__)

ApiResponseValue = (
    bool
    | bytes
    | float
    | int
    | str
    | tuple[datetime, dict[datetime, int]]
    | tuple[datetime, dict[datetime, EventEntry]]
)
DefaultResponseValue = TypeVar("DefaultResponseValue")


@dataclass
class BaseApiResponse:
    object_id: int
    time: datetime


@dataclass
class ValidApiResponse(BaseApiResponse):
    value: ApiResponseValue


@dataclass
class InvalidApiResponse(BaseApiResponse):
    cause: str


ApiResponse = ValidApiResponse | InvalidApiResponse
RctPowerData = dict[int, ApiResponse]


def get_valid_response_value_or(
    response: ApiResponse | None,
    defaultValue: DefaultResponseValue,
) -> ApiResponseValue | DefaultResponseValue:
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

    async def get_serial_number(self) -> str | None:
        inverter_data = await self.async_get_data([INVERTER_SN_OID])

        inverter_sn_response = inverter_data.get(INVERTER_SN_OID)

        if isinstance(inverter_sn_response, ValidApiResponse) and isinstance(
            inverter_sn_response.value, str
        ):
            return inverter_sn_response.value
        else:
            return None

    async def async_get_data(self, object_ids: list[int]) -> RctPowerData:
        async with self._connection_lock:
            async with asyncio.timeout(CONNECTION_TIMEOUT):
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
        object_name = REGISTRY.get_by_id(object_id).name
        read_command_frame = SendFrame(command=Command.READ, id=object_id)

        _LOGGER.debug(
            "Requesting RCT Power data for object %x (%s)...", object_id, object_name
        )
        request_time = datetime.now()

        try:
            async with asyncio.timeout(READ_TIMEOUT):
                await writer.drain()
                writer.write(read_command_frame.data)

                # loop until we return or time out
                while True:
                    response_frame = ReceiveFrame()

                    while not response_frame.complete() and not reader.at_eof():
                        raw_response = await reader.read(1)

                        if len(raw_response) > 0:
                            response_frame.consume(raw_response)

                    if response_frame.complete():
                        response_object_info = REGISTRY.get_by_id(response_frame.id)
                        data_type = response_object_info.response_data_type
                        received_object_name = response_object_info.name

                        # ignore, if this is not the answer to the latest request
                        if object_id != response_frame.id:
                            _LOGGER.debug(
                                "Mismatch of requested and received object ids: requested %x (%s), but received %x (%s)",
                                object_id,
                                object_name,
                                response_frame.id,
                                received_object_name,
                            )
                            continue

                        decoded_value: (
                            bool
                            | bytes
                            | float
                            | int
                            | str
                            | tuple[datetime, dict[datetime, int]]
                            | tuple[datetime, dict[datetime, EventEntry]]
                        ) = decode_value(data_type, response_frame.data)  # type: ignore

                        _LOGGER.debug(
                            "Decoded data for object %x (%s): %s",
                            response_frame.id,
                            received_object_name,
                            decoded_value,
                        )

                        return ValidApiResponse(
                            object_id=object_id,
                            time=request_time,
                            value=decoded_value,
                        )
                    else:
                        _LOGGER.debug(
                            "Error decoding object %x (%s): %s",
                            object_id,
                            object_name,
                            response_frame.data,
                        )
                        return InvalidApiResponse(
                            object_id=object_id, time=request_time, cause="INCOMPLETE"
                        )

        except TimeoutError as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id,
                time=request_time,
                cause="OBJECT_READ_TIMEOUT",
            )
        except FrameCRCMismatch as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="CRC_ERROR"
            )
        except FrameLengthExceeded as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="FRAME_LENGTH_EXCEEDED"
            )
        except InvalidCommand as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="INVALID_COMMAND"
            )
        except struct.error as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="PARSING_ERROR"
            )
        except Exception as exc:
            _LOGGER.debug(
                "Error reading object %x (%s): %s", object_id, object_name, str(exc)
            )
            return InvalidApiResponse(
                object_id=object_id, time=request_time, cause="UNKNOWN_ERROR"
            )
