"""Student Information System - command-line application.

Run from the project root:  python -m src.main
"""
import logging

from src.models.student import ValidationError
from src.services.student_service import StudentService
from src.utils.config import load_config
from src.utils.logger import setup_logger


class StudentInformationSystem:
    def __init__(self):
        config = load_config()
        setup_logger(config["log_file"], config["log_level"])
        self.logger = logging.getLogger("sis")
        self.student_service = StudentService(config["data_file"], config["export_file"])
        self.logger.info("Application started")

    def display_menu(self):
        print("\n=== Student Information System ===")
        print("1. Add Student")
        print("2. View All Students")
        print("3. View Student by ID")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Search Students")
        print("7. Export to CSV")
        print("8. Exit")

    def add_student(self):
        print("\n--- Add New Student ---")
        student_data = {
            "name": input("Name: "),
            "email": input("Email: "),
            "course": input("Course: "),
            "year_level": input("Year Level (1-6): "),
            "gpa": input("GPA (0.0-5.0, Enter for 0): ") or 0.0,
        }
        try:
            student = self.student_service.add_student(student_data)
            self.logger.info(f"Added student: {student['student_id']}")
            print(f"Student added successfully! ID: {student['student_id']}")
        except ValidationError as e:
            self.logger.warning(f"Validation failed: {e}")
            print(f"Invalid input: {e}")
        except Exception as e:
            self.logger.error(f"Error adding student: {e}")
            print("Error adding student.")

    def view_all_students(self):
        print("\n--- All Students ---")
        students = self.student_service.get_all_students()
        if not students:
            print("No students found.")
            return
        for student in students:
            print(f"ID: {student['student_id']}, Name: {student['name']}, "
                  f"Email: {student['email']}, Course: {student['course']}, "
                  f"Year: {student['year_level']}, GPA: {student['gpa']}")

    def view_student(self):
        student_id = input("Enter Student ID: ").strip()
        student = self.student_service.get_student(student_id)
        if student:
            print("\nStudent Details:")
            for key, value in student.items():
                print(f"  {key}: {value}")
        else:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()
        current = self.student_service.get_student(student_id)
        if not current:
            print("Student not found.")
            return
        print("Press Enter to keep the current value.")
        update_data = {
            "name": input(f"Name [{current['name']}]: "),
            "email": input(f"Email [{current['email']}]: "),
            "course": input(f"Course [{current['course']}]: "),
            "year_level": input(f"Year Level [{current['year_level']}]: "),
            "gpa": input(f"GPA [{current['gpa']}]: "),
        }
        try:
            self.student_service.update_student(student_id, update_data)
            print("Student updated successfully!")
        except ValidationError as e:
            print(f"Invalid input: {e}")
        except Exception as e:
            self.logger.error(f"Error updating student: {e}")
            print("Error updating student.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()
        if input(f"Delete {student_id}? (y/n): ").lower() != "y":
            print("Cancelled.")
            return
        if self.student_service.delete_student(student_id):
            print("Student deleted successfully!")
        else:
            print("Student not found.")

    def search_students(self):
        results = self.student_service.search_students(input("Search keyword: "))
        if not results:
            print("No matches found.")
        for s in results:
            print(f"ID: {s['student_id']}, Name: {s['name']}, Course: {s['course']}")

    def export_students(self):
        try:
            print(f"Exported to {self.student_service.export_csv()}")
        except OSError as e:
            self.logger.error(f"Export failed: {e}")
            print("Export failed. Check the logs.")

    def run(self):
        actions = {
            "1": self.add_student, "2": self.view_all_students,
            "3": self.view_student, "4": self.update_student,
            "5": self.delete_student, "6": self.search_students,
            "7": self.export_students,
        }
        while True:
            self.display_menu()
            try:
                choice = input("Enter your choice (1-8): ").strip()
                if choice == "8":
                    self.logger.info("Application exited")
                    print("Goodbye!")
                    break
                action = actions.get(choice)
                if action:
                    action()
                else:
                    print("Invalid choice. Please try again.")
            except (KeyboardInterrupt, EOFError):
                print("\nGoodbye!")
                break
            except Exception:  # last-resort safety net
                self.logger.exception("Unexpected error")
                print("Something went wrong. Details were written to the log.")


if __name__ == "__main__":
    app = StudentInformationSystem()
    app.run()
