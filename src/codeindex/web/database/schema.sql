-- ============================================================================
-- Feature 009: SQLite Database Schema
-- ============================================================================
-- Database schema for workspaces and annotations with full-text search
-- Uses WAL mode for concurrency (configured in connection.py)

-- ============================================================================
-- Workspaces Table
-- ============================================================================
-- Stores saved UI states for collaborative analysis
CREATE TABLE IF NOT EXISTS workspaces (
    -- Primary Key
    id TEXT PRIMARY KEY,                    -- UUID (e.g., 'workspace-abc123')

    -- Metadata
    name TEXT NOT NULL,                     -- User-defined name
    creator TEXT,                           -- Username or email (optional if no auth)
    description TEXT,                       -- Optional description

    -- State Snapshot
    state_json TEXT NOT NULL,               -- JSON blob with UI state

    -- Tags and Categories
    tags TEXT,                              -- Comma-separated tags
    category TEXT,                          -- Optional category

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_accessed_at TIMESTAMP,             -- Track usage frequency

    -- Statistics
    artifact_count INTEGER DEFAULT 0,       -- Number of artifacts in workspace
    view_count INTEGER DEFAULT 0            -- Number of times workspace loaded
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_workspaces_creator ON workspaces(creator);
CREATE INDEX IF NOT EXISTS idx_workspaces_tags ON workspaces(tags);
CREATE INDEX IF NOT EXISTS idx_workspaces_updated_at ON workspaces(updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_workspaces_last_accessed ON workspaces(last_accessed_at DESC);

-- ============================================================================
-- Annotations Table
-- ============================================================================
-- Stores user-generated notes and tags for artifacts
CREATE TABLE IF NOT EXISTS annotations (
    -- Primary Key
    id TEXT PRIMARY KEY,                    -- UUID (e.g., 'annotation-xyz789')

    -- Artifact Reference
    artifact_id TEXT NOT NULL,              -- Weaviate artifact UUID
    artifact_type TEXT,                     -- Optional: DaoCall, GwtPresenter, etc.

    -- Content
    note TEXT,                              -- User note (plain text or Markdown)
    tags TEXT,                              -- Comma-separated tags

    -- Metadata
    author TEXT,                            -- Username or email (optional if no auth)
    visibility TEXT DEFAULT 'shared',       -- 'shared' or 'private' (future enhancement)

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Version Tracking (future enhancement)
    version INTEGER DEFAULT 1,
    edited_by TEXT                          -- Last editor (if different from author)
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_annotations_artifact_id ON annotations(artifact_id);
CREATE INDEX IF NOT EXISTS idx_annotations_author ON annotations(author);
CREATE INDEX IF NOT EXISTS idx_annotations_tags ON annotations(tags);
CREATE INDEX IF NOT EXISTS idx_annotations_updated_at ON annotations(updated_at DESC);

-- ============================================================================
-- Full-Text Search Index for Annotations
-- ============================================================================
-- SQLite FTS5 virtual table for fast note search
CREATE VIRTUAL TABLE IF NOT EXISTS annotations_fts USING fts5(
    artifact_id,
    note,
    tags,
    content='annotations',
    content_rowid='rowid'
);

-- Triggers to keep FTS index in sync with annotations table
CREATE TRIGGER IF NOT EXISTS annotations_ai AFTER INSERT ON annotations BEGIN
    INSERT INTO annotations_fts(rowid, artifact_id, note, tags)
    VALUES (new.rowid, new.artifact_id, new.note, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS annotations_au AFTER UPDATE ON annotations BEGIN
    UPDATE annotations_fts SET
        artifact_id = new.artifact_id,
        note = new.note,
        tags = new.tags
    WHERE rowid = old.rowid;
END;

CREATE TRIGGER IF NOT EXISTS annotations_ad AFTER DELETE ON annotations BEGIN
    DELETE FROM annotations_fts WHERE rowid = old.rowid;
END;

-- ============================================================================
-- Views for Common Queries
-- ============================================================================

-- Recent workspaces view
CREATE VIEW IF NOT EXISTS recent_workspaces AS
SELECT
    id,
    name,
    creator,
    tags,
    artifact_count,
    view_count,
    last_accessed_at,
    updated_at
FROM workspaces
ORDER BY last_accessed_at DESC
LIMIT 50;

-- Annotation counts by artifact
CREATE VIEW IF NOT EXISTS annotation_counts AS
SELECT
    artifact_id,
    artifact_type,
    COUNT(*) as annotation_count,
    MAX(updated_at) as last_updated
FROM annotations
GROUP BY artifact_id, artifact_type;

-- ============================================================================
-- Utility Functions (SQLite doesn't have user-defined functions in schema,
-- these are implemented in Python connection.py)
-- ============================================================================
-- generate_uuid() - Generate UUID for new workspace/annotation
-- current_timestamp() - Get current timestamp
-- json_validate(json_text) - Validate JSON before storing in state_json
