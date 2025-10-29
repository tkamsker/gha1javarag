#!/usr/bin/env python3
import sys
import logging

from src.utils.weaviate_client import WeaviateClient


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    client = WeaviateClient()
    if not client.client:
        logging.error("Weaviate not connected; aborting reset.")
        return 1

    collection_name = "FileExtraction"
    try:
        if client.client.collections.exists(collection_name):
            logging.info("Deleting existing collection: %s", collection_name)
            client.client.collections.delete(collection_name)
        logging.info("Recreating collection with vectorizer disabled: %s", collection_name)
        client._ensure_collection()
        logging.info("Collection reset completed.")
        return 0
    except Exception as e:
        logging.exception("Failed to reset collection: %s", e)
        return 2
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())


