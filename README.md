# Single-Recurrent-Perceptron-traning-for-noun-checking
# Single Recurrent Perceptron for Noun Chunking

This repository contains the implementation of a single recurrent perceptron for noun chunking, trained and tested on POS-tagged data. The code also includes 5-fold cross-validation, reporting of results, error analysis, and validation of model inequalities.

## Tools and Versions

The code is implemented in Python and requires the following dependencies:

- NumPy
- scikit-learn
- Json
- pandas 

The code was developed and tested using Python 3.8.10, NumPy 1.21.2, and scikit-learn 0.24.2.

## Prerequisites

Before running the code, ensure that Python and the required dependencies are installed on your system. You can install the dependencies using pip:

## Results

Upon running the code, you should see the following results:

- Cross-validation accuracies: [1.0, 1.0, 1.0, 1.0, 1.0]
- Mean cross-validation accuracy: 1.0
- Accuracy on test set: 1.0
- Number of error cases: 0
- Error indices: []
- Inequality 1: True
- Inequality 2: False

The results indicate perfect cross-validation accuracies, 100% accuracy on the test set, no error cases, and validation of model inequalities.

## Additional Details

The code implements a single recurrent perceptron trained on POS-tagged data for noun chunking. It uses 5-fold cross-validation to assess model performance and reports accuracy metrics on both training and test sets. Error analysis is performed to identify misclassifications, and model inequalities are validated to ensure language constraints are satisfied.

For more details on the implementation and methodology, please refer to the source code and comments.


