import pytest
from src.models.student import Student, ValidationError
from src.services.student_service import StudentService


@pytest.fixture
def service(tmp_path):
    return StudentService(str(tmp_path / "students.json"), str(tmp_path / "export.csv"))


def data(name="Ana Cruz", email="ana@example.com"):
    return {"name": name, "email": email, "course": "BSCS", "year_level": "2", "gpa": "1.75"}


def test_add_generates_id_and_timestamps(service):
    s = service.add_student(data())
    assert len(s["student_id"]) == 8
    assert s["created_at"] and s["year_level"] == 2 and s["gpa"] == 1.75


def test_get_student(service):
    sid = service.add_student(data())["student_id"]
    assert service.get_student(sid)["name"] == "Ana Cruz"
    assert service.get_student("nope") is None


def test_update(service):
    sid = service.add_student(data())["student_id"]
    updated = service.update_student(sid, {"name": "Ana Reyes", "gpa": "", "year_level": "3"})
    assert updated["name"] == "Ana Reyes" and updated["year_level"] == 3
    assert updated["gpa"] == 1.75  # blank keeps old value
    assert service.update_student("nope", {"name": "X"}) is None


def test_update_validates(service):
    sid = service.add_student(data())["student_id"]
    with pytest.raises(ValidationError):
        service.update_student(sid, {"email": "bad"})


def test_delete(service):
    sid = service.add_student(data())["student_id"]
    assert service.delete_student(sid) is True
    assert service.delete_student(sid) is False


def test_persistence(tmp_path):
    path = str(tmp_path / "s.json")
    sid = StudentService(path).add_student(data())["student_id"]
    assert StudentService(path).get_student(sid) is not None


def test_validation():
    with pytest.raises(ValidationError):
        Student("X", "not-an-email", "BSIT", 1)
    with pytest.raises(ValidationError):
        Student("X", "x@y.com", "BSIT", 9)
    with pytest.raises(ValidationError):
        Student("X", "x@y.com", "BSIT", 1, gpa=7)


def test_duplicate_email_rejected(service):
    service.add_student(data())
    with pytest.raises(ValidationError):
        service.add_student(data(name="Other"))


def test_search(service):
    service.add_student(data())
    service.add_student(data("Ben Lim", "ben@example.com"))
    assert [s["name"] for s in service.search_students("ben")] == ["Ben Lim"]


def test_export_csv(service):
    service.add_student(data())
    assert "Ana Cruz" in open(service.export_csv()).read()


def test_corrupt_file_recovery(tmp_path):
    path = tmp_path / "s.json"
    path.write_text("{ broken")
    service = StudentService(str(path))
    assert service.get_all_students() == []
    assert (tmp_path / "s.json.corrupt").exists()
