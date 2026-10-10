# Git Workflow Guide (follow this for the Commit History + Branching marks)

## 1. First-time setup
```bash
git init
git branch -M main
git remote add origin https://github.com/<your-username>/student-info-system.git
git add .gitignore README.md requirements.txt
git commit -m "chore: initial project setup with README and .gitignore"
git push -u origin main
```

## 2. One feature branch per feature, merged with a Pull Request
```bash
git checkout -b feature/student-model
git add src/models
git commit -m "feat: add Student model with validation"
git push -u origin feature/student-model
# Open a Pull Request on GitHub -> review -> Merge -> then:
git checkout main && git pull
```

Suggested order (each = branch + PR):
| Branch | What to commit |
|---|---|
| `feature/student-model` | `src/models/` |
| `feature/config-logging` | `src/utils/`, `config/` |
| `feature/student-service` | `src/services/`, `data/` (CRUD + JSON) |
| `feature/cli-menu` | `src/main.py` |
| `feature/search-export` | search + CSV export |
| `feature/unit-tests` | `tests/` |
| `docs/readme-update` | README polish |

## 3. GitHub features to use (and mention in your submission)
- Pull Requests, Issues (open one per feature, close via "Closes #1" in a PR)
- Releases/tags: `git tag v1.0.0 && git push --tags`
- Optional: GitHub Actions to run `pytest` on every push
