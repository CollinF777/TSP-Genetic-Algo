import random
import time

# Define cities and distances

cities = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L"]

# distance matrix
distances = {
    "A": {
        "A": 0, "B": 91, "C": 37, "D": 84, "E": 62, "F": 113,
        "G": 49, "H": 76, "I": 105, "J": 68, "K": 57, "L": 99
    },
    "B": {
        "A": 91, "B": 0, "C": 72, "D": 45, "E": 88, "F": 63,
        "G": 104, "H": 51, "I": 116, "J": 79, "K": 34, "L": 97
    },
    "C": {
        "A": 37, "B": 72, "C": 0, "D": 59, "E": 41, "F": 96,
        "G": 28, "H": 68, "I": 83, "J": 52, "K": 76, "L": 61
    },
    "D": {
        "A": 84, "B": 45, "C": 59, "D": 0, "E": 73, "F": 48,
        "G": 81, "H": 36, "I": 92, "J": 64, "K": 57, "L": 85
    },
    "E": {
        "A": 62, "B": 88, "C": 41, "D": 73, "E": 0, "F": 67,
        "G": 53, "H": 79, "I": 46, "J": 91, "K": 69, "L": 38
    },
    "F": {
        "A": 113, "B": 63, "C": 96, "D": 48, "E": 67, "F": 0,
        "G": 109, "H": 42, "I": 77, "J": 31, "K": 54, "L": 82
    },
    "G": {
        "A": 49, "B": 104, "C": 28, "D": 81, "E": 53, "F": 109,
        "G": 0, "H": 74, "I": 61, "J": 84, "K": 95, "L": 47
    },
    "H": {
        "A": 76, "B": 51, "C": 68, "D": 36, "E": 79, "F": 42,
        "G": 74, "H": 0, "I": 55, "J": 39, "K": 44, "L": 91
    },
    "I": {
        "A": 105, "B": 116, "C": 83, "D": 92, "E": 46, "F": 77,
        "G": 61, "H": 55, "I": 0, "J": 68, "K": 102, "L": 29
    },
    "J": {
        "A": 68, "B": 79, "C": 52, "D": 64, "E": 91, "F": 31,
        "G": 84, "H": 39, "I": 68, "J": 0, "K": 47, "L": 106
    },
    "K": {
        "A": 57, "B": 34, "C": 76, "D": 57, "E": 69, "F": 54,
        "G": 95, "H": 44, "I": 102, "J": 47, "K": 0, "L": 73
    },
    "L": {
        "A": 99, "B": 97, "C": 61, "D": 85, "E": 38, "F": 82,
        "G": 47, "H": 91, "I": 29, "J": 106, "K": 73, "L": 0
    }
}

# Calculate total route distance
def route_distance(route):
    total_distance = 0

    for i in range(len(route)):
        current_city = route[i]

        # The % is for the last city to connect back to as otherwise we'd go out of bounds
        next_city = route[(i + 1) % len(route)]

        total_distance += distances[current_city][next_city]

    return total_distance

# Fitness eval
def fitness(route):
    # 1 / a number gives a shorter route a larger fitness score aka better fitness
    return 1 / route_distance(route)

# Population initialization
# Create a random route
def create_route():
    route = cities.copy()
    random.shuffle(route)
    return route

def create_population(pop_size):
    population = []
    for i in range(pop_size):
        population.append(create_route())

    return population

# Parent selection
def select_parent(population):
    # Choose two routes at random
    route1, route2 = random.sample(population, 2)

    # Select the route with the higher fitness
    if fitness(route1) > fitness(route2):
        return route1

    return route2

# Order crossover
def crossover(parent1, parent2):
    # Choose two random positions
    start, end = sorted(random.sample(range(len(parent1)), 2))

    # Start with an empty child
    child = [None] * len(parent1)

    # Copy a section from parent 1
    child[start:end] = parent1[start:end]

    # Go through Parent 2 and add cities that are not already in the child
    remaining_cities = [
        city for city in parent2
        if city not in child
    ]

    remaining_index = 0

    for i in range(len(child)):
        if child[i] is None:
            child[i] = remaining_cities[remaining_index]
            remaining_index += 1

    return child

# Swap mutation
def mutation(route, mutation_rate):
    #  Decide randomly if a mutation occurs
    if random.random() < mutation_rate:
        # Pick two random positions
        index1, index2 = random.sample(range(len(route)), 2)

        # Swap the two cities
        route[index1], route[index2] = route[index2], route[index1]

# Genetic algo
def genetic_algorithm(time_limit):
    population_size = 200
    mutation_rate = 0.02

    # Create the initial population
    population = create_population(population_size)

    # Find the best route in initial population
    best_route = min(population, key=route_distance)
    best_distance = route_distance(best_route)

    start_time = time.time()
    generation = 0

    # Each entry is (gen, elapsed sec, best dist) recorded only when best dist improves
    history = [(0, 0.0, best_distance)]
    print(f"Gen 0 (0.000s): initial best = {best_distance}")
    last_printed_generation = 0

    while time.time() - start_time < time_limit:
        new_population = []

        # Keep the best route from the previous generation
        new_population.append(best_route.copy())

        # Create the rest of the new population
        while len(new_population) < population_size:
            # Select two parents
            parent1 = select_parent(population)
            parent2 = select_parent(population)

            # Create a child using crossover
            child = crossover(parent1, parent2)

            # Potentially mutate child
            mutation(child, mutation_rate)

            # Add the new child to the new population
            new_population.append(child)

        # Replace old population
        population = new_population
        generation += 1

        # Find the best route in the new population
        current_best = min(population, key=route_distance)
        current_distance = route_distance(current_best)

        # Update the overall best route if we found a shorter route
        if current_distance < best_distance:
            best_route = current_best.copy()
            best_distance = current_distance
            elapsed = time.time() - start_time
            history.append((generation, elapsed, best_distance))
            print(f"Gen {generation} ({elapsed:.3f}s): new best = {best_distance}")
            last_printed_generation = generation

    # Print the final generation if it wasnt already printed
    if generation != last_printed_generation:
        elapsed = time.time() - start_time
        print(f"Gen {generation - 1} ({elapsed:.3f}s): Best distance = {best_distance}")

    # Calculate total time used
    elapsed_time = time.time() - start_time

    return best_route, best_distance, elapsed_time, generation, history

# Run the algo
time_limit = 20

best_route, best_distance, elapsed_time, generations, history = genetic_algorithm(time_limit)

# Display results
# Add the starting city to the end so that the printed route also shows return trip
display_route = best_route + [best_route[0]]

print()
print("------")
print("Genetic Algorithm Results")
print("------")

print("Best Route:")
print(" -> ".join(display_route))

print(f"Total Distance: {best_distance}")
print(f"Elapsed Time: {elapsed_time:.2f} seconds")
print(f"Generations completed: {generations}")

last_gen, last_time, _ = history[-1]
print(f"Last improvement: generation {last_gen} at {last_time:.3f}s")
print(f"Number of improvements: {len(history) - 1}")
