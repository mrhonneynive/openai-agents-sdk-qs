# OpenAI Agents SDK Quickstart

A succinct quickstart project demonstrating the OpenAI Agents SDK with `uv`.

## Prerequisites

- [uv](https://docs.astral.sh/uv/) installed.

## Setup

1. **Clone the repository.**
2. **Create and activate a virtual environment:**
   ```bash
   uv venv
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   uv sync
   ```
4. **Configure environment:**
   Copy `.env.example` to `.env` and add your OpenAI API key:
   ```bash
   cp .env.example .env
   ```

## Run

Run the main script:
```bash
uv run main.py
```
