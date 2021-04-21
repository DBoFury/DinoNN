import tensorflow as tf
from utils import *


class NeuralNetwork:
    def __init__(self, input_nodes=get_input_nodes(), hidden_nodes=HIDDEN_NODES,
                 output_nodes=OUTPUT_NODES, num_kernels=NUM_KERNELS, mutation_rate_dense=MUTATION_RATE[0],
                 mutation_rate_conv=MUTATION_RATE[1], path=None):

        self.input_nodes = input_nodes
        self.hidden_nodes = hidden_nodes
        self.output_nodes = output_nodes
        self.num_kernels = num_kernels
        self.mutation_rate_dense = mutation_rate_dense
        self.mutation_rate_conv = mutation_rate_conv
        self.kernels = []

        if path:
            self.load_weights(path)
        else:
            self.kernels = [tf.convert_to_tensor(np.random.normal(0, 0.1, (3, 3, y, y * 4)), dtype=tf.float32)
                            if y < 2 else tf.convert_to_tensor(np.random.normal(0, 0.1, (3, 3, y, y * 2)),
                                                               dtype=tf.float32)
                            for y in [1 if x < 2 else 2 ** x for x in range(1, self.num_kernels + 1)]]
            self.i_h_layer = tf.convert_to_tensor(np.random.normal(0.0, pow(self.hidden_nodes, -0.5),
                                                                   (self.hidden_nodes, self.input_nodes)),
                                                  dtype=tf.float32)
            self.h_o_layer = tf.convert_to_tensor(np.random.normal(0.0, pow(self.hidden_nodes, -0.5),
                                                                   (self.output_nodes, self.hidden_nodes)),
                                                  dtype=tf.float32)

        self.activation_func = lambda x: 1 / (1 + np.exp(-x))

    def predict(self, x):
        for kernel in self.kernels:
            x = tf.nn.conv2d(x, kernel, strides=[1, 1, 1, 1], padding='VALID')
            x = tf.nn.max_pool2d(x, (2, 2), strides=[1, 2, 2, 1], padding='VALID')
            x = tf.nn.relu(x)
        x = tf.reshape(x, (-1, 1))

        i_h_output = np.dot(self.i_h_layer, x)
        i_h_output_act = self.activation_func(i_h_output)

        h_o_output = np.dot(self.h_o_layer, i_h_output_act)
        h_o_output_act = self.activation_func(h_o_output)

        return h_o_output_act

    def copy(self):
        nn = NeuralNetwork(mutation_rate_dense=self.mutation_rate_dense, mutation_rate_conv=self.mutation_rate_conv)
        nn.kernels = []
        for kernel in self.kernels:
            nn.kernels.append(kernel)
        nn.i_h_layer = np.copy(self.i_h_layer)
        nn.h_o_layer = np.copy(self.h_o_layer)
        return nn

    def save_weights(self, path=NN_PATH):
        for i, kernel in enumerate(self.kernels):
            np.save(path + f'kernel_{i + 1}.npy', kernel)
        np.save(path + 'i_h_layer.npy', self.i_h_layer)
        np.save(path + 'h_o_layer.npy', self.h_o_layer)

    def load_weights(self, path=NN_PATH):
        for i in range(1, self.num_kernels + 1):
            self.kernels.append(np.load(path + f'kernel_{i}.npy'))
        self.i_h_layer = np.load(path + 'i_h_layer.npy')
        self.h_o_layer = np.load(path + 'h_o_layer.npy')

    def mutate(self):
        child = self.copy()
        for i, _ in enumerate(child.kernels):
            child.kernels[i] += tf.convert_to_tensor(np.random.normal(0.0, child.mutation_rate_conv,
                                                                      child.kernels[i].shape), dtype=tf.float32)
        child.i_h_layer += tf.convert_to_tensor(np.random.normal(0.0, child.mutation_rate_dense,
                                                                 (child.hidden_nodes, child.input_nodes)),
                                                dtype=tf.float32)
        child.h_o_layer += tf.convert_to_tensor(np.random.normal(0.0, child.mutation_rate_dense,
                                                                 (child.output_nodes, child.hidden_nodes)),
                                                dtype=tf.float32)
        return child
