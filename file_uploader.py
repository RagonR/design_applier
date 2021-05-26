import dropbox, io


class FileUploader:
    def __init__(self, access_token):
        self.access_token = access_token
        self.dbx = dropbox.Dropbox(self.access_token)

    def __del__(self):
        self.dbx.close()

    def upload_image(self, image_binary: io.BytesIO, filename: str):
        try:
            meta = self.dbx.files_upload(image_binary.read(), filename, mode=dropbox.files.WriteMode("overwrite"))
            link = self.dbx.sharing_create_shared_link(filename)
            return link.url
        except dropbox.exceptions.ApiError:
            print("!E!", "Failed to dropbox")

    def check_connection(self) -> bool:
        try:
            self.dbx.check_user(query=u"check_101")
        except dropbox.exceptions.AuthError as a:
            print("wrong access token!?!")
            return False
        return True


def get_file_uploader(token: str):
    return FileUploader(token)
