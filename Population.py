from utils import *
import random
from sklearn.metrics import log_loss
from NeuralNetwork import NeuralNetwork


class Population:
    def __init__(self, pop_size, x, y, session_length, output_labels, best_nn=None):
        self.pop_size = pop_size
        self.train, self.validation = get_train_and_valid(x, y)

        print("Train dataset length {0}, validation dataset length {1} ".format(len(self.train), len(self.validation)))
        print("Train labels distribution " + str(get_labels_count(self.train)))
        print("Validation labels distribution " + str(get_labels_count(self.validation)))

        self.session_length = session_length
        self.output_labels = output_labels

        self.population = {}

        if best_nn:
            for i in range(self.pop_size):
                self.population[best_nn.mutate()] = [0, 0]
        else:
            for i in range(self.pop_size):
                self.population[NeuralNetwork()] = [0, 0]

    def create_new_population(self):
        best_nn = self.get_best_nn()()
        self.population = {}
        for i in range(self.pop_size):
            self.population[best_nn.mutate()] = [0, 0]

    def get_best_nn(self):
        min_loss = 100
        best_nn = None
        for i in self.population:
            if self.population[i][1] < min_loss:
                min_loss = self.population[i][1]
                best_nn = i
        return best_nn

    def get_max_score(self):
        return self.population[self.get_best_nn()][0]

    def get_min_loss(self):
        return self.population[self.get_best_nn()][1]

    def validate(self):
        valid_acc = 0
        valid_loss = 0
        best_nn = self.get_best_nn()
        for i in self.validation:
            img, label = i
            prediction = best_nn.predict(img)
            if self.output_labels[prediction.argmax()] == label:
                valid_acc += 1 / len(self.validation)
            y = np.zeros((len(self.output_labels), 1))
            y[self.output_labels.index(label)] = 1
            valid_loss += log_loss(y, prediction) / len(self.validation)
        return valid_acc, valid_loss

    def session_for_dinos(self):
        for i in range(self.session_length):
            img, label = random.choice(self.train)
            for nn in self.population:
                prediction = nn.predict(img)
                if self.output_labels[prediction.argmax()] == label:
                    self.population[nn][0] += 1/self.session_length
                y = np.zeros((len(self.output_labels), 1))
                y[self.output_labels.index(label)] = 1
                self.population[nn][1] += log_loss(y, prediction)/self.session_length
