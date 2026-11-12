# Cab Pool Matcher

A Python terminal menu for managing student cab requests to Delhi and Jaipur.
Students join a waiting queue for their destination and time slot. 
When a cab leaves, higher-year students get seats first.

The app is run by one operator. There are no logins or separate admin and student modes.

## Running the app

Python 3 is required. Everything used is from the standard library, so there are no extra packages to install.
Keep `main.py` and `cabs.json` in the same folder, then run:

```bash
python main.py
```

The app starts with empty waiting queues. Use the menu to add requests, view students and cabs, preview matches,
dispatch a cab, or quit.

## Cab file

The program loads cabs from `cabs.json`. For example:

```json
[
    {
        "driver_name": "Raj",
        "capacity": 2,
        "destination": "Delhi",
        "time_slot": "Morning"
    },
    {
        "driver_name": "Ram",
        "capacity": 4,
        "destination": "Jaipur",
        "time_slot": "Morning"
    }
]
```

Each cab needs a driver name, capacity, destination, and time slot.

- Capacity must be an integer from 1 to 4.
- Destinations are Delhi and Jaipur.
- Time slots are Morning, Afternoon, Evening, and Night.
- Driver names cannot be empty.

Cabs are considered in the order they appear in the file.

JSON was a straightforward option for this data. `json.load()` reads it into a list of dictionaries, 
and each dictionary is used to create a `Cab` object. It also reads capacity as a number. 
CSV would have worked for these fields too.

If the cab file is missing or invalid, the program explains the problem and stops so the file can be corrected.

## How matching works

There is a separate priority queue for each destination and time slot, giving eight queues in total. 
These queues belong to trips, not individual cabs.

Each request is stored in its queue as:

```python
(-request.year, request.request_number, request)
```

`heapq` removes the smallest value first. Making the year negative puts fifth years ahead of fourth years, and so on.

The request number increases each time a request is created. When two years are equal, the smaller request number comes first. 
This also prevents Python from trying to compare the request objects themselves.

`submission_time` is recorded on each request, but the request number is what the queue uses to break ties.

### Previewing matches

Find Matches works on copies of the queues. It considers open cabs in file order
and takes suitable students from the copied queue up to each cab's capacity.

Removing a student from the copied queue prevents them from appearing in two cabs in the same preview. 
The real queues stay unchanged.

A preview does not reserve seats. If a senior submits a request afterward,
the next preview or dispatch will take that new priority into account.

### Dispatching

The operator enters a destination and time slot. The program finds the first open cab for that trip,
removes students from the actual priority queue, adds them to the cab's passenger list, and marks the cab as departed.

If there is no open cab or nobody is waiting for that trip, it prints a message and leaves the data unchanged.

## Tricky situations

### 1. A cab leaves partly empty

A cab does not have to be full to leave. If it has four seats and only two students are waiting, 
both students are added and it departs with two passengers.

Once it has departed, the remaining seats cannot be filled later. Matching and dispatch both skip departed cabs.

### 2. No cabs are left

New requests can still join their trip's waiting queue even when all its cabs have departed.

Trying to dispatch that trip prints a message saying no open cab is available. The requests stay in the queue. 
They still appear in the waiting-student display and under “People with no seat” when finding matches.

The program does not remove a request just because a cab is unavailable.
This also applies if every cab in the system has departed.

### 3. Two students are in the same year

The earlier request has the smaller request number, so it is removed from the heap first.

For example, two third-year requests might have these priorities:

```python
(-3, 7)
(-3, 8)
```

The years are equal, so Python compares the request numbers. Request 7 gets priority over request 8.

### 4. Handling 1,000 requests

Let `n` be the total number of waiting requests and `c` the number of cabs. The bounds below use `n`, although an individual heap only contains requests for one trip.

## Time Complexities and Reason

1) Add one request :- O(log n) as `heappush()` may move the new entry up the heap. 
2) Add n requests to empty queues :- O(n log n) as the program inserts requests one at a time using `heappush()`. 
3) Find an open cab for a trip :- O(c) as the program checks the cab list until it finds a match or reaches the end.
4) Remove up to four students from a queue :- O(log n) as there are at most four heap removals, each taking O(log n). 
5) Dispatch, including finding the cab :- O(c + log n) as this combines the cab search with at most four heap removals. 

For 1,000 requests, the insertion approach therefore has an O(n log n) upper bound with n = 1,000. 
Requests split across different trip queues can involve smaller heaps.

The cab search is a simple loop because the task only has a few cabs.
It would be possible to index open cabs by trip if the number of cabs became much larger.

## Checks performed

The core code was checked for:

- Higher-year priority and arrival order for equal years.
- Capacity limits and avoiding duplicate matches.
- Repeated previews without changing the actual queues.
- Removing passengers from waiting queues after dispatch.
- Skipping departed cabs.
- Partly filled cabs and trips with no waiting students.
- Invalid menu input, years, destinations, and time slots.
- Missing or invalid cab JSON.

## Limitations

Saving and restoring state has not been implemented.
Quitting loses the current requests and dispatch records.
Restarting loads the cabs again with empty waiting queues.

The app also treats each submitted request separately. It does not check whether the same person has already submitted another request.
