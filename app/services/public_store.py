from typing import Any
from uuid import uuid4

STORE: dict[str, dict[str, dict[str, Any]]] = {
    "files": {},
    "resumes": {},
    "jobs": {},
    "companies": {},
    "history": {},
}


def create_record(bucket: str, data: dict[str, Any]) -> dict[str, Any]:
    record_id = uuid4().hex
    record = {"id": record_id, **data}
    STORE.setdefault(bucket, {})[record_id] = record
    return record


def get_record(bucket: str, record_id: str) -> dict[str, Any] | None:
    return STORE.setdefault(bucket, {}).get(record_id)


def list_records(bucket: str) -> list[dict[str, Any]]:
    return list(STORE.setdefault(bucket, {}).values())


def update_record(bucket: str, record_id: str, data: dict[str, Any]) -> dict[str, Any] | None:
    existing = get_record(bucket, record_id)
    if existing is None:
        return None
    existing.update(data)
    return existing


def delete_record(bucket: str, record_id: str) -> bool:
    return STORE.setdefault(bucket, {}).pop(record_id, None) is not None

