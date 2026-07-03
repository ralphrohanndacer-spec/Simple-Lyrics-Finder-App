import json
from PySide6.QtCore import QUrl, QUrlQuery
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply


network_manager = QNetworkAccessManager()

#Sets up the request for data
def req(track_name, artist_name, ui):

    url = QUrl("https://lrclib.net/api/search")
    params = QUrlQuery()

    items = {
        "track_name": track_name,
        "artist_name": artist_name,
    }

    for key, value in items.items():
        params.addQueryItem(key, value)
    url.setQuery(params)

    request = QNetworkRequest(url)
    request.setRawHeader(b"User-Agent", b"LyricsFinderApp/1.0") #Avoid random request block
    reply = network_manager.get(request)
    reply.finished.connect(lambda: response(reply, ui))

#Checks and handles the response
def response(reply: QNetworkReply, ui):
    try:
        if reply.error() != QNetworkReply.NetworkError.NoError:
            status_code = reply.attribute(QNetworkRequest.Attribute.HttpStatusCodeAttribute)
            error_type = reply.error()

            if status_code is not None:
                error_message = http_error_message(status_code)
            elif error_type == QNetworkReply.NetworkError.TimeoutError:
                error_message = "Timeout error:\nThe request timed out"
            else:
                error_message = "Connection error:\nCheck your internet connection"

            ui.resultLabel.setText(error_message)
            return

        raw_data = reply.readAll().data().decode("utf-8")
        data = json.loads(raw_data)

        if data:
            lyrics = data[0].get('plainLyrics')
            lyrics = lyrics.replace("\n", "<br>") if lyrics else "No lyrics found for this track"
        else:
            lyrics =  "No such song found"
        ui.resultLabel.setHtml(lyrics)

    except Exception:
        ui.resultLabel.setText("Application Error:\nFailed to process track data properly.")

    finally:
        reply.deleteLater()

#Display specific error message
def http_error_message(status_code):
    if status_code == 429:
        return "Slow down! You are searching too fast."
    elif status_code == 400:
        return "Invalid search parameters."
    elif status_code in [500, 502, 503]:
        return "The lyrics database is currently overloaded. Try again later."
    else:
        return f"Server Error (Status: {status_code})"