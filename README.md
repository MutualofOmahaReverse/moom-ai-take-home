# Mutual of Omaha Take Home Assessment

## Running it

```bash
docker compose up --build
```

That is the whole setup. No API key, no config file, nothing to sign up for.

- API: http://localhost:8000 (docs at `/docs`)
- Web: http://localhost:5173
- Postgres: `localhost:55432` (moved off 5432; most machines already have one)

The database seeds itself on first run with synthetic loan files and documents.
To reseed from scratch: `docker compose down -v && docker compose up --build`.

### About the API key

**You do not need one.** Classification and extraction run offline by default,
using keyword rules and regexes in `api/app/services/offline.py`. Every screen
works, the tests run, and nothing in the tickets requires a live model.

There is also a live path that calls the Anthropic API, used instead of the
offline one when `ANTHROPIC_API_KEY` is set. That is entirely optional and we
are not expecting it. The SDK code is there to be read and changed either way.
A fix to it is verified with a unit test, not with a network call.

### Tests

```bash
docker compose exec api pytest
```

---

## How it fits together

```
  web (React/TS, :5173)
        |
        v
  api (FastAPI, :8000)
        |
        +-- services/classifier.py   what kind of document is this
        +-- services/extractor.py    pull fields out of it
        +-- prompts.py               the prompt text for both
        |
        v
  db (Postgres, :5432)
        loan_file       one borrower's application
        document        a file uploaded against it, with its type + confidence
        extraction      fields pulled out of a document
        checklist_item  what a complete file needs, per product
```

The interesting endpoints:

| | |
|---|---|
| `GET /loans` | every loan file with a document count |
| `GET /loans/{id}/missing` | what that file is still missing |
| `POST /documents/{id}/classify` | classify one document |
| `POST /documents/classify-pending` | classify everything unclassified |
| `GET /admin/stats` | counts, useful for checking the seed worked |

## The data

Everything in the seed is synthetic. Every name, address, account number and
amount was made up for this exercise. There is no real borrower data anywhere in
this repository and there never should be.

---

## Your tickets

Sent separately by email. 

