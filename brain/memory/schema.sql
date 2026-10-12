-- Jarvis memory schema
CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    email TEXT,
    role TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    status TEXT DEFAULT 'active',
    owner_id INTEGER REFERENCES people(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS preferences (
    id INTEGER PRIMARY KEY,
    key TEXT UNIQUE NOT NULL,
    value TEXT NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS decisions (
    id INTEGER PRIMARY KEY,
    context TEXT NOT NULL,
    decision TEXT NOT NULL,
    outcome TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS pending (
    id INTEGER PRIMARY KEY,
    content TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY,
    text TEXT NOT NULL,
    embedding BLOB NOT NULL,
    table_name TEXT,
    row_id INTEGER
);

CREATE INDEX IF NOT EXISTS idx_decisions_context ON decisions(context);
CREATE INDEX IF NOT EXISTS idx_pending_status ON pending(status);
