#!/usr/bin/env python3
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

# Ensure project root is on sys.path when running as a script
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.config import Config
from src.utils.weaviate_client import WeaviateClient
from src.utils.logger import setup_logger

logger = setup_logger("diagnose_weaviate")


def read_fallback_counts(project: str) -> dict:
    """Read fallback file and return stats for the project and overall."""
    fallback_path = Config.BUILD_DIR / "step1_extracted_data.json"
    stats = {
        "fallback_file_exists": fallback_path.exists(),
        "fallback_total_projects": 0,
        "fallback_total_files": 0,
        "fallback_project_files": 0,
        "fallback_path": str(fallback_path),
    }
    if not fallback_path.exists():
        return stats

    try:
        data = json.loads(fallback_path.read_text(encoding="utf-8"))
        stats["fallback_total_projects"] = len(data)
        stats["fallback_total_files"] = sum(len(files or []) for files in data.values())
        stats["fallback_project_files"] = len(data.get(project, []))
        return stats
    except Exception as e:
        logger.warning(f"Could not parse fallback file {fallback_path}: {e}")
        return stats


def list_projects_in_weaviate(wc: WeaviateClient, sample_limit: int = 10000) -> Counter:
    """Fetch all objects (best-effort) and count by project."""
    try:
        collection = wc.client.collections.get("FileExtraction", timeout=5.0)
        try:
            results = collection.query.fetch_objects(limit=sample_limit, timeout=10.0)
        except Exception:
            return Counter()
        counter = Counter()
        for obj in getattr(results, "objects", []) or []:
            proj = obj.properties.get("project")
            if proj:
                counter[proj] += 1
        return counter
    except Exception:
        return Counter()


def fetch_project_files(wc: WeaviateClient, project: str, limit_preview: int = 10) -> list:
    files = wc.query_by_project(project)
    if limit_preview and len(files) > limit_preview:
        return files[:limit_preview]
    return files


def main():
    parser = argparse.ArgumentParser(description="Diagnose why Step 2 found no files in Weaviate for a project.")
    parser.add_argument("--project", default="cuco-ui-cct-common", help="Project identifier to check")
    parser.add_argument("--preview", type=int, default=10, help="How many file entries to preview")
    args = parser.parse_args()

    print("== Weaviate Diagnostics ==")
    print(f"WEAVIATE_URL: {Config.WEAVIATE_URL}")

    wc = WeaviateClient()

    is_connected = bool(getattr(wc, "client", None))
    print(f"Connected: {is_connected}")

    # Try to verify collection exists and vectorizer setting
    collection_ok = False
    vectorizer = "unknown"
    try:
        import httpx
        resp = httpx.get(f"{wc.base_url}/v1/schema/FileExtraction", timeout=5.0)
        if resp.status_code == 200:
            schema = resp.json()
            collection_ok = True
            vectorizer = schema.get("vectorizer", "unknown")
        elif resp.status_code == 404:
            collection_ok = False
        else:
            print(f"Unexpected schema status: {resp.status_code}")
    except Exception as e:
        print(f"Schema check failed: {e}")

    print(f"Collection exists: {collection_ok}")
    print(f"Vectorizer: {vectorizer}")

    # Count projects in Weaviate
    project_counts = Counter()
    if is_connected and collection_ok:
        project_counts = list_projects_in_weaviate(wc)
    top_projects = project_counts.most_common(10)
    total_objects = sum(project_counts.values())

    print(f"Total objects in Weaviate: {total_objects}")
    if top_projects:
        print("Top projects by object count:")
        for proj, cnt in top_projects:
            print(f"  - {proj}: {cnt}")
    else:
        print("No objects returned or unable to query all.")

    # Query target project
    print("")
    print(f"== Project Probe: {args.project} ==")
    files_preview = fetch_project_files(wc, args.project, args.preview)
    project_weaviate_count = len(files_preview)
    # If we previewed fewer than actual, also report full count best-effort
    full_count_estimate = project_counts.get(args.project, project_weaviate_count)

    print(f"Weaviate files (preview): {project_weaviate_count}")
    print(f"Weaviate files (estimated total): {full_count_estimate}")
    if files_preview:
        print("Sample filePaths:")
        for f in files_preview:
            print(f"  - {f.get('filePath')}")

    # Fallback comparison
    print("")
    print("== Fallback Data (Step 1) ==")
    fb_stats = read_fallback_counts(args.project)
    for k, v in fb_stats.items():
        print(f"{k}: {v}")

    # Simple guidance based on findings
    print("")
    print("== Heuristics ==")
    if not is_connected or not collection_ok:
        print("- Weaviate not reachable or collection missing. Expect fallback to be used.")
    elif vectorizer != "none":
        print("- Collection vectorizer is not 'none'. Recreate with vectorizer=none to avoid embedding calls.")
    elif full_count_estimate == 0 and fb_stats.get("fallback_project_files", 0) > 0:
        print("- No Weaviate objects for project, but fallback has files. Likely ingestion didn’t store objects or project name mismatch.")
    elif full_count_estimate > 0:
        print("- Weaviate has objects for project. Investigate Step 2 retrieval/matching logic.")
    else:
        print("- Insufficient data to determine cause.")

    wc.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
