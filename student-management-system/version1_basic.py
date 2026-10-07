# =====================================================
# STUDENT MANAGEMENT SYSTEM - Version 1 (Basic)
# Created by Gobinda Bogati
# Stores each student as a tuple (name, grade) in a list
# =====================================================

students = []

# Loop keeps showing the menu until the user chooses to exit
while True:
    print("\n===== STUDENT MANAGEMENT SYSTEM =====")
    print("1. Add Student")
    print("2. Remove Student")
    print("3. View Students")
    print("4. Exit")
    choice = input("Enter your choice: ")

    # Add Student
    if choice == "1":
        name = input("Enter student name: ").strip()

        # Check the name is not empty
        if name == "":
            print("Name cannot be empty.")
            continue

        # Check the student has not already been added
        duplicate = False
        for student in students:
            if student[0].lower() == name.lower():
                duplicate = True
                break
        if duplicate:
            print("That student has already been added.")
            continue

        # Keep asking until a valid mark between 0 and 100 is entered
        while True:
            mark_input = input("Enter student mark: ")
            if mark_input.isdigit() and 0 <= int(mark_input) <= 100:
                mark = int(mark_input)
                break
            print("Invalid mark. Please enter a whole number between 0 and 100.")

        # Grade categorisation
        if mark >= 85:
            grade = "HD"
            message = "You got a High Distinction."
        elif mark >= 75:
            grade = "D"
            message = "You got a Distinction."
        elif mark >= 65:
            grade = "C"
            message = "You got a Credit."
        elif mark >= 50:
            grade = "P"
            message = "You have passed."
        else:
            grade = "F"
            message = "You have failed."

        # Store student name and grade
        students.append((name, grade))
        print("\nStudent added successfully.")
        print("Name:", name)
        print("Grade:", grade)
        print(message)

    # Remove Student
    elif choice == "2":
        if len(students) == 0:
            print("No students available to remove.")
        else:
            name = input("Enter student name to remove: ").strip()
            for student in students:
                if student[0].lower() == name.lower():
                    students.remove(student)
                    print("Student removed successfully.")
                    break
            else:
                # The else runs only if the loop finished without a break
                print("Student not found.")

    # View Students
    elif choice == "3":
        if len(students) == 0:
            print("No students available.")
        else:
            print("\n===== STUDENT LIST =====")
            for student in students:
                print("Name:", student[0], "| Grade:", student[1])
            print("Total students:", len(students))

    # Exit
    elif choice == "4":
        print("Exiting Student Management System...")
        break

    # Invalid choice
    else:
        print("Invalid choice. Please select 1, 2, 3 or 4.")
