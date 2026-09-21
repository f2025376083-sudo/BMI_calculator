# BMI Calculator – Python GUI Application

A professional BMI (Body Mass Index) Calculator developed in Python using Tkinter, SQLite, and Matplotlib. The application provides a user-friendly graphical interface for calculating BMI, categorizing results, storing user records, and visualizing BMI trends over time.

## Project Overview

This project was developed as part of *Task 2 – BMI Calculator*. It demonstrates practical implementation of Python programming, GUI development, database management, input validation, error handling, and data visualization.

The application allows users to enter their name, weight, and height to calculate their BMI. Each result can be stored locally and reviewed later through a personalized BMI history and trend graph.

## Key Features

- *Graphical User Interface*
  - Built with Python Tkinter
  - Simple and user-friendly interface
  - No command-line interaction required

- *BMI Calculation*
  - Calculates BMI using the standard formula:
  
  BMI = Weight (kg) / Height² (m²)

- *BMI Classification*
  - Underweight: BMI < 18.5
  - Normal: BMI 18.5–24.9
  - Overweight: BMI 25–29.9
  - Obese: BMI ≥ 30

- *Input Validation*
  - Prevents empty input
  - Rejects non-numeric values
  - Rejects zero and negative values
  - Displays helpful error messages

- *Multi-User Support*
  - Allows BMI records to be saved for different users
  - User-specific history can be retrieved

- *Data Persistence*
  - Uses SQLite for local data storage
  - BMI records remain available after closing the application

- *BMI History*
  - Displays previously saved BMI records
  - Shows date, weight, height, BMI, and category

- *BMI Trend Visualization*
  - Generates a line chart using Matplotlib
  - Helps visualize changes in BMI over multiple records

- *Error Handling*
  - Handles database read/write errors
  - Handles graph and input-related errors
  - Provides user-friendly messages

## Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Core programming language |
| Tkinter | Graphical User Interface |
| SQLite | Local database and data persistence |
| Matplotlib | BMI trend visualization |

## Project Structure

```text
BMI_Calculator_Project/
│
├── app.py
├── README.md
├── requirements.txt
└── .gitignore
