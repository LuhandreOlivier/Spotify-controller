# Spotify API Integration

## Authentication

This project uses the Spotify Web API for:
- Playback control
- Volume adjustment
- Track metadata retrieval

## Required Credentials

The following are required:
- Client ID
- Client Secret
- Access Token
- Refresh Token

## Token Refresh

When the access token expires, the firmware automatically requests a refreshed token using the refresh token flow.

## API Endpoints Used

| Purpose | Endpoint |
|---|---|
| Current Track | `/v1/me/player/currently-playing` |
| Playback State | `/v1/me/player` |
| Volume Control | `/v1/me/player/volume` |
| Skip Track | `/v1/me/player/next` |
| Previous Track | `/v1/me/player/previous` |
