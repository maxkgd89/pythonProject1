import time
import random
import math
import sys

# set a list of 6 people from diff. cities
people = [('Lisbon', 'LIS'),
          ('Madrid', 'MAD'),
          ('Paris', 'CDG'),
          ('Dublin', 'DUB'),
          ('Brussels', 'BRU'),
          ('London', 'LHR')]

#parce a dictionary from flights.txt
flights = {} 
for line in open('flights.txt'):
    origin, destiny, departure, arrival, price = line.split(',')
    flights.setdefault((origin, destiny), [])
    flights[(origin, destiny)].append((departure, arrival, int(price)))

# for key, value in flights.items():
# print(key, value)

# if put there ARRAY then can get a PRINT DASHBOARD of all pass and flights
def print_schedule(schedule):
    flight_id = -1
    total_price = 0
    for i in range(len(schedule) // 2):
        name = people[i][0]
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][schedule[flight_id]]
        total_price += going[2]
        flight_id += 1
        returning = flights[(destiny, origin)][schedule[flight_id]]
        total_price += returning[2]
        print('%10s%10s %5s-%5s U$%3s %5s-%5s U$%3s' % (name, origin, going[0],
                                                        going[1], going[2],
                                                        returning[0], returning[1], returning[2]))
    print('Total price: ', total_price)

def get_minutes(hour):
    t = time.strptime(hour, '%H:%M')
    minutes = t[3] * 60 + t[4]
    return minutes

# pass here N schedules and fun calculates COSTs, Waiting Time
def fitness_function(solution):
    total_price = 0
    last_arrival = 0
    first_departure = 1439

    flight_id = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][solution[flight_id]]
        flight_id += 1
        returning = flights[(destiny, origin)][solution[flight_id]]

        total_price += going[2]
        total_price += returning[2]

        if last_arrival < get_minutes(going[1]):
            last_arrival = get_minutes(going[1])
        if first_departure > get_minutes(returning[0]):
            first_departure = get_minutes(returning[0])

    total_wait = 0
    flight_id = -1
    for i in range(len(solution) // 2):
        origin = people[i][1]
        flight_id += 1
        going = flights[(origin, destiny)][solution[flight_id]]
        flight_id += 1
        returning = flights[(destiny, origin)][solution[flight_id]]

        total_wait += last_arrival - get_minutes(going[1])
        total_wait += get_minutes(returning[0]) - first_departure

    # 3PM - 10AM
    # 11AM - 3PM
    if last_arrival > first_departure:
        total_price += 50

    return total_price + total_wait

# just random generateor of how many people and flights for search
domain = [(0,9)] * (len(people) * 2)
[random.randint(0,9) for i in range(len(domain))]

# puts DOMAIN and itterates 1K times using each time FITNESS FUNCTION
def random_search(domain, fitness_function):
  best_cost = sys.maxsize
  for i in range(1000):
    solution = [random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
    cost = fitness_function(solution)
    if cost < best_cost:
      best_cost = cost
      best_solution = solution
  return best_solution

random_solution = random_search(domain, fitness_function)

fitness_function(random_solution)

print_schedule(random_solution)
