from __future__ import annotations
from typing import Optional, Union
from pathlib import Path
import mimetypes
import os

from supabase import create_client, Client
from django.conf import settings

def _client() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase credentials not configured")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)

def create_signed_url(bucket: str, path: str, expires_in: Optional[int] = None) -> str:
    """
    Return a signed URL for private file access.
    """
    exp = expires_in or settings.SUPABASE_SIGNED_URL_EXP_SECONDS
    res = _client().storage.from_(bucket).create_signed_url(path=path, expires_in=exp)
    if "signedURL" in res:
        return res["signedURL"]  # supabase-py v2 returns dict
    # fallback key names
    return res.get("signed_url") or res.get("signedUrl") or res.get("url")  # type: ignore

def upload_bytes(bucket: str, path: str, data: Union[bytes, bytearray], content_type: Optional[str] = None, upsert: bool = True) -> str:
    """
    Upload raw bytes to storage and return the file path (key) stored.
    """
    if content_type is None:
        content_type = "application/octet-stream"
    _client().storage.from_(bucket).upload(
        path=path,
        file=data,
        file_options={"contentType": content_type, "upsert": upsert},
    )
    return path

def upload_file(bucket: str, path: str, file_path: Union[str, Path], upsert: bool = True) -> str:
    """
    Upload a local file and return its storage path.
    """
    file_path = Path(file_path)
    content_type, _ = mimetypes.guess_type(str(file_path))
    with open(file_path, "rb") as f:
        _client().storage.from_(bucket).upload(
            path=path,
            file=f,
            file_options={"contentType": content_type or "application/octet-stream", "upsert": upsert},
        )
    return path

def remove_file(bucket: str, path: str) -> None:
    _client().storage.from_(bucket).remove([path])

def public_url(bucket: str, path: str) -> str:
    """
    If the bucket is public, this returns a public URL (no signature).
    """
    return _client().storage.from_(bucket).get_public_url(path)
