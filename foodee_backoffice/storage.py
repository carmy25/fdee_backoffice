import os
from storages.backends.s3boto3 import S3Boto3Storage


class TigrisMediaStorage(S3Boto3Storage):

    def url(self, name):
        return f"https://{self.bucket_name}.fly.storage.tigris.dev/{name}"

    def get_available_name(self, name, max_length=None):
        """
        Preserve the original name, and if file exists, append suffixes.
        """
        if not self.exists(name):
            return name

        base, ext = os.path.splitext(name)
        counter = 1
        new_name = f"{base}_{counter}{ext}"
        while self.exists(new_name):
            counter += 1
            new_name = f"{base}_{counter}{ext}"

        return new_name
