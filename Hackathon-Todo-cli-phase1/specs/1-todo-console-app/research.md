# Research Document: Todo In-Memory Python Console Application

## Python CLI Frameworks Research

### Options Evaluated

1. **argparse** (Built-in)
   - Pros: Part of standard library, no dependencies
   - Cons: Verbose, less intuitive for complex CLIs
   - Python 3.13 Compatibility: Full support

2. **click**
   - Pros: Popular, well-documented, composable commands
   - Cons: More complex for simple use cases, older design patterns
   - Python 3.13 Compatibility: Full support

3. **typer**
   - Pros: Modern, type hint integration, simple for complex CLIs, great developer experience
   - Cons: Additional dependency
   - Python 3.13 Compatibility: Full support

4. **rich-cli**
   - Pros: Beautiful output, rich formatting capabilities
   - Cons: More complex, primarily focused on output formatting
   - Python 3.13 Compatibility: Full support

**Decision**: Typer is selected as it provides the best balance of modern features, type safety, and ease of use.

## uv Package Manager Research

### Overview
uv is a fast Python package installer and resolver written in Rust. It's significantly faster than pip and pip-tools while maintaining compatibility with existing Python packaging standards.

### Key Features
- Fast dependency resolution and installation
- Built-in virtual environment management
- PEP 582 support (project-local packages)
- Compatible with existing Python packaging tools

### Usage with Python 3.13
- uv supports Python 3.13 fully
- Can manage projects targeting Python 3.13
- Creates virtual environments with specified Python versions

### Best Practices
- Use `uv venv` to create virtual environments
- Use `uv pip install` for installing packages
- Use `uv sync` to install from pyproject.toml
- Maintain a uv.lock file for reproducible builds

## Data Modeling Approaches

### Options Evaluated

1. **dataclasses**
   - Pros: Built-in to Python 3.7+, supports type hints, clean syntax
   - Cons: Limited validation compared to alternatives
   - Python 3.13 Compatibility: Full support

2. **Pydantic**
   - Pros: Rich validation, serialization, type conversion
   - Cons: Additional dependency, more complex for simple use cases
   - Python 3.13 Compatibility: Full support

3. **Simple dictionaries**
   - Pros: No dependencies, simple
   - Cons: No type safety, no validation, harder to maintain
   - Python 3.13 Compatibility: Full support

**Decision**: dataclasses are selected as they provide the right balance of type safety and simplicity for this use case.

## Project Structure

### Recommended Structure
The selected structure separates concerns clearly:
- Models: Data definitions and validation
- Services: Business logic and operations
- Repositories: Data access and storage logic
- CLI: User interface and command definitions

This follows clean architecture principles and makes testing easier.

## Summary of Decisions

1. **CLI Framework**: Typer
2. **Data Modeling**: dataclasses
3. **Package Manager**: uv
4. **Project Structure**: Modular with clear separation of concerns
5. **Testing Framework**: pytest (standard Python testing framework that works well with uv)