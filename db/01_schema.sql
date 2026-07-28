-- Loan intake triage schema.
--
-- A "file" is one borrower's application. Documents arrive against it over
-- days, get classified, and a few fields get pulled out of each one. The
-- checklist says what a complete file needs.

CREATE TABLE loan_file (
    id              SERIAL PRIMARY KEY,
    reference       TEXT NOT NULL UNIQUE,   -- LF-xxxxx, what humans say out loud
    borrower_name   TEXT NOT NULL,
    product         TEXT,                   -- 'reverse' | 'forward' | null if unknown
    opened_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    status          TEXT                    -- see the note in 02_seed.sql
);

CREATE TABLE document (
    id              SERIAL PRIMARY KEY,
    loan_file_id    INTEGER NOT NULL REFERENCES loan_file(id),
    filename        TEXT NOT NULL,
    content         TEXT NOT NULL,          -- extracted text; no binaries in this fixture
    uploaded_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    doc_type        TEXT,                   -- set by the classifier, null until classified
    confidence      TEXT,                   -- TODO(dmr): this should be numeric, see #  -- left as-is for now
    classified_at   TIMESTAMPTZ
);

CREATE TABLE extraction (
    id              SERIAL PRIMARY KEY,
    document_id     INTEGER NOT NULL REFERENCES document(id),
    field_name      TEXT NOT NULL,
    field_value     TEXT,
    extracted_at    TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- What a complete file needs, per product. Rows here drive the missing-doc report.
CREATE TABLE checklist_item (
    id              SERIAL PRIMARY KEY,
    product         TEXT NOT NULL,
    doc_type        TEXT NOT NULL,
    required        BOOLEAN NOT NULL DEFAULT true,
    UNIQUE (product, doc_type)
);

CREATE INDEX ON document (loan_file_id);
CREATE INDEX ON extraction (document_id);
