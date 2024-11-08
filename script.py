import googleapiclient.discovery
import isodate


def get_playlist_duration(api_key, playlist_id):
    
    # inicializa o cliente da API do YouTube
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey = api_key)

    total_duration = 0

    # pega todos os vídeos da playlist
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part = "contentDetails",
            playlistId = playlist_id,
            maxResults = 50,
            pageToken = next_page_token
        )
        response = request.execute()

        video_ids = [item['contentDetails']['videoId'] for item in response['items']]

        # pega a duração de cada vídeo
        video_request = youtube.videos().list(
            part = "contentDetails",
            id = ",".join(video_ids)
        )
        video_response = video_request.execute()

        for video in video_response['items']:
            duration = isodate.parse_duration(video['contentDetails']['duration'])
            total_duration += duration.total_seconds()

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    # Converte para horas
    total_hours = total_duration // 3600
    total_minutes = (total_duration % 3600) // 60
    total_seconds = int(total_duration % 60)
    return f"{int(total_hours)} horas {int(total_minutes)} minutos e {int(total_seconds)} segundos"


api_key = "AIzaSyATHL22mLRvnhCyNBRQWlnAe5qJ9MnOAjA"

playlist_id = (input(f"Digite o ID da playlist: "))
print(get_playlist_duration(api_key, playlist_id))
