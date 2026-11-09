from datetime import datetime
from pathlib import Path
import heapq
import json


class Cab:
    def __init__(self, driver_name, capacity, destination, time_slot):
        self.driver_name = driver_name
        self.capacity = capacity
        self.destination = destination
        self.time_slot = time_slot
        self.has_left = False
        self.passengers = []


class RideRequest:
    next_number = 0

    def __init__(self, student_name, destination, time_slot, year):
        self.student_name = student_name
        self.destination = destination
        self.time_slot = time_slot
        self.year = year
        self.submission_time = datetime.now()

        self.request_number = RideRequest.next_number
        RideRequest.next_number += 1


def load_cabs():
    cab_file = Path(__file__).with_name("cabs.json")

    try:
        with open(cab_file, "r", encoding="utf-8") as file:
            cab_data = json.load(file)

    except FileNotFoundError:
        print("Could not find cabs.json.")
        print("Keep it in the same folder as your Python file.")
        raise SystemExit(1)

    except (json.JSONDecodeError, UnicodeDecodeError):
        print("cabs.json is not a valid UTF-8 JSON file.")
        print("Check its formatting and try again.")
        raise SystemExit(1)

    except OSError as error:
        print(f"Could not open cabs.json: {error}")
        raise SystemExit(1)

    if not isinstance(cab_data, list):
        print("cabs.json must contain a list of cab details.")
        raise SystemExit(1)

    if not cab_data:
        print("cabs.json contains no cabs.")
        raise SystemExit(1)

    cabs = []
    cab_number = 0

    for details in cab_data:
        cab_number += 1

        if not isinstance(details, dict):
            print(f"Cab {cab_number} must contain a dictionary of details.")
            raise SystemExit(1)

        required_fields = [
            "driver_name",
            "capacity",
            "destination",
            "time_slot"
        ]

        for field in required_fields:
            if field not in details:
                print(f"Cab {cab_number} is missing '{field}'.")
                raise SystemExit(1)

        driver_name = details["driver_name"]
        capacity = details["capacity"]
        destination = details["destination"]
        time_slot = details["time_slot"]

        if not isinstance(driver_name, str):
            print(f"Cab {cab_number}: driver_name must be text.")
            raise SystemExit(1)

        driver_name = driver_name.strip()

        if not driver_name:
            print(f"Cab {cab_number}: driver_name cannot be empty.")
            raise SystemExit(1)

        if type(capacity) is not int:
            print(f"Cab {cab_number}: capacity must be a whole number.")
            raise SystemExit(1)

        if not 1 <= capacity <= 4:
            print(f"Cab {cab_number}: capacity must be from 1 to 4.")
            raise SystemExit(1)

        if not isinstance(destination, str):
            print(f"Cab {cab_number}: destination must be text.")
            raise SystemExit(1)

        destination = destination.strip().title()

        if destination not in ("Delhi", "Jaipur"):
            print(f"Cab {cab_number}: destination must be Delhi or Jaipur.")
            raise SystemExit(1)

        if not isinstance(time_slot, str):
            print(f"Cab {cab_number}: time_slot must be text.")
            raise SystemExit(1)

        time_slot = time_slot.strip().title()

        if time_slot not in ("Morning", "Afternoon", "Evening", "Night"):
            print(
                f"Cab {cab_number}: time_slot must be "
                "Morning, Afternoon, Evening, or Night."
            )
            raise SystemExit(1)

        cab = Cab(driver_name, capacity, destination, time_slot)
        cabs.append(cab)

    return cabs


def add_request(waiting_requests, request):
    trip = (request.destination, request.time_slot)

    heapq.heappush(
        waiting_requests[trip],
        (-request.year, request.request_number, request)
    )


def find_matches(cabs, waiting_requests):
    temporary_queues = {}

    for trip, queue in waiting_requests.items():
        temporary_queues[trip] = queue.copy()

    matches_by_cab = {}

    for cab in cabs:
        if cab.has_left:
            continue

        trip = (cab.destination, cab.time_slot)
        queue = temporary_queues[trip]
        cab_matches = []

        while queue and len(cab_matches) < cab.capacity:
            entry = heapq.heappop(queue)
            student = entry[2]
            cab_matches.append(student)

        matches_by_cab[cab] = cab_matches

    return matches_by_cab


# LOAD CABS

cabs = load_cabs()


# TEST OBJECTS

# Requests are created in arrival order
aditi = RideRequest("Aditi", "Delhi", "Morning", 3)
vikram = RideRequest("Vikram", "Delhi", "Morning", 5)
meera = RideRequest("Meera", "Jaipur", "Morning", 3)
riya = RideRequest("Riya", "Jaipur", "Evening", 1)
arjun = RideRequest("Arjun", "Delhi", "Morning", 5)
neha = RideRequest("Neha", "Delhi", "Morning", 4)
kabir = RideRequest("Kabir", "Delhi", "Morning", 3)
isha = RideRequest("Isha", "Delhi", "Evening", 2)
rohan = RideRequest("Rohan", "Delhi", "Evening", 5)
sana = RideRequest("Sana", "Delhi", "Evening", 4)
dev = RideRequest("Dev", "Jaipur", "Morning", 5)
tara = RideRequest("Tara", "Jaipur", "Morning", 4)
aman = RideRequest("Aman", "Jaipur", "Morning", 2)
priya = RideRequest("Priya", "Jaipur", "Morning", 1)
zoya = RideRequest("Zoya", "Jaipur", "Evening", 4)
om = RideRequest("Om", "Delhi", "Night", 5)

test_requests = [
    aditi, vikram, meera, riya,
    arjun, neha, kabir, isha,
    rohan, sana, dev, tara,
    aman, priya, zoya, om
]

waiting_requests = {}

for destination in ("Delhi", "Jaipur"):
    for time_slot in ("Morning", "Afternoon", "Evening", "Night"):
        trip = (destination, time_slot)
        waiting_requests[trip] = []

for request in test_requests:
    add_request(waiting_requests, request)


# MENU

while True:
    try:
        user_req = int(input('''
    CAB POOL MATCHER

    1. Add a ride request
    2. Show waiting students and cabs
    3. Find matches
    4. Dispatch a cab
    5. Quit

    Choose an option: '''))

    except ValueError:
        print("Enter a whole number from 1 to 5.")
        continue

    if user_req == 1:  # Add ride request
        while True:
            name = input("Enter your name: ").strip().title()
            if name:
                break
            print("Name cannot be empty.")

        while True:
            try:
                year = int(input("Enter your year (1-5): "))
                if 1 <= year <= 5:
                    break
                print("Enter a year from 1 to 5.")
            except ValueError:
                print("Enter a whole number.")

        while True:
            time_slot = input(
                "Enter your desired time slot "
                "(Morning/Afternoon/Evening/Night): "
            ).strip().title()

            if time_slot in ("Morning", "Afternoon", "Evening", "Night"):
                break
            print("Enter Morning, Afternoon, Evening, or Night.")

        while True:
            destination = input(
                "Enter your desired destination (Delhi/Jaipur): "
            ).strip().title()

            if destination in ("Delhi", "Jaipur"):
                break
            print("Enter Delhi or Jaipur.")

        request = RideRequest(name, destination, time_slot, year)
        add_request(waiting_requests, request)
        print("Your request has been added to the waiting list.")

    elif user_req == 2:  # See other students and cabs waiting
        print("*Students*")
        students_waiting = False

        for queue in waiting_requests.values():
            ordered_queue = sorted(queue)

            for entry in ordered_queue:
                travelling_student_name = entry[2]
                students_waiting = True

                print(
                    f"{travelling_student_name.student_name}, "
                    f"{travelling_student_name.destination}, "
                    f"{travelling_student_name.time_slot}, "
                    f"Year {travelling_student_name.year}"
                )

        if not students_waiting:
            print("No students are waiting.")

        print("*Cab Drivers*")

        for cab_driver_name in cabs:
            if cab_driver_name.has_left:
                status = "Departed"
            else:
                status = "Available"

            print(
                f"{cab_driver_name.driver_name}, "
                f"{cab_driver_name.destination}, "
                f"{cab_driver_name.time_slot}, "
                f"Capacity: {cab_driver_name.capacity}, "
                f"Status: {status}"
            )

            if cab_driver_name.has_left:
                passenger_names = []

                for student in cab_driver_name.passengers:
                    passenger_names.append(student.student_name)

                print(f"Passengers: {', '.join(passenger_names)}")

    elif user_req == 3:  # Find Matches
        matches = find_matches(cabs, waiting_requests)
        selected_students = []

        if not matches:
            print("No available cabs.")

        for cab, students in matches.items():
            show_student_matches = []

            for student in students:
                show_student_matches.append(student.student_name)
                selected_students.append(student)

            print(f"{cab.driver_name} --> {show_student_matches}")

        # Waitlisted people

        print("*People with no seat*")
        people_with_no_seat = False

        for queue in waiting_requests.values():
            for entry in sorted(queue):
                student = entry[2]

                if student not in selected_students:
                    people_with_no_seat = True

                    print(
                        f"{student.student_name}, "
                        f"{student.destination}, {student.time_slot}"
                    )

        if not people_with_no_seat:
            print("None.")

    elif user_req == 4:  # Dispatch a cab
        while True:
            destination = input(
                "Enter your destination (Delhi/Jaipur): "
            ).strip().title()

            if destination in ("Delhi", "Jaipur"):
                break
            print("Enter Delhi or Jaipur.")

        while True:
            time_slot = input(
                "Enter your desired time_slot "
                "(Morning/Afternoon/Evening/Night): "
            ).strip().title()

            if time_slot in ("Morning", "Afternoon", "Evening", "Night"):
                break
            print("Enter Morning, Afternoon, Evening, or Night.")

        chosen_cab = None

        for cab in cabs:
            if (
                not cab.has_left
                and cab.destination == destination
                and cab.time_slot == time_slot
            ):
                chosen_cab = cab
                break

        if chosen_cab is None:
            print("No open cab is available for this trip.")
            continue

        trip = (chosen_cab.destination, chosen_cab.time_slot)
        queue = waiting_requests[trip]

        if not queue:
            print("No students are waiting for this trip.")
            continue

        passenger_names = []

        while queue and len(chosen_cab.passengers) < chosen_cab.capacity:
            entry = heapq.heappop(queue)
            student = entry[2]

            chosen_cab.passengers.append(student)
            passenger_names.append(student.student_name)

        chosen_cab.has_left = True

        print(
            f"{chosen_cab.driver_name} departed with "
            f"{', '.join(passenger_names)}."
        )

    elif user_req == 5:
        break

    else:
        print("Choose an option from 1 to 5.")


# for travelling_student_name in waiting_requests:
#     print(travelling_student_name.student_name, travelling_student_name.submission_time)