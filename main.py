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
    def __init__(self, student_name, destination, time_slot, year):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submission_time = datetime.now()


# TEST OBJECTS

cab1 = Cab("Raj", 2, "Delhi", "Morning")
cab2 = Cab("Ram", 4, "Jaipur", "Morning")

aditi = RideRequest("Aditi", "Delhi", "Morning", 3)
vikram = RideRequest("Vikram", "Delhi", "Morning", 5)
meera = RideRequest("Meera", "Jaipur", "Morning", 3)
riya = RideRequest("Riya", "Jaipur", "Evening", 5)

cabs = [cab1, cab2]
waiting_requests = [aditi, vikram, meera, riya]


# MENU

while True:
    user_req = int(input('''
    CAB POOL MATCHER

    1. Add a ride request
    2. Show waiting students and cabs
    3. Find matches
    4. Dispatch a cab
    5. Quit

    Choose an option: '''))

    if user_req == 1:
        name = input("Enter your name: ")
        year = int(input("Enter your year: "))
        time_slot = input("Enter your desired time slot: ")
        destination = input("Enter your desired destination: ")

        request = RideRequest(
            name.strip(),
            destination.strip().title(),
            time_slot.strip().title(),
            year
        )
        waiting_requests.append(request)

    elif user_req == 2:
        print("*Students*")
        for travelling_student_name in waiting_requests:
            if travelling_student_name.destination == "Delhi":
                print(f"{travelling_student_name.student_name}, Delhi")

            elif travelling_student_name.destination == "Jaipur":
                print(f"{travelling_student_name.student_name}, Jaipur")

        print("*Cab Drivers*")
        for cab_driver_name in cabs:
            print(cab_driver_name.driver_name)

    elif user_req == 3:
        pass

    elif user_req == 4:
        pass

    elif user_req == 5:
        break