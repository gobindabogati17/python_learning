# =====================================================
# STUDENT MANAGEMENT SYSTEM - Version 2 (Advanced)
# Created by Gobinda Bogati
#
# What's new compared to version 1:
#   - Uses classes (Student and StudentManager)
#   - Saves students to a JSON file so data stays after closing
#   - Each student gets an ID and their actual mark is stored
#   - Search, update mark, sort, statistics and CSV export
#   - Code split into functions instead of one big loop
# =====================================================

import csv
import json
import os
from datetime import datetime

DATA_FILE = "students.json"
EXPORT_FILE = "students_export.csv"

# Grade boundaries, checked from highest to lowest
GRADE_BANDS = [
    (85, "HD", "High Distinction"),
    (75, "D", "Distinction"),
    (65, "C", "Credit"),
    (50, "P", "Pass"),
    (0, "F", "Fail"),
]


def get_grade(mark):
    """Return (grade, label) for a mark between 0 and 100."""
    for minimum, grade, label in GRADE_BANDS:
        if mark >= minimum:
            return grade, label


# -----------------------------------------------------
# Student class: holds the details of one student
# -----------------------------------------------------
class Student:
    def __init__(self, student_id, name, mark, added_on=None):
        self.student_id = student_id
        self.name = name
        self.mark = mark
        self.added_on = added_on or datetime.now().strftime("%Y-%m-%d %H:%M")

    # The grade is worked out from the mark every time,
    # so it can never get out of sync after a mark update
    @property
    def grade(self):
        return get_grade(self.mark)[0]

    @property
    def grade_label(self):
        return get_grade(self.mark)[1]

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "mark": self.mark,
            "added_on": self.added_on,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data["student_id"], data["name"], data["mark"], data.get("added_on"))


# -----------------------------------------------------
# StudentManager class: looks after the whole list
# and saving/loading it from the file
# -----------------------------------------------------
class StudentManager:
    def __init__(self, filename=DATA_FILE):
        self.filename = filename
        self.students = []
        self.load()

    def load(self):
        if not os.path.exists(self.filename):
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
            self.students = [Student.from_dict(item) for item in data]
        except (json.JSONDecodeError, KeyError, TypeError):
            print("Warning: the data file could not be read. Starting with an empty list.")
            self.students = []

    def save(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([s.to_dict() for s in self.students], file, indent=4)

    def next_id(self):
        if not self.students:
            return 1
        return max(s.student_id for s in self.students) + 1

    def find_by_name(self, name):
        for student in self.students:
            if student.name.lower() == name.lower():
                return student
        return None

    def find_by_id(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                return student
        return None

    def search(self, text):
        text = text.lower()
        return [s for s in self.students if text in s.name.lower()]

    def add(self, name, mark):
        student = Student(self.next_id(), name, mark)
        self.students.append(student)
        self.save()
        return student

    def remove(self, student):
        self.students.remove(student)
        self.save()

    def update_mark(self, student, new_mark):
        student.mark = new_mark
        self.save()

    def sorted_students(self, sort_by):
        if sort_by == "name":
            return sorted(self.students, key=lambda s: s.name.lower())
        if sort_by == "mark":
            return sorted(self.students, key=lambda s: s.mark, reverse=True)
        return sorted(self.students, key=lambda s: s.student_id)

    def statistics(self):
        marks = [s.mark for s in self.students]
        top = max(self.students, key=lambda s: s.mark)
        bottom = min(self.students, key=lambda s: s.mark)
        passed = sum(1 for m in marks if m >= 50)

        distribution = {grade: 0 for _, grade, _ in GRADE_BANDS}
        for student in self.students:
            distribution[student.grade] += 1

        return {
            "total": len(marks),
            "average": sum(marks) / len(marks),
            "top": top,
            "bottom": bottom,
            "pass_rate": passed / len(marks) * 100,
            "distribution": distribution,
        }

    def export_csv(self, filename=EXPORT_FILE):
        with open(filename, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Mark", "Grade", "Added On"])
            for s in self.sorted_students("id"):
                writer.writerow([s.student_id, s.name, s.mark, s.grade, s.added_on])
        return filename


# -----------------------------------------------------
# Input helpers: keep asking until the input is valid
# -----------------------------------------------------
def ask_mark(prompt="Enter student mark (0-100): "):
    while True:
        mark_input = input(prompt).strip()
        if mark_input.isdigit() and 0 <= int(mark_input) <= 100:
            return int(mark_input)
        print("Invalid mark. Please enter a whole number between 0 and 100.")


def ask_yes_no(prompt):
    while True:
        answer = input(prompt + " (y/n): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Please type y or n.")


def pick_student(manager):
    """Let the user choose a student by ID number or by full name."""
    entry = input("Enter student ID or name: ").strip()
    if entry.isdigit():
        student = manager.find_by_id(int(entry))
    else:
        student = manager.find_by_name(entry)
    if student is None:
        print("Student not found.")
    return student


def print_table(students):
    print(f"\n{'ID':<5}{'Name':<22}{'Mark':>5}  {'Grade':<6}{'Result'}")
    print("-" * 55)
    for s in students:
        print(f"{s.student_id:<5}{s.name:<22}{s.mark:>5}  {s.grade:<6}{s.grade_label}")
    print("-" * 55)
    print("Total students:", len(students))


# -----------------------------------------------------
# Menu options
# -----------------------------------------------------
def add_student(manager):
    name = input("Enter student name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return
    if not all(part.isalpha() for part in name.replace("-", " ").replace("'", " ").split()):
        print("Name can only contain letters, spaces, hyphens and apostrophes.")
        return
    if manager.find_by_name(name):
        print("That student has already been added.")
        return

    name = name.title()
    mark = ask_mark()
    student = manager.add(name, mark)

    print("\nStudent added successfully.")
    print("ID:   ", student.student_id)
    print("Name: ", student.name)
    print("Grade:", student.grade, f"({student.grade_label})")


def remove_student(manager):
    if not manager.students:
        print("No students available to remove.")
        return
    student = pick_student(manager)
    if student and ask_yes_no(f"Remove {student.name} (ID {student.student_id})?"):
        manager.remove(student)
        print("Student removed successfully.")


def view_students(manager):
    if not manager.students:
        print("No students available.")
        return
    print("Sort by: 1. ID   2. Name   3. Mark (highest first)")
    option = input("Choose sort order (press Enter for ID): ").strip()
    sort_by = {"2": "name", "3": "mark"}.get(option, "id")
    print_table(manager.sorted_students(sort_by))


def search_students(manager):
    text = input("Enter part of a name to search: ").strip()
    if text == "":
        print("Search text cannot be empty.")
        return
    results = manager.search(text)
    if results:
        print_table(results)
    else:
        print("No students match that search.")


def update_student(manager):
    if not manager.students:
        print("No students available to update.")
        return
    student = pick_student(manager)
    if student is None:
        return
    print(f"Current mark for {student.name}: {student.mark} ({student.grade})")
    old_grade = student.grade
    manager.update_mark(student, ask_mark("Enter new mark (0-100): "))
    print("Mark updated.")
    if student.grade != old_grade:
        print(f"Grade changed from {old_grade} to {student.grade}.")


def show_statistics(manager):
    if not manager.students:
        print("No students yet, so there are no statistics to show.")
        return
    stats = manager.statistics()
    print("\n===== CLASS STATISTICS =====")
    print("Total students:", stats["total"])
    print(f"Average mark:   {stats['average']:.1f}")
    print(f"Highest mark:   {stats['top'].mark} ({stats['top'].name})")
    print(f"Lowest mark:    {stats['bottom'].mark} ({stats['bottom'].name})")
    print(f"Pass rate:      {stats['pass_rate']:.1f}%")
    print("\nGrade distribution:")
    for grade, count in stats["distribution"].items():
        print(f"  {grade:<3}{count:>3}  {'#' * count}")


def export_students(manager):
    if not manager.students:
        print("No students to export.")
        return
    filename = manager.export_csv()
    print(f"Exported {len(manager.students)} students to {filename}")


# -----------------------------------------------------
# Main program
# -----------------------------------------------------
def main():
    manager = StudentManager()

    menu = {
        "1": ("Add Student", add_student),
        "2": ("Remove Student", remove_student),
        "3": ("View Students", view_students),
        "4": ("Search Students", search_students),
        "5": ("Update Student Mark", update_student),
        "6": ("Class Statistics", show_statistics),
        "7": ("Export to CSV", export_students),
    }

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        for key, (label, _) in menu.items():
            print(f"{key}. {label}")
        print("8. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "8":
            print("Data saved. Exiting Student Management System...")
            break
        elif choice in menu:
            menu[choice][1](manager)
        else:
            print("Invalid choice. Please select a number from 1 to 8.")


# Only run the menu when this file is run directly
if __name__ == "__main__":
    main()
