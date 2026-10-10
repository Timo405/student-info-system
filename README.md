# Student Information System

A command-line Student Information System built in Python with a cloud-ready architecture: modular code, external configuration, structured logging, and robust error handling. Data is stored in JSON.

## Features
- **CRUD**: add, view, update, delete students
- **JSON persistence** with atomic writes (no half-written files)
- **Auto-generated student IDs**, created/updated timestamps
- **Validation**: email format, year level (1-6), GPA (0.0-5.0), required fields, duplicate emails
- **Search** by name, ID, course or email
- **CSV export**
- **Error recovery**: a corrupt data file is backed up (`.corrupt`) and the app restarts cleanly
- **Logging** to `logs/app.log`
- **Unit tests** with pytest

## Project Structure
```
student-info-system/
├── src/
│   ├── models/student.py            # Student model + validation
│   ├── services/student_service.py  # CRUD, search, export, persistence
│   ├── utils/config.py              # Config loader (file + env overrides)
│   ├── utils/logger.py              # Logging setup
│   └── main.py                      # CLI menu
├── data/students.json
├── config/config.json
├── logs/
├── tests/
├── requirements.txt
└── README.md
```

## Getting Started
```bash
git clone https://github.com/Timo405/student-info-system.git
cd student-info-system
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m src.main
```

## Configuration
Edit `config/config.json`, or override any key with an environment variable prefixed `SIS_` (useful in containers/cloud):
```bash
SIS_DATA_FILE=/mnt/storage/students.json python -m src.main
```

| Key | Purpose | Default |
|---|---|---|
| `data_file` | JSON database path | `data/students.json` |
| `export_file` | CSV export path | `data/students_export.csv` |
| `log_file` | Log path | `logs/app.log` |
| `log_level` | DEBUG/INFO/WARNING/ERROR | `INFO` |

## Running Tests
```bash
python -m pytest
```

## Design Notes
- **Separation of concerns**: model (data/rules), service (business logic), utils (infrastructure), main (UI).
- **Cloud-readiness**: no hard-coded paths, env-var overrides, logs written to a file that can be shipped to a log aggregator.

## Author
Timothy Manasan
