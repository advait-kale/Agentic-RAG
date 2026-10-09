# Agentic RAG Email Assistant

A local email question-answering backend. It fetches recent Gmail messages, cleans and chunks their text, creates embeddings with Ollama, and stores them in Supabase with pgvector. The `/query` endpoint retrieves relevant email chunks and asks a local language model to answer from that context.

## Features

- Gmail access through Google OAuth using `simplegmail`.
- HTML cleanup and chunking of email content before indexing.
- Ollama embeddings (`qwen3-embedding:0.6b`) and chat (`qwen3:8b`) by default.
- Supabase Postgres with pgvector for vector storage and similarity search.
- FastAPI endpoint for questions over indexed emails.

The current implementation is a RAG application. It does not yet include an agent loop, email triage actions, or tools for sending or modifying email.

## How it works

```text
Gmail → clean and chunk messages → Ollama embeddings → Supabase/pgvector
Question → embed query → similarity search → Ollama answer
```

Email ingestion is implemented in `app/agents/tools/email_tool.py`. The Gmail client currently fetches messages from the last three days. Retrieval and answer generation are in `app/services/RAG.py` and `app/services/chat.py`.

## Requirements

- Windows, macOS, or Linux
- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/) with the models listed below
- A Supabase project with pgvector enabled
- A Google OAuth Desktop application credentials file for Gmail

Pull the default models with Ollama:

```bash
ollama pull qwen3:8b
ollama pull qwen3-embedding:0.6b
```

Keep Ollama running while using the application.

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the repository root with the required Supabase keys and email address:

   ```dotenv
   ANON_PUBLIC_KEY=your_supabase_anon_key
   SERVICE_ROLE=your_supabase_service_role_key
   EMAIL_ADDRESS=your_email_address
   ```

   `PROJECT_URL` can be set if you use a different Supabase project. The application currently has a default project URL in `app/config/settings.py`. Keep `.env` and all credentials out of version control.

3. Create the vector table and search function by running [`sql/init_supabase.sql`](sql/init_supabase.sql) in the Supabase SQL editor. The schema uses 1024-dimensional vectors, matching the default embedding model.

4. Set up Gmail OAuth:

   - Create/download a Google OAuth Desktop client credentials JSON file.
   - Put it in the repository root as `client_secret.json`.
   - The first Gmail access opens the OAuth consent flow and creates `gmail_token.json` in the root.

   Both files contain credentials and are ignored by Git. Add your Google account as a test user if the OAuth consent screen is in testing mode.

## Run

Start the API from the repository root:

```bash
uv run python run.py
```

The server listens at `http://127.0.0.1:8000`. Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

Ask a question using the `/query` query parameter:

```bash
curl -X POST "http://127.0.0.1:8000/query?query=Summarize%20recent%20internship%20emails%20and%20their%20due%20dates"
```

The endpoint returns the generated answer as a string. It requires indexed email data in Supabase and a running Ollama service.

## Index recent email

Run the seeding script from the repository root:

```bash
uv run -m app.agents.tools.email_tool
```

This fetches Gmail messages from the last three days, chunks and embeds them, then upserts the resulting records into `rag_chunks` in Supabase.

## Configuration

Model and service settings are defined in `app/config/settings.py` and can be supplied through `.env`:

| Setting | Default / source | Purpose |
|---|---|---|
| `LLM_MODEL` | `qwen3:8b` | Ollama chat model |
| `LLM_PROVIDER` | `ollama` | LangChain chat provider |
| `EMBEDDING_MODEL` | `qwen3-embedding:0.6b` | Ollama embedding model |
| `PROJECT_URL` | Set in `settings.py` | Supabase project URL |
| `ANON_PUBLIC_KEY` | Required in `.env` | Supabase public key |
| `SERVICE_ROLE` | Required in `.env` | Supabase service role key |
| `EMAIL_ADDRESS` | Required in `.env` | Email address setting |

Gmail OAuth filenames are currently passed to `simplegmail` using its default root-level filenames; the similarly named settings fields are not yet wired into `GmailAPI.py`.

## Project layout

```text
app/
  agents/tools/email_tool.py  Gmail-to-Supabase indexing pipeline
  config/settings.py          Environment-based settings
  services/
    RAG.py                     Retrieval and answer orchestration
    chat.py                    Ollama chat and response generation
    chunking.py                Email text splitting
    embeddings.py              Ollama embeddings
sql/
  database.py                  Supabase client, upsert, and vector search
  init_supabase.sql            pgvector table, RPC, and index
GmailAPI.py                    Gmail OAuth and message cleanup
run.py                         Uvicorn entry point
```

## Known limitations

- Only `POST /query` and Gmail indexing are currently implemented; there is no `/seed` API route.
- The answer endpoint collects the model stream and returns the completed answer; it does not stream an HTTP response.
- Gmail fetch window is currently fixed to three days in `GmailAPI.py`.
- Chunk IDs are randomly generated when indexing, so repeating a seed can create duplicate chunks for the same email.
- Local model downloads and external Gmail/Supabase credentials are needed; the prebuilt files under `dist/` are not a substitute for configuring these services.
