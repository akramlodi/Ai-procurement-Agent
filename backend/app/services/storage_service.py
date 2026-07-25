import os


class StorageService:
    BUCKET = "procurement-files"

    def __init__(self, supabase):
        self.supabase = supabase

    def upload_file(self, procurement_id: str, filename: str, file_bytes: bytes, content_type: str = "application/octet-stream") -> str:
        path = f"{procurement_id}/{filename}"
        self.supabase.storage.from_(self.BUCKET).upload(
            path,
            file_bytes,
            file_options={"content-type": content_type},
        )
        return path

    def get_signed_url(self, storage_path: str) -> str:
        result = self.supabase.storage.from_(self.BUCKET).create_signed_url(storage_path, 3600)
        return result.get("signedURL", "")
