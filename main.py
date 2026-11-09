from datetime import datetime
import heapq


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


# TEST OBJECTS

cab1 = Cab("Raj", 2, "Delhi", "Morning")
cab2 = Cab("Ram", 4, "Jaipur", "Morning")
cab3 = Cab("Amit", 1, "Delhi", "Morning")
cab4 = Cab("Sunil", 2, "Delhi", "Evening")
cab5 = Cab("Mohan", 1, "Jaipur", "Evening")
cab6 = Cab("Rakesh", 3, "Jaipur", "Morning")

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

cabs = [cab1, cab2, cab3, cab4, cab5, cab6]

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
    user_req = int(input('''
    CAB POOL MATCHER

    1. Add a ride request
    2. Show waiting students and cabs
    3. Find matches
    4. Dispatch a cab
    5. Quit

    Choose an option: '''))

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

        for queue in waiting_requests.values():
            for entry in queue:
                travelling_student_name = entry[2]

                if travelling_student_name.destination == "Delhi":
                    print(f"{travelling_student_name.student_name}, Delhi")

                elif travelling_student_name.destination == "Jaipur":
                    print(f"{travelling_student_name.student_name}, Jaipur")

        print("*Cab Drivers*")
        for cab_driver_name in cabs:
            print(cab_driver_name.driver_name)

    elif user_req == 3:  # Find Matches
        matches = find_matches(cabs, waiting_requests)
        selected_students = []

        for cab, students in matches.items():
            show_student_matches = []

            for student in students:
                show_student_matches.append(student.student_name)
                selected_students.append(student)

            print(f"{cab.driver_name} --> {show_student_matches}")

        # Waitlisted people

        print("*People with no seat*")

        for queue in waiting_requests.values():
            for entry in queue:
                student = entry[2]

                if student not in selected_students:
                    print(
                        f"{student.student_name}, "
                        f"{student.destination}, {student.time_slot}"
                    )

    elif user_req == 4:  # Dispatch a cab
        destination = input("Enter your destination: ").strip().title()
        time_slot = input("Enter your desired time_slot: ").strip().title()

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


# for travelling_student_name in waiting_requests:
#     print(travelling_student_name.student_name, travelling_student_name.submission_time)