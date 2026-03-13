# Automated Daily Standup Generator

A Python CLI tool designed to fetch your recent GitHub commits and Pull Requests, and leverage an LLM (OpenAI) to automatically generate a clean, readable daily standup report.

## Why this exists
Writing daily standup updates manually is repetitive. This tool automatically pulls what you *actually* did from Git history and uses AI to summarize it into plain English, saving time for Software Engineers, SREs, and DevOps professionals.

## Tech Stack
*   **Language:** Python 3
*   **CLI Framework:** Click
*   **Integrations:** PyGithub (GitHub REST API), OpenAI API

## Setup & Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/your-username/standup-generator.git
   cd standup-generator
   ```

2. **Set up a Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Rename `.env.example` to `.env` and add your keys:
   *   `GITHUB_TOKEN`: A GitHub Personal Access Token (PAT) with `repo` scope.
   *   `OPENAI_API_KEY`: An OpenAI Developer API key.

## Usage

Run the CLI tool from the root directory:

```bash
# Generate a standup for the last 24 hours (default)
python3 src/cli.py generate

# Generate a standup for the last 7 days
python3 src/cli.py generate --days 7
```

## Example Output
```text
Initializing Standup Generator for user: shammeesala
----------------------------------------
Fetching commits since 2024-03-12...
Fetching PRs since 2024-03-12...

--- Generated Standup Report ---

* Implemented automatic GitHub Username detection using the provided PAT token.
* Built the core LLM Summarization module utilizing `gpt-3.5-turbo`.
* Created the Click CLI interface with error handling and environment validation.

----------------------------------------
Done! Have a great standup.
```
