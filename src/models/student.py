"""Student model: data object with auto-generated ID, timestamps and validation."""
import re
import uuid
from datetime import datetime

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+(\.[\w-]+)+$")


class ValidationError(ValueError):
    """Raised when student data fails validation."""


def validate_fields(name, email, course, year_level, gpa):
    """Validate raw values and return cleaned (year_level:int, gpa:float)."""
    if not str(name).strip():
        raise ValidationError("Name cannot be empty.")
    if not EMAIL_PATTERN.match(str(email).strip()):
        raise ValidationError("Email format is invalid.")
    if not str(course).strip():
        raise ValidationError("Course cannot be empty.")
    try:
        year_level = int(year_level)
    except (TypeError, ValueError):
        raise ValidationError("Year level must be a whole number.")
    if not 1 <= year_level <= 6:
        raise ValidationError("Year level must be between 1 and 6.")
    try:
        gpa = float(gpa)
    except (TypeError, ValueError):
        raise ValidationError("GPA must be a number.")
    if not 0.0 <= gpa <= 5.0:
        raise ValidationError("GPA must be between 0.0 and 5.0.")
    return year_level, gpa


class Student:
    def __init__(self, name, email, course, year_level, gpa=0.0,
                 student_id=None, created_at=None, updated_at=None):
        year_level, gpa = validate_fields(name, email, course, year_level, gpa)
        # Auto-generate a short unique ID when none is supplied
        self.student_id = student_id or str(uuid.uuid4())[:8]
        self.name = str(name).strip()
        self.email = str(email).strip()
        self.course = str(course).strip()
        self.year_level = year_level
        self.gpa = gpa
        now = datetime.now().isoformat()
        self.created_at = created_at or now
        self.updated_at = updated_at or now

    def to_dict(self):
        """Convert to a JSON-serialisable dictionary."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "course": self.course,
            "year_level": self.year_level,
            "gpa": self.gpa,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)

    def __str__(self):
        return (f"[{self.student_id}] {self.name} | {self.email} | "
                f"{self.course} | Year {self.year_level} | GPA {self.gpa}")
