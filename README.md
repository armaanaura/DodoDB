# DodoDB

DodoDB is a small database project built from scratch in Python for learning database internals in a disciplined way.

The goal of this project is not to build a production database immediately. The goal is to understand how databases work by implementing the core pieces step by step, starting from a minimal in-memory design and growing it over time.

## Project Goals

- learn database internals by building them directly
- start with a small and correct in-memory database
- avoid unnecessary complexity in the early versions
- focus on clean design, correctness, and testing
- evolve the system gradually toward more advanced features

## Current Scope

The current version focuses on the most basic database components:

- database object
- table creation
- table management
- schema-related design foundations

This project intentionally does not start with SQL parsing, distributed systems, replication, query optimization, or other advanced database features.

## Design Philosophy

This project follows a strict learning-first engineering approach:

- build the smallest correct version first
- keep the architecture simple
- avoid over-engineering
- implement features only when the previous layer is stable
- prioritize clarity over premature optimization

## Planned Evolution

The project is expected to grow in stages such as:

1. in-memory database core
2. schema validation
3. row insertion and scanning
4. filtering, update, and delete operations
5. persistence to disk
6. indexing
7. query language support
8. more advanced storage-engine concepts

## Tech Stack

- Python
- Rust (potentially for performance-critical components in the future)

## Setup

### Prerequisites

- Python 3.11 or later recommended
- Git

### Clone the repository

```bash
git clone git@github.com:armaanaura/DodoDB.git
cd DodoDB
````

### Create a virtual environment

```bash
python -m venv venv
```

### Activate the virtual environment

#### On Windows

```bash
venv\Scripts\activate
```

#### On macOS/Linux

```bash
source venv/bin/activate
```

### Install dependencies

If you are using only the Python standard library for now, there may be nothing to install yet.

If you add testing tools like `pytest`, install them with:

```bash
pip install pytest
```

You can also later maintain a `requirements.txt` file and install with:

```bash
pip install -r requirements.txt
```

## Running the Project

Once the project has an entry file, you can run it like this:

```bash
python main.py
```

## Running Tests

If you are using `pytest`, run:

```bash
pytest
```

## Purpose

This project is primarily for deep learning and experimentation with database internals. It is being built as an educational system, with the intention of understanding real database design decisions through implementation.

## Status

Early development.

## Author

Armaan
armaanaurapvt@gmail.com

