# Num, Operator, and BinOp Classes: A Python Numeric Evaluation Library

## Overview

This repository contains a Python implementation of numeric classes and an arithmetic expression evaluator. The primary components are the `Num` class for number representation, the `Operator` class for performing operations, and the `BinOp` class for binary operations. The library can evaluate simple mathematical expressions consisting of addition, subtraction, multiplication, and other common operations.

## Features

1. **Num Class**: A wrapper around Python numbers, supporting both integers and floating-point numbers. It provides the following:

* Conversion between numeric types (`int`, `float`).

* Arithmetic operations (`+`, `-`, `*`, `/`, `//`, `%`, `**`).

* Comparison operators (`==`, `!=`, `<`, `<=`, `>`, `>=`).

2. **Operator Class**: Represents arithmetic operators (`+`, `-`, `*`, `/`, etc.) and allows combining numeric expressions with callable operations.

3. **BinOp Class**: Represents binary operations using the `Num` and `Operator` classes, allowing construction and evaluation of arithmetic expressions.

4. **Tokenizer and Parser**: Utilities to tokenize and parse mathematical expressions, enabling evaluation of expressions with multiple operators and nested subexpressions.

