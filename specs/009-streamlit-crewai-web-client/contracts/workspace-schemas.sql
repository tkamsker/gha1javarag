-- Workspace Schemas Contract
-- Feature: 009-streamlit-crewai-web-client
-- Version: 1.0.0
-- Date: 2026-01-14
--
-- This file defines the SQLite database schema for workspace and annotation storage.
-- All tables must be created with WAL mode enabled for concurrent access.
--
-- Usage:
--   sqlite3 data/workspaces.db < contracts/workspace-schemas.sql

-- ==============================================================================
-- Database Configuration
-- ==============================================================================

-- Enable Write-Ahead Logging (WAL) mode for concurrent reads/writes
PRAGMA journal_mode=WAL;

-- Set busy timeout to 5 seconds to handle lock contention
PRAGMA busy_timeout=5000;

-- Enable foreign key constraints
PRAGMA foreign_keys=ON;

-- Use synchronous=NORMAL for better performance with WAL mode
PRAGMA synchronous=NORMAL;

-- ==============================================================================
-- Workspaces Table
-- ==============================================================================

-- Stores saved workspace states for collaborative analysis sessions
CREATE TABLE IF NOT EXISTS workspaces (
    -- Primary key (UUID format)
    id TEXT PRIMARY KEY NOT NULL,

    -- Workspace metadata
    name TEXT NOT NULL,
    description TEXT,
    creator TEXT,  -- Username or email
    tags TEXT,     -- Comma-separated tags (e.g., "authentication,security,review")

    -- Workspace state (JSON blob)
    state_json TEXT NOT NULL,  -- Stores UI state: {query, filters, artifact_ids, agent_settings, notes}

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Constraints
    CHECK(length(name) >= 3 AND length(name) <= 200),
    CHECK(length(state_json) >= 2),  -- Minimum: "{}"
    CHECK(created_at <= updated_at)
);

-- ==============================================================================
-- Workspaces Indexes
-- ==============================================================================

-- Index for querying by creator
CREATE INDEX IF NOT EXISTS idx_workspaces_creator
    ON workspaces(creator);

-- Index for querying by most recent (descending order)
CREATE INDEX IF NOT EXISTS idx_workspaces_updated_at
    ON workspaces(updated_at DESC);

-- Index for tag-based queries (SQLite doesn't have array type, so we use LIKE)
CREATE INDEX IF NOT EXISTS idx_workspaces_tags
    ON workspaces(tags);

-- Full-text search index on workspace name and description
CREATE VIRTUAL TABLE IF NOT EXISTS workspaces_fts USING fts5(
    name,
    description,
    tags,
    content=workspaces,
    content_rowid=rowid
);

-- ==============================================================================
-- Workspaces Triggers
-- ==============================================================================

-- Automatically update updated_at timestamp on modification
CREATE TRIGGER IF NOT EXISTS update_workspace_timestamp
AFTER UPDATE ON workspaces
FOR EACH ROW
BEGIN
    UPDATE workspaces
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Keep FTS index in sync with workspaces table
CREATE TRIGGER IF NOT EXISTS workspaces_fts_insert
AFTER INSERT ON workspaces
BEGIN
    INSERT INTO workspaces_fts(rowid, name, description, tags)
    VALUES (new.rowid, new.name, new.description, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS workspaces_fts_update
AFTER UPDATE ON workspaces
BEGIN
    UPDATE workspaces_fts
    SET name = new.name,
        description = new.description,
        tags = new.tags
    WHERE rowid = new.rowid;
END;

CREATE TRIGGER IF NOT EXISTS workspaces_fts_delete
AFTER DELETE ON workspaces
BEGIN
    DELETE FROM workspaces_fts WHERE rowid = old.rowid;
END;

-- ==============================================================================
-- Annotations Table
-- ==============================================================================

-- Stores user annotations (notes and tags) on artifacts
CREATE TABLE IF NOT EXISTS annotations (
    -- Primary key (UUID format)
    id TEXT PRIMARY KEY NOT NULL,

    -- Artifact reference
    artifact_id TEXT NOT NULL,  -- Weaviate artifact UUID
    artifact_type TEXT,         -- Optional: artifact type for display (DaoCall, GwtPresenter, etc.)

    -- Annotation content
    note TEXT,                  -- Markdown-formatted note
    tags TEXT,                  -- Comma-separated tags (e.g., "bug,needs-review,security")

    -- Metadata
    author TEXT NOT NULL,       -- Username or email
    visibility TEXT DEFAULT 'shared' CHECK(visibility IN ('private', 'shared', 'public')),

    -- Timestamps
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Constraints
    CHECK(length(artifact_id) > 0),
    CHECK(note IS NOT NULL OR tags IS NOT NULL),  -- At least one of note/tags required
    CHECK(created_at <= updated_at)
);

-- ==============================================================================
-- Annotations Indexes
-- ==============================================================================

-- Index for querying by artifact_id (most common query)
CREATE INDEX IF NOT EXISTS idx_annotations_artifact_id
    ON annotations(artifact_id);

-- Index for querying by author
CREATE INDEX IF NOT EXISTS idx_annotations_author
    ON annotations(author);

-- Index for querying by tags
CREATE INDEX IF NOT EXISTS idx_annotations_tags
    ON annotations(tags);

-- Index for querying by visibility
CREATE INDEX IF NOT EXISTS idx_annotations_visibility
    ON annotations(visibility);

-- Composite index for artifact_id + visibility (common filter)
CREATE INDEX IF NOT EXISTS idx_annotations_artifact_visibility
    ON annotations(artifact_id, visibility);

-- Full-text search index on annotation notes and tags
CREATE VIRTUAL TABLE IF NOT EXISTS annotations_fts USING fts5(
    note,
    tags,
    content=annotations,
    content_rowid=rowid
);

-- ==============================================================================
-- Annotations Triggers
-- ==============================================================================

-- Automatically update updated_at timestamp on modification
CREATE TRIGGER IF NOT EXISTS update_annotation_timestamp
AFTER UPDATE ON annotations
FOR EACH ROW
BEGIN
    UPDATE annotations
    SET updated_at = CURRENT_TIMESTAMP
    WHERE id = NEW.id;
END;

-- Keep FTS index in sync with annotations table
CREATE TRIGGER IF NOT EXISTS annotations_fts_insert
AFTER INSERT ON annotations
BEGIN
    INSERT INTO annotations_fts(rowid, note, tags)
    VALUES (new.rowid, new.note, new.tags);
END;

CREATE TRIGGER IF NOT EXISTS annotations_fts_update
AFTER UPDATE ON annotations
BEGIN
    UPDATE annotations_fts
    SET note = new.note,
        tags = new.tags
    WHERE rowid = new.rowid;
END;

CREATE TRIGGER IF NOT EXISTS annotations_fts_delete
AFTER DELETE ON annotations
BEGIN
    DELETE FROM annotations_fts WHERE rowid = old.rowid;
END;

-- ==============================================================================
-- Workspace-Artifact Junction Table
-- ==============================================================================

-- Many-to-many relationship: workspaces can contain multiple artifacts,
-- artifacts can appear in multiple workspaces
CREATE TABLE IF NOT EXISTS workspace_artifacts (
    -- Composite primary key
    workspace_id TEXT NOT NULL,
    artifact_id TEXT NOT NULL,

    -- Metadata
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    added_by TEXT,  -- User who added this artifact to workspace

    -- Foreign key constraints
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE CASCADE,

    PRIMARY KEY (workspace_id, artifact_id)
);

-- ==============================================================================
-- Workspace-Artifact Indexes
-- ==============================================================================

-- Index for querying artifacts in a workspace
CREATE INDEX IF NOT EXISTS idx_workspace_artifacts_workspace
    ON workspace_artifacts(workspace_id);

-- Index for finding workspaces containing an artifact
CREATE INDEX IF NOT EXISTS idx_workspace_artifacts_artifact
    ON workspace_artifacts(artifact_id);

-- ==============================================================================
-- Export History Table
-- ==============================================================================

-- Tracks export operations for audit and cleanup
CREATE TABLE IF NOT EXISTS export_history (
    -- Primary key
    id TEXT PRIMARY KEY NOT NULL,

    -- Export metadata
    workspace_id TEXT,  -- Optional: export from workspace
    export_type TEXT NOT NULL CHECK(export_type IN ('markdown', 'pdf', 'json', 'csv', 'gherkin', 'playwright')),
    file_path TEXT NOT NULL,
    file_size_bytes INTEGER,

    -- User context
    created_by TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,

    -- Cleanup
    expires_at TIMESTAMP,  -- Exports deleted after expiration (default: 24h)
    deleted_at TIMESTAMP,  -- NULL until file deleted

    -- Foreign key constraints
    FOREIGN KEY (workspace_id) REFERENCES workspaces(id) ON DELETE SET NULL
);

-- ==============================================================================
-- Export History Indexes
-- ==============================================================================

-- Index for cleanup job (find expired exports)
CREATE INDEX IF NOT EXISTS idx_export_history_expires
    ON export_history(expires_at)
    WHERE deleted_at IS NULL;

-- Index for user export history
CREATE INDEX IF NOT EXISTS idx_export_history_user
    ON export_history(created_by, created_at DESC);

-- ==============================================================================
-- Views for Common Queries
-- ==============================================================================

-- View: Workspaces with artifact counts
CREATE VIEW IF NOT EXISTS workspaces_with_counts AS
SELECT
    w.id,
    w.name,
    w.description,
    w.creator,
    w.tags,
    w.created_at,
    w.updated_at,
    COUNT(wa.artifact_id) AS artifact_count
FROM workspaces w
LEFT JOIN workspace_artifacts wa ON w.id = wa.workspace_id
GROUP BY w.id;

-- View: Annotations with artifact details
CREATE VIEW IF NOT EXISTS annotations_with_artifacts AS
SELECT
    a.id,
    a.artifact_id,
    a.artifact_type,
    a.note,
    a.tags,
    a.author,
    a.visibility,
    a.created_at,
    a.updated_at
FROM annotations a;

-- View: Recent activity (last 100 workspace updates or annotations)
CREATE VIEW IF NOT EXISTS recent_activity AS
SELECT
    'workspace_update' AS activity_type,
    w.id AS entity_id,
    w.name AS entity_name,
    w.creator AS user,
    w.updated_at AS timestamp
FROM workspaces w
UNION ALL
SELECT
    'annotation_create' AS activity_type,
    a.id AS entity_id,
    a.artifact_id AS entity_name,
    a.author AS user,
    a.created_at AS timestamp
FROM annotations a
ORDER BY timestamp DESC
LIMIT 100;

-- ==============================================================================
-- Sample Data (for testing/development)
-- ==============================================================================

-- Uncomment to insert sample workspace
-- INSERT INTO workspaces (id, name, creator, state_json, tags)
-- VALUES (
--     'ws-sample-001',
--     'Authentication Module Review',
--     'dev@example.com',
--     '{"query": "user authentication", "filters": {"artifact_type": ["DaoCall", "GwtPresenter"]}, "artifact_ids": ["uuid1", "uuid2"]}',
--     'authentication,security,review'
-- );

-- Uncomment to insert sample annotation
-- INSERT INTO annotations (id, artifact_id, artifact_type, note, tags, author, visibility)
-- VALUES (
--     'ann-sample-001',
--     'artifact-uuid-123',
--     'GwtPresenter',
--     '# Security Issue\n\nThis presenter lacks input validation on the login form.',
--     'security,bug,needs-fix',
--     'dev@example.com',
--     'shared'
-- );

-- ==============================================================================
-- Validation Queries
-- ==============================================================================

-- Check table structure
-- SELECT name, sql FROM sqlite_master WHERE type='table' AND name IN ('workspaces', 'annotations', 'workspace_artifacts', 'export_history');

-- Check indexes
-- SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index' AND tbl_name IN ('workspaces', 'annotations', 'workspace_artifacts', 'export_history');

-- Check triggers
-- SELECT name, tbl_name, sql FROM sqlite_master WHERE type='trigger' AND tbl_name IN ('workspaces', 'annotations');

-- Verify WAL mode enabled
-- PRAGMA journal_mode;  -- Should return 'wal'

-- ==============================================================================
-- Migration Support
-- ==============================================================================

-- Version tracking table for schema migrations
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY NOT NULL,
    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
    description TEXT
);

-- Insert initial schema version
INSERT OR IGNORE INTO schema_version (version, description)
VALUES (1, 'Initial schema with workspaces, annotations, and export history');

-- ==============================================================================
-- Cleanup Jobs
-- ==============================================================================

-- Query to find expired exports (run daily via cron)
-- DELETE FROM export_history
-- WHERE expires_at < CURRENT_TIMESTAMP AND deleted_at IS NULL;

-- Query to vacuum database (reclaim disk space after deletions)
-- VACUUM;

-- ==============================================================================
-- End of Schema
-- ==============================================================================
