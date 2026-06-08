# Contributing to ChineseMet

Thank you for your interest in contributing to ChineseMet! We welcome contributions from the community.

## How to Contribute

### Reporting Issues

If you find a bug or have a suggestion:

1. Check if the issue already exists in the [issue tracker](https://github.com/your-org/ChineseMet/issues)
2. If not, open a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Your environment details (OS, Python version, etc.)

### Adding Questions

To add new meteorological questions to the dataset:

1. Fork the repository
2. Add your questions to a new JSON file following the existing format:
   ```json
   {
     "id": -1,
     "subject": "天气分析",
     "task": "单项选择题",
     "question": "Question text in Chinese",
     "choices": {
       "A": "Option A",
       "B": "Option B",
       "C": "Option C",
       "D": "Option D"
     },
     "answer": ["A"],
     "analysis": "Optional explanation"
   }
   ```
   Use `单项选择题` for single-choice questions and `多项选择题` for multiple-choice questions.
3. Submit a pull request with a clear description

### Code Contributions

1. Fork the repository
2. Create a new branch: `git checkout -b feature/your-feature-name`
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

### Code Style

- Follow PEP 8 for Python code
- Add docstrings to all functions and classes
- Use type hints where appropriate
- Keep functions focused and modular

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/ChineseMet.git
cd ChineseMet

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r src/requirements.txt

# Run a syntax check
python -m compileall src examples
```

## Questions?

Feel free to open an issue for any questions or discussions.
