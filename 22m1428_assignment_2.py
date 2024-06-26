# -*- coding: utf-8 -*-
"""Untitled43.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1onw4iu3yacKz_wfwNyLq6VuDOQYjmOH_
"""

import numpy as np
import json
from sklearn.model_selection import KFold

def preprocess_data(data):
    train_pos_tags = []
    train_chunk_tags = []
    train_tokens = []
    for example in data:
        tokens = example["tokens"]
        pos_tags = example["pos_tags"]
        chunk_tags = example["chunk_tags"]
        encoded_pos = pos_tags
        train_tokens.append(tokens)
        train_pos_tags.append(pos_tags)
        train_chunk_tags.append(chunk_tags)
    return train_tokens, train_pos_tags, train_chunk_tags

# Function to load data from JSON file
def load_data(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    tokens = data['tokens']
    pos_tags = data['pos_tags']
    chunk_tags = data['chunk_tags']
    return tokens, pos_tags, chunk_tags

# Activation function (sigmoid)
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Derivative of sigmoid
def sigmoid_derivative(x):
    return x * (1 - x)

# Padding function for input data
def pad_input_data(data, max_length):
    padded_data = np.zeros((len(data), max_length))
    for i, seq in enumerate(data):
        padded_data[i, :len(seq)] = seq
    return padded_data
# Function to calculate accuracy
def calculate_accuracy(true_labels, predicted_labels):
    correct_predictions = np.sum(true_labels == predicted_labels)
    total_predictions = len(true_labels)
    accuracy = correct_predictions / total_predictions
    return accuracy

# Training function
def train_single_recurrent_perceptron(X, Y, weights_input_hidden, weights_hidden_output, learning_rate=0.01, epochs=100):
    for epoch in range(epochs):
        # Forward pass
        hidden_layer_input = np.dot(X, weights_input_hidden)
        hidden_layer_output = sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, weights_hidden_output)
        output = sigmoid(output_layer_input)
        Y_shape = (Y.shape[0], output_dim)

        # Reshape padded_train_chunk_tags to match the correct shape
        Y = Y[:, :output_dim].reshape(Y_shape)
        print(Y.shape)
        # Backpropagation through time
        output_error = Y - output
        output_delta = output_error * sigmoid_derivative(output)

        hidden_error = output_delta.dot(weights_hidden_output.T)
        hidden_delta = hidden_error * sigmoid_derivative(hidden_layer_output)

        # Update weights
        weights_hidden_output += hidden_layer_output.T.dot(output_delta) * learning_rate
        weights_input_hidden += X.T.dot(hidden_delta) * learning_rate

    return weights_input_hidden, weights_hidden_output



# Load data
# Load training data

with open('/content/train.jsonl', 'r') as train_file:
    train_data = [json.loads(line) for line in train_file]
# Determine maximum sequence length

train_tokens, train_pos_tags, train_chunk_tags = preprocess_data(train_data)

with open('/content/test.jsonl', 'r') as train_file:
    test_data = [json.loads(line) for line in train_file]
test_tokens, test_pos_tags, test_chunk_tags = preprocess_data(test_data)

# Determine maximum sequence length
max_seq_length = max(len(seq) for seq in train_pos_tags)

# Padding input data
padded_train_pos_tags = pad_input_data(train_pos_tags, max_seq_length)
padded_train_chunk_tags = pad_input_data(train_chunk_tags, max_seq_length)

# Initialize parameters
np.random.seed(42)
input_dim = 4  # Number of POS tags
hidden_dim = 5  # Dimension of hidden layer
output_dim = 2  # Binary output for chunking
learning_rate = 0.01
epochs = 100


# Initialize weights
weights_input_hidden = np.random.rand(padded_train_pos_tags.shape[1], hidden_dim)
weights_hidden_output = np.random.rand(hidden_dim, output_dim)

# Perform 5-fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)
fold_accuracies = []

for train_index, val_index in kf.split(padded_train_pos_tags):
    X_train_fold, X_val_fold = padded_train_pos_tags[train_index], padded_train_pos_tags[val_index]
    Y_train_fold, Y_val_fold = padded_train_chunk_tags[train_index], padded_train_chunk_tags[val_index]
    print(X_train_fold.shape)
    print(Y_train_fold.shape)
    # Train the single recurrent perceptron
    weights_input_hidden_trained, weights_hidden_output_trained = train_single_recurrent_perceptron(
        X_train_fold, Y_train_fold, weights_input_hidden, weights_hidden_output, learning_rate, epochs)

    # Validate on validation set
    hidden_layer_input_val = np.dot(X_val_fold, weights_input_hidden_trained)
    hidden_layer_output_val = sigmoid(hidden_layer_input_val)
    output_layer_input_val = np.dot(hidden_layer_output_val, weights_hidden_output_trained)
    output_val = sigmoid(output_layer_input_val)

    # Predicted chunk tags
    predicted_chunk_tags_val = np.argmax(output_val, axis=1)

    # Calculate accuracy for the fold
    accuracy_fold = calculate_accuracy(np.argmax(Y_val_fold, axis=1), predicted_chunk_tags_val)
    fold_accuracies.append(accuracy_fold)

# Report cross-validation results

print("Cross-validation accuracies:", fold_accuracies)
print("Mean cross-validation accuracy:", np.mean(fold_accuracies))

# Train the single recurrent perceptron on full training data
weights_input_hidden_trained, weights_hidden_output_trained = train_single_recurrent_perceptron(
    padded_train_pos_tags, padded_train_chunk_tags, weights_input_hidden, weights_hidden_output, learning_rate, epochs)

max_seq_length = max(len(seq) for seq in train_pos_tags)

# Padding function for input data
def pad_input_data(data, max_length):
    padded_data = np.zeros((len(data), max_length))
    for i, seq in enumerate(data):
        padded_data[i, :min(len(seq), max_length)] = seq[:max_length]  # Adjusted to use min(len(seq), max_length)
    return padded_data

# Test on test set
# hidden_layer_input_test = np.dot(pad_input_data(test_pos_tags, max_seq_length), weights_input_hidden_trained)
# hidden_layer_output_test = sigmoid(hidden_layer_input_test)
# output_layer_input_test = np.dot(hidden_layer_output_test, weights_hidden_output_trained)
# output_test = sigmoid(output_layer_input_test)
# predicted_chunk_tags_test = np.argmax(output_test, axis=1)


# Pad test data to match maximum sequence length
padded_test_pos_tags = pad_input_data(test_pos_tags, max_seq_length)
print(padded_test_pos_tags.shape)
print(weights_input_hidden_trained.shape)
# Test on test set
hidden_layer_input_test = np.dot(padded_test_pos_tags, weights_input_hidden_trained)
hidden_layer_output_test = sigmoid(hidden_layer_input_test)
output_layer_input_test = np.dot(hidden_layer_output_test, weights_hidden_output_trained)
output_test = sigmoid(output_layer_input_test)
predicted_chunk_tags_test = np.argmax(output_test, axis=1)

weights_input_hidden_trained_transposed = weights_input_hidden_trained.T

weights_input_hidden_trained_transposed.shape

# Calculate accuracy on test set
accuracy_test = calculate_accuracy(np.argmax(pad_input_data(test_chunk_tags, max_seq_length), axis=1), predicted_chunk_tags_test)
print("Accuracy on test set:", accuracy_test)

# Error cases and analysis
error_indices = np.where(predicted_chunk_tags_test != np.argmax(pad_input_data(test_chunk_tags, max_seq_length), axis=1))[0]
print("Number of error cases:", len(error_indices))
print("Error indices:", error_indices)

# Report model weights
print("Model weights - Input to Hidden layer:")
print(weights_input_hidden_trained)
print("Model weights - Hidden to Output layer:")
print(weights_hidden_output_trained)

# Validate inequalities for model weights
inequality1 = np.sum(weights_input_hidden_trained[:, 1:]) > np.sum(weights_input_hidden_trained[:, 0])
inequality2 = np.sum(weights_hidden_output_trained[1:, :]) > np.sum(weights_hidden_output_trained[0, :])
print("Inequality 1:", inequality1)
print("Inequality 2:", inequality2)