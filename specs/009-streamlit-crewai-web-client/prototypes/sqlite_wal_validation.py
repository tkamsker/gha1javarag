#!/usr/bin/env python3
"""
SQLite WAL Mode Concurrency Validation Prototype

Purpose: Validate SQLite WAL mode can handle 50 concurrent writers with acceptable latency
Status: Phase 0 Research - Technical Feasibility Validation
"""

import sqlite3
import time
import statistics
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict


def create_test_database(db_path: Path) -> None:
    """Create test database with workspaces and annotations tables in WAL mode."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Enable WAL mode
    cursor.execute("PRAGMA journal_mode=WAL;")
    cursor.execute("PRAGMA busy_timeout=5000;")  # 5 seconds
    cursor.execute("PRAGMA synchronous=NORMAL;")  # Balance safety and performance

    # Create workspaces table (simplified schema)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS workspaces (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            state_json TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            artifact_count INTEGER DEFAULT 0
        )
    """)

    # Create index for performance
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_workspaces_updated_at
        ON workspaces(updated_at DESC)
    """)

    conn.commit()
    conn.close()

    print(f"✅ Created test database at {db_path}")
    print(f"✅ Enabled WAL mode with 5s busy timeout")


def write_workspace(db_path: Path, workspace_id: int, delay_ms: int = 0) -> Dict:
    """Simulate workspace write operation."""
    start_time = time.time()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Simulate some processing time
        if delay_ms > 0:
            time.sleep(delay_ms / 1000.0)

        # Insert workspace
        cursor.execute("""
            INSERT INTO workspaces (id, name, state_json, artifact_count)
            VALUES (?, ?, ?, ?)
        """, (
            f"workspace-{workspace_id}",
            f"Test Workspace {workspace_id}",
            f'{{"query": "test", "filters": {{}}}}',
            10
        ))

        conn.commit()
        conn.close()

        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": True,
            "workspace_id": workspace_id,
            "latency_ms": elapsed_ms
        }

    except sqlite3.OperationalError as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "workspace_id": workspace_id,
            "latency_ms": elapsed_ms,
            "error": str(e)
        }


def read_workspaces(db_path: Path, limit: int = 10) -> Dict:
    """Simulate concurrent read operation."""
    start_time = time.time()

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, name, artifact_count, updated_at
            FROM workspaces
            ORDER BY updated_at DESC
            LIMIT ?
        """, (limit,))

        results = cursor.fetchall()
        conn.close()

        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": True,
            "count": len(results),
            "latency_ms": elapsed_ms
        }

    except Exception as e:
        elapsed_ms = (time.time() - start_time) * 1000
        return {
            "success": False,
            "latency_ms": elapsed_ms,
            "error": str(e)
        }


def run_concurrent_test(db_path: Path, num_writers: int, num_readers: int) -> Dict:
    """Run concurrent write and read test."""
    print(f"\n[Test] {num_writers} concurrent writers, {num_readers} concurrent readers")

    write_results = []
    read_results = []

    with ThreadPoolExecutor(max_workers=num_writers + num_readers) as executor:
        # Submit write tasks
        write_futures = [
            executor.submit(write_workspace, db_path, i, delay_ms=10)
            for i in range(num_writers)
        ]

        # Submit read tasks (interleaved with writes)
        read_futures = [
            executor.submit(read_workspaces, db_path, limit=10)
            for _ in range(num_readers)
        ]

        # Collect write results
        for future in as_completed(write_futures):
            write_results.append(future.result())

        # Collect read results
        for future in as_completed(read_futures):
            read_results.append(future.result())

    # Calculate statistics
    write_latencies = [r["latency_ms"] for r in write_results if r["success"]]
    read_latencies = [r["latency_ms"] for r in read_results if r["success"]]

    write_failures = len([r for r in write_results if not r["success"]])
    read_failures = len([r for r in read_results if not r["success"]])

    return {
        "write_count": len(write_results),
        "write_success": len(write_latencies),
        "write_failures": write_failures,
        "write_latency_p50": statistics.median(write_latencies) if write_latencies else 0,
        "write_latency_p95": statistics.quantiles(write_latencies, n=20)[18] if len(write_latencies) >= 20 else max(write_latencies) if write_latencies else 0,
        "read_count": len(read_results),
        "read_success": len(read_latencies),
        "read_failures": read_failures,
        "read_latency_p50": statistics.median(read_latencies) if read_latencies else 0,
        "read_latency_p95": statistics.quantiles(read_latencies, n=20)[18] if len(read_latencies) >= 20 else max(read_latencies) if read_latencies else 0,
    }


def main():
    """Main entry point."""
    print("=" * 80)
    print("SQLite WAL Mode Concurrency Validation")
    print("=" * 80)

    # Create test database
    db_path = Path("specs/009-streamlit-crewai-web-client/prototypes/test_concurrency.db")
    db_path.parent.mkdir(parents=True, exist_ok=True)

    # Clean up old database
    if db_path.exists():
        db_path.unlink()

    create_test_database(db_path)

    # Run progressive concurrency tests
    test_scenarios = [
        {"writers": 10, "readers": 10},   # Light load
        {"writers": 25, "readers": 25},   # Medium load
        {"writers": 50, "readers": 50},   # Target load (50 concurrent users)
    ]

    all_results = []

    for scenario in test_scenarios:
        result = run_concurrent_test(
            db_path,
            scenario["writers"],
            scenario["readers"]
        )
        all_results.append({**scenario, **result})

        # Print results
        print(f"  Writes: {result['write_success']}/{result['write_count']} successful")
        print(f"  Write latency: p50={result['write_latency_p50']:.1f}ms, p95={result['write_latency_p95']:.1f}ms")
        print(f"  Reads: {result['read_success']}/{result['read_count']} successful")
        print(f"  Read latency: p50={result['read_latency_p50']:.1f}ms, p95={result['read_latency_p95']:.1f}ms")
        if result['write_failures'] > 0 or result['read_failures'] > 0:
            print(f"  ⚠️  Failures: {result['write_failures']} writes, {result['read_failures']} reads")
        print()

    # Final validation
    print("=" * 80)
    print("Validation Summary")
    print("=" * 80)

    target_scenario = all_results[-1]  # 50 concurrent users

    # Check against requirements
    write_p95_ok = target_scenario["write_latency_p95"] < 100  # <100ms target
    write_failure_ok = target_scenario["write_failures"] == 0
    read_p95_ok = target_scenario["read_latency_p95"] < 50  # <50ms target

    print(f"Target: 50 concurrent users (50 writers + 50 readers)")
    print()
    print("Results:")
    print(f"  Write p95 latency: {target_scenario['write_latency_p95']:.1f}ms (<100ms target)")
    print(f"  Status: {'✅ PASS' if write_p95_ok else '❌ FAIL'}")
    print(f"  Write failures: {target_scenario['write_failures']} (0 expected)")
    print(f"  Status: {'✅ PASS' if write_failure_ok else '❌ FAIL'}")
    print(f"  Read p95 latency: {target_scenario['read_latency_p95']:.1f}ms (<50ms target)")
    print(f"  Status: {'✅ PASS' if read_p95_ok else '❌ FAIL'}")
    print()

    if write_p95_ok and write_failure_ok and read_p95_ok:
        print("✅ SUCCESS - SQLite WAL mode can handle 50 concurrent users")
        print()
        print("Recommendation: PROCEED with SQLite WAL mode for workspaces/annotations")
        return 0
    else:
        print("❌ FAILED - SQLite WAL mode does not meet requirements")
        print()
        print("Recommendation: Consider alternatives (PostgreSQL, Redis) or reduce concurrency target")
        return 1

    # Cleanup
    # db_path.unlink()


if __name__ == "__main__":
    exit(main())
