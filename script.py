from googleapiclient.http import MediaFileUpload
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import sys
from getCreds import getCreds


def getFiles(creds):
    try:
        service = build("drive", "v3", credentials=creds)
        results = (
            service.files()
            .list(pageSize=20, fields="nextPageToken, files(id, name)")
            .execute()
        )
        items = results.get("files", [])

        if not items:
            print("No files found.")
            return
        print("Files:")
        for item in items:
            print(f"{item['name']} ({item['id']})")
    except HttpError as error:
        print(f"An error occurred: {error}")


def uploadFile(creds, filePath, folder="1aP79jtm2N7tVfEhmNcHCZteKQ4V7mJEL"):
    try:
        service = build("drive", "v3", credentials=creds)
        file_metadata = {"name": os.path.basename(filePath), "parents": [folder]}
        media = MediaFileUpload(filePath, resumable=True)
        file = (
            service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        print(f'File ID: {file.get("id")}')

    except HttpError as error:
        print(f"An error occurred: {error}")
        file = None

    return file.get("id")


def uploadDirectory(creds, path, folder="1aP79jtm2N7tVfEhmNcHCZteKQ4V7mJEL"):
    try:
        if os.path.isfile(path):
            return uploadFile(creds, path, folder)
        elif os.path.isdir(path):
            service = build("drive", "v3", credentials=creds)
            file_metadata = {
                "name": os.path.basename(path),
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [folder],
            }

            folder = service.files().create(body=file_metadata, fields="id").execute()
            newFolderID = folder.get("id")
            filePaths = [os.path.join(path, i) for i in os.listdir(path)]
            for filePath in filePaths:
                if os.path.isfile(filePath):
                    uploadFile(creds, filePath, newFolderID)
                elif os.path.isdir(filePath):
                    uploadDirectory(creds, filePath, newFolderID)
            return newFolderID

    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


if __name__ == "__main__":
    creds = getCreds()
    path = sys.argv[1]
    uploadDirectory(creds, path)
