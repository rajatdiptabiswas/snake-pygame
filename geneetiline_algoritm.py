import random

class Individuaal:
    def __init__(self, sequence, mutation_rate):
        self.sequence = sequence
        self.mutation_rate = mutation_rate
        self.fitness = 0

    def mutate(self):
        for i in range(len(self.sequence)):
            if random.random() <= self.mutation_rate:
                self.sequence[i] = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def crossover(self, partner):
        # Create a new child individual
        child = Individuaal(self.sequence.copy(), self.mutation_rate)

        # Choose a random crossover point
        crossover_point = random.randint(0, len(self.sequence))

        # Swap genetic material between parents at the crossover point
        child.sequence[crossover_point:] = partner.sequence[crossover_point:]

        return child

    def evaluate_fitness(self, score):
        self.fitness = score  # Assign the score as the fitness value

    def __repr__(self):
        return f"Actions: {self.sequence}, Fitness: {self.fitness}"

    def get_next_move(self, current_direction):
        # Determine the valid moves based on the current direction
        if current_direction == 'UP' or current_direction == 'DOWN':
            valid_moves = ['LEFT', 'RIGHT']
        else:
            valid_moves = ['UP', 'DOWN']

        # Choose the next move from the valid moves
        next_move = random.choice(valid_moves)

        return next_move
