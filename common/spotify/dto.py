from pydantic import BaseModel


class AccessTokenBody(BaseModel):
    access_token: str
    token_type: str
    scope: str
    expires_in: int
    refresh_token: str


class ProfileResponse(BaseModel, extra='ignore'):
    id: str
    display_name: str
    uri: str
    # TODO images

class ArtistDetails(BaseModel, extra='ignore'):
    id: str
    name: str
    # TODO genres: list[str]

class TopArtistsResponse(BaseModel):
    items: list[ArtistDetails]

class TrackDetail(BaseModel, extra='ignore'):
    artists: list[ArtistDetails]
    name: str
    album_type: str
    id: str

class AlbumDetails(BaseModel, extra='ignore'):
    album: TrackDetail

class TopTracksResponse(BaseModel):
    items: list[AlbumDetails]

