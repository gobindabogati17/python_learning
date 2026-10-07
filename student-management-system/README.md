# Student Management System (Python)

A command-line program for keeping track of students, their marks and grades. I built it while studying Programming in Python (TECH1200) at Kaplan Business School, and this repo shows how it changed as I learned more.

## Versions

**Version 1** (`version1_basic.py`) was my first attempt. It keeps students in a list of tuples, works out a grade from the mark, and lets you add, remove and view students. Everything is lost when the program closes.

**Version 2** (`student_management.py`) is the current one. I rewrote it to practise:

- classes (`Student` and `StudentManager`)
- saving and loading data with a JSON file
- splitting the program into functions
- input validation and error handling
- exporting to CSV

## Features (version 2)

1. Add a student with a mark from 0 to 100. Each student gets an ID number.
2. Remove a student by ID or name, with a confirmation step.
3. View all students sorted by ID, name or mark.
4. Search by part of a name.
5. Update a mark. The grade changes with it.
6. Class statistics: average, highest, lowest, pass rate and grade distribution.
7. Export everything to `students_export.csv`.

Grades follow the Australian scale:

| Mark | Grade |
|------|-------|
| 85-100 | HD (High Distinction) |
| 75-84 | D (Distinction) |
| 65-74 | C (Credit) |
| 50-64 | P (Pass) |
| 0-49 | F (Fail) |

## How to run it

You need Python 3. No extra packages are required.

```
python student_management.py
```

Data is saved to `students.json` in the same folder, so your students are still there next time you run it.

## What I'd like to add next

- unit tests with `unittest` or `pytest`
- marks for more than one subject per student
- a simple GUI with Tkinter
- storing data in SQLite instead of JSON
