# **CISC 3160 FINAL PROJECT**

This project implements a **tokenizer** and **parser** for a simple programming language that supports variable assignments and arithmetic expressions. The program can tokenize input, parse it for syntax validation, and evaluate expressions if they are valid.

---

## **Features**

- Tokenizes identifiers, numbers, operators, and special characters.
- Parses and evaluates expressions with:
  - Addition, subtraction, and multiplication operators.
  - Nested parentheses for operator precedence.
- Detects and reports:
  - **Syntax errors** (e.g., missing semicolons, invalid characters).
  - **Undefined variables**.
  - **Leading zero errors**.

---

## **Project Structure**

```plaintext
.
├── tokenizer.py         # Contains the tokenizer, parser, and evaluation logic.
├── README.md            # Documentation (this file).
```


# Getting Started
## Prerequisites
    Ensure you have Python 3.8 or higher installed

## Installation
1. Clone the repository:
```Bash
    git clone <repository_url>
    cd repository_directory
```
2. Run the program:
```Bash
    python tokenizer.py
```

# Language Specification
The custom language supports the following grammar:
```Bash
Program:
    Assignment*

Assignment:
    Identifier = Exp;

Exp: 
    Exp + Term | Exp - Term | Term

Term:
    Term * Fact  | Fact

Fact:
    ( Exp ) | - Fact | + Fact | Literal | Identifier

Identifier:
    Letter [Letter | Digit]*

Letter:
    a|...|z|A|...|Z|_

Literal:
    0 | NonZeroDigit Digit*
        
NonZeroDigit:
    1|...|9

Digit:
    0|1|...|9
```

# How it works
## 1. Tokenization
    - Splits the input program into tokens such as:
        - Identifier (e.g., x, y, counter)
        - NUMBER (e.g., 123,0)
        - Operatros like (+, -, *), and symbols like ( "(, ), ;, =" )
    - Validates:
        - No leading zeros (e.g., (001) is invalid)
        - No invalid characters in the input
## 2. Parsing
    - Ensures the program adheres to the defined grammar
    - Detects:
        - Missing semicolons
        - Invalid syntax (e.g., x + = y)

## 3. Evaluations
    - Executes valid assignments and expressions
    - Reports errors such as:
        - Undefined variables (e.g., using a variable before it's assigned)
        - Errors usage with semicolons (e.g., ending a statement and initialize another statement)

# Examples:
## Example 1:
```Bash
Input:
x = 1; 
y = 2; 
z = ---(x+y)*(x+-y);

Output:
x = 1
y = 2
z = 3
```

```Bash
Input:
x = 001;

Output:
Error: Leading zeroes are not allowed
```

# Contributing
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a new feature branch:
```Bash
git checkout -b feature-name
```
3. Commit your changes:
```Bash
git commit -m 'add feature-name'
```
4. Push to the branch
```Bash
git push origin feature-name
```
5. Open a PR (pull request)

# License
This project is licensed under the MIT License. See the LICENSE file for details.
Feel free to update sections like 
**repository URL**, **contributing guidelines**, or **license** based on your project details. Let me know if you need further refinements!


