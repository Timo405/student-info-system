"""Student service: CRUD, search and export, persisted as JSON.

Records are exchanged as plain dictionaries (easy to serialise to JSON).
"""
import csv
import json
import logging
import os
from datetime import datetime

from src.models.student import Student, ValidationError, validate_fields

log = logging.getLogger("sis")

FIELDS = ["student_id", "name", "email", "course", "year_level", "gpa",
          "created_at", "updated_at"]


class StudentService:
    def __init__(self, data_file="data/students.json", export_file="data/students_export.csv"):
        self.data_file = data_file
        self.export_file = export_file
        self._ensure_data_file()

    # ---------- persistence ----------
    def _ensure_data_file(self):
        """Create the data folder and an empty JSON file if missing."""
        os.makedirs(os.path.dirname(self.data_file) or ".", exist_ok=True)
        if not os.path.exists(self.data_file):
            self._save_students([])

    def _load_students(self):
        """Read all records. A corrupt file is backed up and replaced (recovery)."""
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            if not isinstance(data, list):
                raise ValueError("Top-level JSON must be a list")
            return data
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, ValueError) as exc:
            backup = self.data_file + ".corrupt"
            os.replace(self.data_file, backup)
            log.error("Corrupt data file (%s). Backed up to %s", exc, backup)
            self._save_students([])
            return []

    def _save_students(self, students):
        """Write atomically so a crash never leaves a half-written file."""
        tmp = self.data_file + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(students, f, indent=2)
            os.replace(tmp, self.data_file)
        except OSError as exc:
            log.error("Failed to save data: %s", exc)
            raise

    # ---------- CRUD ----------
    def add_student(self, student_data):
        """Validate and store a new student; returns the saved record."""
        students = self._load_students()
        student = Student(**student_data)  # raises ValidationError if invalid
        if any(s["email"].lower() == student.email.lower() for s in students):
            raise ValidationError("A student with that email already exists.")
        students.append(student.to_dict())
        self._save_students(students)
        log.info("Added student %s", student.student_id)
        return student.to_dict()

    def get_all_students(self):
        return self._load_students()

    def get_student(self, student_id):
        """Return the record, or None if not found."""
        for student in self._load_students():
            if student["student_id"] == student_id:
                return student
        return None

    def update_student(self, student_id, update_data):
        """Update fields (blank values are ignored). Returns record or None."""
        students = self._load_students()
        for student in students:
            if student["student_id"] == student_id:
                changes = {k: v for k, v in update_data.items()
                           if k in ("name", "email", "course", "year_level", "gpa")
                           and v not in (None, "")}
                merged = {**student, **changes}
                # Re-validate the merged record
                merged["year_level"], merged["gpa"] = validate_fields(
                    merged["name"], merged["email"], merged["course"],
                    merged["year_level"], merged["gpa"])
                student.update(merged)
                student["updated_at"] = datetime.now().isoformat()
                self._save_students(students)
                log.info("Updated student %s", student_id)
                return student
        return None

    def delete_student(self, student_id):
        """Delete a student. Returns True if a record was removed."""
        students = self._load_students()
        remaining = [s for s in students if s["student_id"] != student_id]
        if len(remaining) == len(students):
            return False
        self._save_students(remaining)
        log.info("Deleted student %s", student_id)
        return True

    # ---------- bonus features ----------
    def search_students(self, keyword):
        """Case-insensitive search across ID, name, email and course."""
        kw = keyword.strip().lower()
        return [s for s in self._load_students()
                if any(kw in str(s[k]).lower()
                       for k in ("student_id", "name", "email", "course"))]

    def export_csv(self, path=None):
        path = path or self.export_file
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        students = self._load_students()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(students)
        log.info("Exported %d students to %s", len(students), path)
        return path
