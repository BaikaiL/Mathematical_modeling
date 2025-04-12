# ============================================================
# Implement your effective and efficient algorithm !!
# This is the only file you need to modify !!

# Input:
#  coords: the map coordinates read from data file (you should not modify)

# Output:
#  path: a list of integers such that [p1 p2 ... pn p1]
#        in which  p1 is always 0 as the starting point
#        also path ends at p1

# Notes:
#   make sure the output length is n+1, in which n is number of nodes
#   make sure your solution is a valid TSP solution

# Warnings:
#   any invalid solution (incorrect length, not return to starting point)
#   will fail the test
# ============================================================
from tools import city_distance
import numpy as np
import random

random.seed(42)
np.random.seed(42)

def fitness_function(path, distance_matrix):
    """
    Fitness parameter, which calculates the total distance of the path.

    path: a list of integers such that [p1 p2 ... pn p1]
    distance_matrix: a 2D numpy array of distances between cities
    return: the inverse of the total distance of the path
    """
    N = len(path)
    cur_dist = 0
    for i in range(N - 1):
        cur_dist += distance_matrix[path[i], path[i + 1]]
    return 1 / cur_dist


def initialize_population(num_nodes, population_size):
    """
    Initialize the population of paths.

    num_nodes: number of cities
    population_size: number of paths in the population
    return: a list of paths, each path is a list of integers
    """
    population = []
    for _ in range(population_size):
        path = list(range(1, num_nodes))
        np.random.shuffle(path)
        path = [0] + path + [0]
        population.append(path)
    return population


# Roulette Wheel Selection
def select_parents(population, fitness_scores):
    total_scores = sum(fitness_scores)
    probabilities = [score / total_scores for score in fitness_scores]
    # Select a parent based on the fitness scores
    selected_index = random.choices(range(len(population)), weights=probabilities, k=1)[0]
    return population[selected_index]

# Depending on the size of the problem, select the PMX
def crossover(parent1, parent2):
    # Extract the middle part
    p1 = parent1[1:-1]
    p2 = parent2[1:-1]
    size = len(p1)

    # Randomly select the start and end points for crossover
    start,end = sorted(random.sample(range(size), 2))


    # Generate the middle part of child1
    child1_mid = [-1] * size
    child1_mid[start:end + 1] = p2[start:end + 1]
    # Establish a mapping: elements in the crossover region of p2 -> elements in the crossover region of p1
    mapping = {p2[i]: p1[i] for i in range(start, end + 1)}
    # Handle non-crossover regions
    for i in list(range(0, start)) + list(range(end + 1, size)):
        current_val = p1[i]
        # If the current value is in the crossover region of child1, replace it using the mapping
        while current_val in child1_mid[start:end + 1]:
            current_val = mapping[current_val]
        child1_mid[i] = current_val

    # Generate the middle part of child2, which is the same as child1
    child2_mid = [-1] * size
    child2_mid[start:end + 1] = p1[start:end + 1]
    mapping2 = {p1[i]: p2[i] for i in range(start, end + 1)}
    for i in list(range(0, start)) + list(range(end + 1, size)):
        current_val = p2[i]
        while current_val in child2_mid[start:end + 1]:
            current_val = mapping2[current_val]
        child2_mid[i] = current_val

    # Construct the complete path by adding 0 at the beginning and end
    child1 = [0] + child1_mid + [0]
    child2 = [0] + child2_mid + [0]

    return child1, child2



# Select RSM, generate two points, and reverse the path between them.
def mutate(individual):
    mutated_individual = individual.copy()

    # Generate two random points
    start, end = sorted(random.sample(range(1, len(mutated_individual) - 1), 2))

    # Reverse the segment between the two points
    mutated_individual[start:end + 1] = reversed(mutated_individual[start:end + 1])

    return mutated_individual


def GA(num_nodes, distance_matrix, num_generations=100, population_size=50, crossover_rate=1, mutation_rate=0.1):
    """
    Implementation of genetic algorithm

    num_nodes: number of cities
    distance_matrix: a 2D numpy array of distances between cities
    num_generations: number of generations for the genetic algorithm
    population_size: number of paths in the population
    crossover_rate: probability of crossover for each pair of paths
    mutation_rate: probability of mutation for each path

    return: the best path found by the genetic algorithm
    """

    # Initialize population
    population = initialize_population(num_nodes, population_size)

    # Start iterating
    for _ in range(num_generations):
        # Calculate the total fitness function for all paths in the population
        fitness_scores = [fitness_function(i, distance_matrix) for i in population]
        new_population = []

        # If a cross occurs, the parent is picked
        # and the child is generated according to the crossing rules
        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores), select_parents(population, fitness_scores)

            if random.random() < crossover_rate:
                # Perform crossover
                child1, child2 = crossover(parent1, parent2)
                new_population.append(child1)
                new_population.append(child2)
            else:
                new_population.append(parent1)
                new_population.append(parent2)

        # In the event of a mutation, the offspring are updated according to the mutation rules
        for i in range(len(new_population)):
            if random.random() < mutation_rate:
                new_population[i] = mutate(new_population[i])
        # Update the population
        population = new_population
    # return the best path found by the genetic algorithm
    best_path = max(population, key=lambda path: fitness_function(path, distance_matrix))
    return best_path


def my_wonderful_function(coords):
    num_nodes = len(coords)
    distance_matrix = city_distance(coords)

    # Run the genetic algorithm
    path = GA(num_nodes, distance_matrix)
    # make sure it's valid output, since starting and ending at 0
    assert path[0] == path[-1] == 0
    assert len(path) == num_nodes + 1
    assert len(set(path)) == num_nodes

    return path