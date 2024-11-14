import pytest
import sys
import numpy as np
import pandas as pd

# Add current directory to sys.path to import shopping module
sys.path.insert(0, "")

import shopping as shopping

def test_load_data_lines():
    """Test that load_data returns the correct number of lines"""
    evidence, labels = shopping.load_data("shopping.csv")
    if isinstance(evidence, pd.core.frame.DataFrame):
        evidence = evidence.values.tolist()
    expected = 12330
    assert len(evidence) == expected, "load_data does not return the correct number of evidence"
    assert len(labels) == expected, "load_data does not return the correct number of labels"

def test_load_data_int():
    """Test that load_data handles integer values correctly"""
    evidence, labels = shopping.load_data("shopping.csv")
    if isinstance(evidence, pd.core.frame.DataFrame):
        evidence = evidence.values.tolist()
    
    tests = [
        (0, 0, 0),
        (2, 4, 1),
    ]
    for row, col, expected in tests:
        assert evidence[row][col] == expected, "load_data does not correctly handles integer values"

def test_load_data_float():
    """Test that load_data handles float values correctly"""
    evidence, labels = shopping.load_data("shopping.csv")
    if isinstance(evidence, pd.core.frame.DataFrame):
        evidence = evidence.values.tolist()
    
    tests = [
        (0, 6, 0.2),
        (3, 7, 0.14),
    ]
    for row, col, expected in tests:
        assert evidence[row][col] == expected, "load_data does not correctly handles float values"

def test_load_data_month():
    """Test that load_data handles month conversion correctly"""
    evidence, labels = shopping.load_data("shopping.csv")
    if isinstance(evidence, pd.core.frame.DataFrame):
        evidence = evidence.values.tolist()
    
    tests = [
        (0, 10, 1),
        (256, 10, 2),
    ]
    for row, col, expected in tests:
        assert evidence[row][col] == expected, "load_data does not correctly handles month conversion"

def test_load_data_visitor():
    """Test that load_data handles boolean values correctly"""
    evidence, labels = shopping.load_data("shopping.csv")
    if isinstance(evidence, pd.core.frame.DataFrame):
        evidence = evidence.values.tolist()
    
    tests = [
        (0, 15, 1),
        (93, 15, 0),
    ]
    for row, col, expected in tests:
        assert evidence[row][col] == expected, "load_data does not correctly handles boolean values"

def test_train_model():
    """Test that train_model returns a k-nearest-neighbor classifier"""
    evidence = [
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0.0, 0, 0.0, 2, 64.0, 0.0, 0.1, 0.0, 0.0, 1, 2, 2, 1, 2, 1, 0],
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 4, 1, 9, 3, 1, 0],
        [0, 0.0, 0, 0.0, 2, 2.666666667, 0.05, 0.14, 0.0, 0.0, 1, 3, 2, 2, 4, 1, 0],
        [0, 0.0, 0, 0.0, 10, 627.5, 0.02, 0.05, 0.0, 0.0, 1, 3, 3, 1, 4, 1, 1],
        [0, 0.0, 0, 0.0, 19, 154.2166667, 0.015789474, 0.024561404, 0.0, 0.0, 1, 2, 2, 1, 3, 1, 0],
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.4, 1, 2, 4, 3, 3, 1, 0],
        [1, 0.0, 0, 0.0, 0, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 2, 1, 5, 1, 1],
        [0, 0.0, 0, 0.0, 2, 37.0, 0.0, 0.1, 0.0, 0.8, 1, 2, 2, 2, 3, 1, 0],
        [0, 0.0, 0, 0.0, 3, 738.0, 0.0, 0.022222222, 0.0, 0.4, 1, 2, 4, 1, 2, 1, 0]
    ]
    labels = [0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
    
    model = shopping.train_model(evidence, labels)
    assert "KNeighborsClassifier" in str(type(model)), f"Expected KNeighborsClassifier, got {type(model)}"

def test_train_model_n():
    """Test that train_model returns a k-nearest-neighbor classifier with n=1"""
    evidence = [
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 1, 1, 1, 1, 0],
        [0, 0.0, 0, 0.0, 2, 64.0, 0.0, 0.1, 0.0, 0.0, 1, 2, 2, 1, 2, 1, 0],
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 4, 1, 9, 3, 1, 0],
        [0, 0.0, 0, 0.0, 2, 2.666666667, 0.05, 0.14, 0.0, 0.0, 1, 3, 2, 2, 4, 1, 0],
        [0, 0.0, 0, 0.0, 10, 627.5, 0.02, 0.05, 0.0, 0.0, 1, 3, 3, 1, 4, 1, 1],
        [0, 0.0, 0, 0.0, 19, 154.2166667, 0.015789474, 0.024561404, 0.0, 0.0, 1, 2, 2, 1, 3, 1, 0],
        [0, 0.0, 0, 0.0, 1, 0.0, 0.2, 0.2, 0.0, 0.4, 1, 2, 4, 3, 3, 1, 0],
        [1, 0.0, 0, 0.0, 0, 0.0, 0.2, 0.2, 0.0, 0.0, 1, 1, 2, 1, 5, 1, 1],
        [0, 0.0, 0, 0.0, 2, 37.0, 0.0, 0.1, 0.0, 0.8, 1, 2, 2, 2, 3, 1, 0],
        [0, 0.0, 0, 0.0, 3, 738.0, 0.0, 0.022222222, 0.0, 0.4, 1, 2, 4, 1, 2, 1, 0]
    ]
    labels = [0, 0, 0, 1, 0, 1, 0, 1, 0, 1]
    
    model = shopping.train_model(evidence, labels)
    assert model.n_neighbors == 1, f"Expected n_neighbors to be 1, got {model.n_neighbors}"

def test_evaluate_sensitivity():
    """Test that evaluate provides correct sensitivity"""
    data = [1, 1, 1, 1, 0, 0, 0, 0]
    predictions = np.array([1, 1, 1, 0, 0, 0, 1, 1])
    sensitivity, _ = shopping.evaluate(data, predictions)
    
    expected = 0.75
    assert sensitivity == expected, "evaluate function provides correct values for sensitivity"

def test_evaluate_specificity():
    """Test that evaluate provides correct specificity"""
    data = [1, 1, 1, 1, 0, 0, 0, 0]
    predictions = np.array([1, 1, 1, 0, 0, 0, 1, 1])
    _, specificity = shopping.evaluate(data, predictions)
    
    expected = 0.5
    assert specificity == expected, "evaluate function provides correct values for specificity"