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


def find_matches(cabs, waiting_requests):
    ordered_requests = sorted(
        waiting_requests,
        key=lambda request: request.year,
        reverse=True
    )

    selected_students = []
    matches_by_cab = {}

    for cab in cabs:
        if cab.has_left:
            continue

        cab_matches = []

        for student in ordered_requests:
            if student in selected_students:
                continue

            if (
                student.destination == cab.destination
                and student.time_slot == cab.time_slot
                and len(cab_matches) < cab.capacity
            ):
                selected_students.append(student)
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

waiting_requests = [
    aditi, vikram, meera, riya,
    arjun, neha, kabir, isha,
    rohan, sana, dev, tara,
    aman, priya, zoya, om
]


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
            time_slot = input("Enter your desired time slot ""(Morning/Afternoon/Evening/Night): ").strip().title()

            if time_slot in ("Morning", "Afternoon", "Evening", "Night"):
                break
            print("Enter Morning, Afternoon, Evening, or Night.")

        while True:
            destination = input("Enter your desired destination (Delhi/Jaipur): ").strip().title()

            if destination in ("Delhi", "Jaipur"):
                break
            print("Enter Delhi or Jaipur.")

        request = RideRequest(name, destination, time_slot, year)
        waiting_requests.append(request)
        print("Your request has been added to the waiting list.")

    elif user_req == 2:  # See other students and cabs waiting
        print("*Students*")
        for travelling_student_name in waiting_requests:
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

        for student in waiting_requests:
            if student not in selected_students:
                print(
                    f"{student.student_name}, "
                    f"{student.destination}, {student.time_slot}"
                )

    elif user_req == 4:  # Dispatch a cab
        destination = input("Enter your destination: ")
        time_slot = input("Enter your desired time_slot: ")

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

        matches = find_matches([chosen_cab], waiting_requests)
        passengers = matches[chosen_cab]

        if not passengers:
            print("No Students on the cab")
            continue

        passenger_names = []

        for student in passengers:
            chosen_cab.passengers.append(student)
            waiting_requests.remove(student)
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