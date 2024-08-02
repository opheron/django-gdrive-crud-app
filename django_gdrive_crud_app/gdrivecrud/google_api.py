from typing import Optional

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource


def build_google_service() -> Resource | None:
    """Use user info from allauth to build Google API service """
    # TODO: Fix to use current user's Social Token
    token = SocialToken.objects.get(pk=1)

    # use SocialApp to get client info
    client = SocialApp.objects.get(
        provider='google'
    )

    scopes = [
        'profile',
        'email',
        'https://www.googleapis.com/auth/drive'  # might actually be unnecessary since requested previously
    ]

    creds = Credentials(
        token=token.token,
        refresh_token=token,
        scopes=scopes,
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=client.client_id,
        client_secret=client.secret)

    service = build('drive', 'v3', credentials=creds)
    return service


def get_gdrive_root_folder_items(service) -> list | None:
    results = (
        service.files()
        .list(
            # pageSize=200,
            fields="nextPageToken, files(id, name, modifiedTime, kind, mimeType, webContentLink, webViewLink, fileExtension, exportLinks)",
            q="'root' in parents and mimeType != 'application/vnd.google-apps.folder'",
            orderBy="folder,name,modifiedTime desc",
        )
        .execute()
    )
    # print(f"{results=}")
    items = results.get("files", [])

    if not items:
        # print("No files found.")
        return None

    # print("Files:")
    # for item in items:
    #     print(f"{item['name']} ({item['id']})")

    return results
