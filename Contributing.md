# Contributing to my-twin

First off, thank you for considering contributing to my-twin! It's people like you that make this digital twin system better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Process](#development-process)
- [Style Guidelines](#style-guidelines)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)

## 📜 Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. Please read and follow our [Code of Conduct](CODE_OF_CONDUCT.md) to keep our community approachable and respectable.

In short:
- Be respectful and inclusive
- Be patient and welcoming
- Be collaborative
- Focus on what's best for the community

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Virtual environment knowledge
- Basic understanding of AI/ML concepts

### Setting Up Your Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork**
```bash
git clone https://github.com/YOUR_USERNAME/my-twin.git
cd my-twin
```

3. **Add the upstream repository**
```bash
git remote add upstream https://github.com/Allreality/my-twin.git
```

4. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

5. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Development dependencies
```

6. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your configuration
```

7. **Verify setup**
```bash
python verify_setup.py
```

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the [issue tracker](https://github.com/Allreality/my-twin/issues) to avoid duplicates.

When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Environment details**:
  - OS and version
  - Python version
  - my-twin version

**Example Bug Report:**

```markdown
**Title:** Emotional state not persisting between sessions

**Description:**
The emotional state resets to neutral after ending and restarting a session, 
even though ENABLE_EMOTIONAL_STATE=true in .env

**Steps to Reproduce:**
1. Start a session with emotional tracking enabled
2. Have a conversation that generates positive emotions
3. End the session
4. Start a new session
5. Check emotional state

**Expected:** Emotional state should persist or gradually decay
**Actual:** Emotional state resets to neutral immediately

**Environment:**
- OS: Ubuntu 22.04
- Python: 3.10.2
- my-twin: 1.0.0
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case**: Why is this enhancement needed?
- **Proposed solution**: How should it work?
- **Alternatives considered**: What other approaches did you think about?
- **Additional context**: Mockups, examples, etc.

### Your First Code Contribution

Unsure where to begin? Look for issues tagged with:

- `good first issue` - Simple issues perfect for newcomers
- `help wanted` - Issues that need assistance
- `documentation` - Documentation improvements

### Pull Requests

We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the style guidelines
6. Issue that pull request!

## 🔨 Development Process

### Branch Naming Convention

Use descriptive branch names with prefixes:

- `feature/` - New features
- `bugfix/` - Bug fixes
- `hotfix/` - Critical fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/modifications

**Examples:**
```bash
feature/add-voice-input
bugfix/emotional-state-persistence
docs/update-memory-system-guide
refactor/optimize-semantic-memory
```

### Development Workflow

1. **Create a feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make your changes**
   - Write clear, concise code
   - Add comments for complex logic
   - Update documentation as needed

3. **Test your changes**
```bash
# Run existing tests
python -m pytest tests/

# Test specific components
python test_basic_twin.py
python test_claude_basic.py
```

4. **Commit your changes** (see [Commit Guidelines](#commit-guidelines))
```bash
git add .
git commit -m "feat: add voice input support"
```

5. **Keep your branch updated**
```bash
git fetch upstream
git rebase upstream/main
```

6. **Push to your fork**
```bash
git push origin feature/your-feature-name
```

7. **Create a Pull Request**

## 🎨 Style Guidelines

### Python Code Style

Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) with these specifics:

**Formatting:**
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (Black formatter default)
- Use double quotes for strings (except to avoid escaping)

**Naming Conventions:**
```python
# Classes: PascalCase
class DigitalTwin:
    pass

# Functions and variables: snake_case
def process_input(user_message):
    emotional_state = get_current_emotion()
    
# Constants: UPPER_SNAKE_CASE
MAX_MEMORY_SIZE = 1000
DEFAULT_PERSONALITY = "my_PERSONALITY.txt"

# Private methods: _leading_underscore
def _internal_process(self):
    pass
```

**Docstrings:**
```python
def process_input(self, user_input: str, context: dict = None) -> str:
    """
    Process user input through the digital twin system.
    
    Args:
        user_input (str): The user's message or query
        context (dict, optional): Additional context for processing
        
    Returns:
        str: The twin's response
        
    Raises:
        ValueError: If user_input is empty
        
    Example:
        >>> twin = DigitalTwin()
        >>> response = twin.process_input("Hello!")
        >>> print(response)
        'Hello! How can I assist you today?'
    """
    pass
```

**Type Hints:**
```python
from typing import List, Dict, Optional, Union

def get_memories(
    self,
    query: str,
    limit: int = 10,
    memory_type: Optional[str] = None
) -> List[Dict[str, Union[str, float]]]:
    """Retrieve memories matching the query."""
    pass
```

### Code Organization

**File Structure:**
```python
# 1. Standard library imports
import os
import sys
from datetime import datetime

# 2. Third-party imports
import numpy as np
from anthropic import Anthropic

# 3. Local application imports
from .memory import SemanticMemory
from .personality import PersonalityEngine

# 4. Constants
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30

# 5. Classes and functions
class MyClass:
    pass

def my_function():
    pass
```

**Module Organization:**
```
my_module/
├── __init__.py
├── core.py           # Core functionality
├── utils.py          # Utility functions
├── exceptions.py     # Custom exceptions
└── tests/
    └── test_core.py
```

### Documentation Style

**README sections:**
- Clear, descriptive headings
- Code examples for major features
- Installation instructions
- Quick start guide
- API documentation

**Code comments:**
```python
# Good: Explains WHY
# Use exponential decay to gradually reduce emotional intensity
# This mimics natural emotional fade in human psychology
emotion_value *= self.decay_rate

# Bad: Explains WHAT (obvious from code)
# Multiply emotion_value by decay_rate
emotion_value *= self.decay_rate
```

## 📝 Commit Guidelines

We follow [Conventional Commits](https://www.conventionalcommits.org/):

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```bash
# Feature
feat(memory): add semantic memory compression

# Bug fix
fix(personality): correct trait weight calculation

# Documentation
docs(readme): update installation instructions

# Multiple changes
feat(twin): add voice input support

- Implement audio capture
- Add speech-to-text conversion
- Integrate with existing input processing
- Update documentation

Closes #123
```

### Commit Message Guidelines

- Use present tense ("add feature" not "added feature")
- Use imperative mood ("move cursor to..." not "moves cursor to...")
- Capitalize the first letter
- No period at the end of the subject line
- Limit subject line to 50 characters
- Wrap body at 72 characters
- Reference issues and PRs in the footer

## 🔍 Pull Request Process

### Before Submitting

1. **Update documentation** for any changed functionality
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update CHANGELOG.md** if applicable
5. **Check code style** with linters

### PR Title Format

Follow the same format as commit messages:

```
feat(memory): add long-term memory persistence
fix(api): correct authentication token validation
docs(contributing): add PR process section
```

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix (non-breaking change fixing an issue)
- [ ] New feature (non-breaking change adding functionality)
- [ ] Breaking change (fix or feature causing existing functionality to break)
- [ ] Documentation update

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] No new warnings generated
- [ ] Tests added for changes
- [ ] All tests passing

## Related Issues
Closes #(issue number)

## Screenshots (if applicable)
```

### Review Process

1. **Automated checks**: CI/CD runs tests and style checks
2. **Code review**: Maintainers review your code
3. **Revisions**: Address feedback and update PR
4. **Approval**: Once approved, your PR will be merged

### After Your PR is Merged

1. Delete your feature branch
2. Pull the latest changes from upstream
3. Celebrate! 🎉

## 🧪 Testing Guidelines

### Writing Tests

```python
import pytest
from my_twin import DigitalTwin

def test_twin_initialization():
    """Test that twin initializes correctly."""
    twin = DigitalTwin()
    assert twin is not None
    assert twin.personality is not None

def test_memory_storage():
    """Test that memories are stored correctly."""
    twin = DigitalTwin()
    twin.store_memory("test memory")
    memories = twin.get_memories()
    assert len(memories) == 1
    assert memories[0]["content"] == "test memory"

@pytest.mark.parametrize("input,expected", [
    ("hello", "greeting"),
    ("goodbye", "farewell"),
])
def test_message_classification(input, expected):
    """Test message classification."""
    twin = DigitalTwin()
    result = twin.classify_message(input)
    assert result == expected
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_memory.py

# Run with coverage
pytest --cov=my_twin tests/

# Run with verbose output
pytest -v
```

## 📚 Additional Resources

- [Project Documentation](https://github.com/Allreality/my-twin/wiki)
- [Issue Tracker](https://github.com/Allreality/my-twin/issues)
- [Discussions](https://github.com/Allreality/my-twin/discussions)

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 💬 Questions?

- Open a [Discussion](https://github.com/Allreality/my-twin/discussions)
- Create an [Issue](https://github.com/Allreality/my-twin/issues)

---

Thank you for contributing to my-twin! 🚀