from datetime import datetime

class Cab:
    def __init__(self, driver_name, capacity, destination, time_slot):
        self.driver_name = driver_name
        self.capacity = capacity
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []

class RideRequest:
    def __init__(self, student_name, destination, time_slot, year, submission_time):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submission_time = datetime.now()


# TEST OBJECTS

cab = Cab("Raj", 2, "Delhi", "Morning")

aditi = RideRequest("Aditi", "Delhi", "Morning", 3)
vikram = RideRequest("Vikram", "Delhi", "Morning", 5)
meera = RideRequest("Meera", "Delhi", "Morning", 3)
riya = RideRequest("Riya", "Delhi", "Evening", 5)

waiting_requests = [aditi, vikram, meera, riya]

