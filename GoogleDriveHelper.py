from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriverHelper:
    def __init__(self, folder_name: str):
        self.drive = self._get_drive()
        self.folder_id = self._setup_folder(folder_name=folder_name)

    def upload_file_from_path(self, file_path: str, file_name: str):
        file_metadata = {
            'title': file_name,
            'parents': [{'id': self.folder_id}]
        }
        file = self.drive.CreateFile(file_metadata)
        file.SetContentFile(file_path)
        file.Upload()

    def upload_file_from_content(self, file_bytes: bytes, file_name: str):
        file_metadata = {
            'title': file_name,
            'parents': [{'id': self.folder_id}]
        }
        file = self.drive.CreateFile(file_metadata)
        file.SetContentString(file_bytes)
        file.Upload()

    def _setup_folder(self, folder_name: str):
        query = "title='folder_name' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = (self.drive
                     .ListFile({'q': query.format('folder_name', folder_name)})
                     .GetList())
        if not file_list:
            folder_metadata = {
                'title': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']
        else:
            folder_id = file_list[0]['id']
        return folder_id

    @staticmethod
    def _get_drive() -> GoogleDrive:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        return GoogleDrive(gauth)