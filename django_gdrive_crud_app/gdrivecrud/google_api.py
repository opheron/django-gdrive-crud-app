from typing import Optional

from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build, Resource
from google.auth.transport.requests import Request

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
        'https://www.googleapis.com/auth/drive'  # include gdrive API scope to ensure permissions request
    ]

    credentials = Credentials(
        token=token.token,
        refresh_token=token,
        scopes=scopes,
        token_uri='https://accounts.google.com/o/oauth2/token',
        client_id=client.client_id,
        client_secret=client.secret)

    # refresh credentials if invalid or expired
    if not credentials.valid or credentials.expired:
        if credentials.refresh_token:
            token.token_secret = credentials.refresh_token

    token.token = credentials.token
    token.save()

    service = build('drive', 'v3', credentials=credentials)
    return service


def get_gdrive_root_folder_items(service) -> list | None:
    results = (
        service.files()
        .list(
            # pageSize=200,
            fields="nextPageToken, files(id, name, modifiedTime, kind, mimeType, webContentLink, webViewLink, fileExtension, exportLinks)",
            q="'root' in parents and mimeType != 'application/vnd.google-apps.folder' and trashed = false",
            orderBy="folder,name,modifiedTime desc",
        )
        .execute()
    )
    items = results.get("files", [])

    if not items:
        return None

    return results

def delete_gdrive_file(service, file_id) -> bool:

    body_value = {'trashed': True}
    response = service.files().update(fileId=file_id, body=body_value).execute()
    return response
