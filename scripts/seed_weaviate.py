#!/usr/bin/env python3
import argparse
import json
import random
import string
import sys
from pathlib import Path
from typing import Dict, Optional, List

# Ensure project root is on sys.path when running as a script
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from src.config import Config
from src.utils.logger import setup_logger

logger = setup_logger("seed_weaviate")


def _rand_name(prefix: str = "Test", length: int = 6) -> str:
    letters = string.ascii_letters + string.digits
    return f"{prefix}{''.join(random.choice(letters) for _ in range(length))}"


def ensure_collection(vectorizer: str, recreate: bool = False) -> None:
    """Ensure FileExtraction collection exists with desired vectorizer."""
    base = Config.WEAVIATE_URL.rstrip('/')
    name = "FileExtraction"

    try:
        resp = httpx.get(f"{base}/v1/schema/{name}", timeout=5.0)
        if resp.status_code == 200:
            existing = resp.json()
            existing_vec = existing.get("vectorizer")
            if recreate and existing_vec != vectorizer:
                httpx.delete(f"{base}/v1/schema/{name}", timeout=10.0)
                logger.info(f"Deleted existing {name} to recreate with vectorizer={vectorizer}")
            else:
                if existing_vec != vectorizer:
                    logger.warning(f"Collection exists with vectorizer={existing_vec}. Use --recreate to change to {vectorizer}.")
                return
        elif resp.status_code not in (404,):
            logger.warning(f"Unexpected status fetching schema: {resp.status_code}")
    except Exception as e:
        logger.warning(f"Schema check failed: {e}")

    # Create
    schema = {
        "class": name,
        "description": "File extraction storage",
        "vectorizer": vectorizer,
        "properties": [
            {"name": "filePath", "dataType": ["text"]},
            {"name": "project", "dataType": ["text"]},
            {"name": "fileType", "dataType": ["text"]},
            {"name": "extractedInfo", "dataType": ["text"]},
            {"name": "metadata", "dataType": ["text"]},
            {"name": "processed", "dataType": ["boolean"]},
        ],
    }
    create = httpx.post(f"{base}/v1/schema", json=schema, timeout=15.0)
    if create.status_code not in (200, 201):
        raise RuntimeError(f"Failed to create collection: {create.status_code} {create.text}")


def embed_text_ollama(text: str) -> Optional[List[float]]:
    """Generate an embedding via Ollama embeddings API."""
    try:
        url = f"{Config.OLLAMA_BASE_URL.rstrip('/')}/api/embeddings"
        payload = {"model": Config.OLLAMA_EMBED_MODEL_NAME, "prompt": text}
        resp = httpx.post(url, json=payload, timeout=30.0)
        if resp.status_code != 200:
            logger.warning(f"Embedding request failed: {resp.status_code} {resp.text}")
            return None
        data = resp.json()
        vec = data.get("embedding") or data.get("data", [{}])[0].get("embedding")
        if isinstance(vec, list) and vec:
            return vec
        return None
    except Exception as e:
        logger.warning(f"Embedding exception: {e}")
        return None


def insert_object(props: Dict, vector: Optional[List[float]] = None) -> str:
    """Insert object via REST. Tries vectors then falls back to vector."""
    base = Config.WEAVIATE_URL.rstrip('/')
    payload = {"class": "FileExtraction", "properties": props}

    # Try with vectors structure (newer API)
    if vector:
        payload_with_vectors = dict(payload)
        payload_with_vectors["vectors"] = {"default": vector}
        r = httpx.post(f"{base}/v1/objects", json=payload_with_vectors, timeout=15.0)
        if r.status_code in (200, 201):
            return r.json().get("id", "")
        # Fallback to legacy 'vector'
        payload_with_vector = dict(payload)
        payload_with_vector["vector"] = vector
        r = httpx.post(f"{base}/v1/objects", json=payload_with_vector, timeout=15.0)
        if r.status_code in (200, 201):
            return r.json().get("id", "")
        raise RuntimeError(f"Insert failed with vectors and vector fields: {r.status_code} {r.text}")

    # No vector provided
    r = httpx.post(f"{base}/v1/objects", json=payload, timeout=15.0)
    if r.status_code in (200, 201):
        return r.json().get("id", "")
    raise RuntimeError(f"Insert failed: {r.status_code} {r.text}")


def build_props(project: str, idx: int) -> Dict:
    cls = _rand_name("TestCls")
    file_path = f"infra/cuco/administration.ui/src/main/java/{cls}{idx}.java"
    extracted = {
        "classes": [
            {"name": cls, "methods": [{"name": "m1", "params": []}]}
        ],
        "extractionStatus": "complete",
    }
    return {
        "filePath": file_path,
        "project": project,
        "fileType": "java",
        "extractedInfo": json.dumps(extracted),
        "metadata": "{}",
        "processed": True,
    }


def main():
    parser = argparse.ArgumentParser(description="Seed Weaviate with test objects and control vectorization/embedding.")
    parser.add_argument("--project", default="cuco-ui-cct-common", help="Target project name")
    parser.add_argument("--count", type=int, default=5, help="Number of objects to insert")
    parser.add_argument("--vectorizer", choices=["none", "text2vec-ollama"], default="none", help="Collection vectorizer mode")
    parser.add_argument("--recreate", action="store_true", help="Delete and recreate collection if needed")
    parser.add_argument("--embed", action="store_true", help="Generate embeddings via Ollama and attach vector (useful when vectorizer=none)")
    parser.add_argument("--embed-text", default="filePath fileType extractedInfo", help="Fields to concatenate for embedding text")
    args = parser.parse_args()

    print("== Seeding Weaviate ==")
    print(f"WEAVIATE_URL: {Config.WEAVIATE_URL}")
    print(f"Vectorizer: {args.vectorizer} | Recreate: {args.recreate} | Embed: {args.embed}")

    ensure_collection(args.vectorizer, recreate=args.recreate)

    inserted = []
    for i in range(args.count):
        props = build_props(args.project, i)

        vector: Optional[List[float]] = None
        if args.embed:
            # Build text to embed
            parts: List[str] = []
            for field in args.embed_text.split():
                val = props.get(field)
                if isinstance(val, str):
                    parts.append(val)
            text = "\n".join(parts)
            vector = embed_text_ollama(text)

        uid = insert_object(props, vector=vector)
        inserted.append(uid)
        print(f"Inserted: {uid} -> {props['filePath']}")

    print(f"Done. Inserted {len(inserted)} objects into FileExtraction.")


if __name__ == "__main__":
    sys.exit(main())
