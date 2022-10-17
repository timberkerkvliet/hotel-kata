from datetime import date
from unittest import TestCase

from hotel import Hotel, Period, Stay, BookingStatus


class TestHotel(TestCase):
    def test_all_rooms_available(self):
        hotel = Hotel(no_of_rooms=2)

        rooms = hotel.get_available_rooms(
            period=Period(arrival_date=date(2022,1 ,1), departure_date=date(2022, 1, 2))
        )

        self.assertEqual({0, 1}, rooms)

    def test_no_rooms_available(self):
        hotel = Hotel(no_of_rooms=2)
        period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 2))

        hotel.book(stay=Stay(room_no=1, period=period))
        hotel.book(stay=Stay(room_no=0, period=period))

        available_rooms = hotel.get_available_rooms(period=period)

        self.assertEqual(set(), available_rooms)

    def test_room_is_not_available_in_exact_same_period(self):
        hotel = Hotel(no_of_rooms=2)
        period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 2))
        stay = Stay(room_no=1, period=period)

        hotel.book(stay=stay)

        available_rooms = hotel.get_available_rooms(period=period)

        self.assertEqual({0}, available_rooms)

    def test_room_is_not_available_in_overlapping_period(self):
        hotel = Hotel(no_of_rooms=2)
        period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 3))
        stay = Stay(room_no=1, period=period)

        hotel.book(stay=stay)

        other_period = Period(arrival_date=date(2022, 1, 2), departure_date=date(2022, 1, 4))
        available_rooms = hotel.get_available_rooms(period=other_period)

        self.assertEqual({0}, available_rooms)

    def test_no_room_available_in_overlapping_period(self):
        hotel = Hotel(no_of_rooms=2)

        stay = Stay(
            room_no=0,
            period=Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 4))
        )
        hotel.book(stay=stay)

        stay = Stay(
            room_no=1,
            period=Period(arrival_date=date(2022, 1, 3), departure_date=date(2022, 1, 5))
        )
        hotel.book(stay=stay)

        wanted_period = Period(arrival_date=date(2022, 1, 3), departure_date=date(2022, 1, 4))
        available_rooms = hotel.get_available_rooms(period=wanted_period)

        self.assertEqual(set(), available_rooms)

    def test_one_room_available_in_overlapping_period(self):
        hotel = Hotel(no_of_rooms=2)

        stay = Stay(
            room_no=0,
            period=Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 4))
        )
        hotel.book(stay=stay)

        stay = Stay(
            room_no=1,
            period=Period(arrival_date=date(2022, 1, 3), departure_date=date(2022, 1, 5))
        )
        hotel.book(stay=stay)

        wanted_period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 2))
        available_rooms = hotel.get_available_rooms(period=wanted_period)

        self.assertEqual({1}, available_rooms)

    def test_unavailable_room_can_not_be_booked(self):
        hotel = Hotel(no_of_rooms=2)
        period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 2))
        stay = Stay(room_no=1, period=period)

        hotel.book(stay=stay)

        with self.assertRaises(Exception):
            hotel.book(stay=stay)

    def test_booking_has_status_reserved(self):
        hotel = Hotel(no_of_rooms=2)
        period = Period(arrival_date=date(2022, 1, 1), departure_date=date(2022, 1, 2))
        stay = Stay(room_no=1, period=period)

        booking_id = hotel.book(stay=stay)

        self.assertEqual(BookingStatus.RESERVED, hotel.get_booking_status(booking_id))
