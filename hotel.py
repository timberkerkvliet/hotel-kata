from __future__ import annotations

import uuid
from dataclasses import dataclass
from datetime import date
from enum import Enum
from uuid import UUID


class BookingStatus(Enum):
    RESERVED = 0
    CONFIRMED = 1
    UNCONFIRMED = 2


@dataclass
class Period:
    arrival_date: date
    departure_date: date

    def intersects_with(self, period: Period) -> bool:
        return period.arrival_date < self.departure_date \
               and period.departure_date > self.arrival_date


@dataclass
class Stay:
    room_no: int
    period: Period

    def intersects_with(self, stay: Stay) -> bool:
        return stay.room_no == self.room_no \
               and self.period.intersects_with(stay.period)


@dataclass
class Booking:
    id: UUID
    stay: Stay
    status: BookingStatus

    def intersects_with(self, stay: Stay) -> bool:
        return self.stay.intersects_with(stay)


class Hotel:
    def __init__(self, no_of_rooms: int):
        self._no_of_rooms = no_of_rooms
        self._bookings: dict[UUID, Booking] = {}

    def _is_stay_possible(self, stay: Stay) -> bool:
        return all(
            not booking.intersects_with(stay=stay)
            for booking in self._bookings.values()
        )

    def get_available_rooms(self, period: Period) -> set[int]:
        return {
            room_no for room_no in range(self._no_of_rooms)
            if self._is_stay_possible(stay=Stay(room_no=room_no, period=period))
        }

    def book(self, stay: Stay) -> UUID:
        if not self._is_stay_possible(stay=stay):
            raise ValueError('Room is not available')

        new_booking = Booking(
            id=uuid.uuid4(),
            stay=stay,
            status=BookingStatus.RESERVED
        )
        self._bookings[new_booking.id] = new_booking

        return new_booking.id

    def get_booking_status(self, booking_id: UUID) -> BookingStatus:
        return self._bookings[booking_id].status
