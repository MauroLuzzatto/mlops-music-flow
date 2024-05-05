
[![Tests](https://github.com/MauroLuzzatto/music-flow-api/workflows/Tests/badge.svg)](https://github.com/MauroLuzzatto/music-flow-api/actions?workflow=Tests)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


# MusicFlow API

MusicFlow is an API that use the Spotify's API to predict the number of song streams using the Spotify audio features and track metadata.

The MusicFlow API uses the personal Spotify streaming history to train a machine learning model that predicts the number of streams for a given song. The training dataset uses number of stream values between 0 and 30.

The MusicFlow API is built using the FastAPI framework, which makes it fast, easy to use, and well-documented.



## Available Endpoints

The MusicFlow API provides the following endpoints:

- `musicflow.link/` - The root page of the MusicFlow API.
- `musicflow.link/api/health` - Returns the health status of the API.
- `musicflow.link/api/raw_features/?song={song}&artist={artist}` - Returns the unprocessed audio features of a song using the Spotify API.
- `musicflow.link/api/features/?song={song}&artist={artist}` - Returns the unprocessed audio features of a song.
- `musicflow.link/api/prediction/?song={song}&artist={artist}` - Predicts the number of streams for a given song based on the Spotify audio features and track metadata.


## Examples

### root


[https://musicflow.link/](https://musicflow.link)

<p align="center">
<img src="https://github.com/MauroLuzzatto/mlops-music-flow/raw/main/static/ui.png"/>
</p>

### `/prediction`

Let's predict the number of streams for "The Less I know the better" from "Tame Impala":

[https://musicflow.link/api/prediction/?song=The Less I know the better&artist=Tame Impala](https://musicflow.link/api/prediction/?song=The%20Less%20I%20know%20the%20better&artist=Tame%20Impala)


Response:
```
{
    "song": "The Less I Know The Better",
    "artist": "Tame Impala",
    "prediction": 5.35,
    "description": (
        "The predicted number of future streams of the song based on the Spotify"
        " API audio features."
    ),
    "song_metadata": {
        "song": "The Less I Know The Better",
        "artist": ["Tame Impala"],
        "album": "Currents",
    },
    "message": {"emoji": "😍", "text": "What a banger!"},
}
```


### `/features`

[https://musicflow.link/api/features/?song=The Less I know the better&artist=Tame Impala](https://musicflow.link/api/features/?song=The%20Less%20I%20know%20the%20better&artist=Tame%20Impala)


Response:
```
{
  "track":{
    "track_name":"The less I know the better",
    "artist_name":"Tame Impala",
    "number_of_available_markets":183,
    "num_artists":1,
    "duration_ms":216320,
    "explicit":true,
    "popularity":83,
    "isrc":"AUUM71500303"
  },
  "album":{
    "release_date_precision":"day",
    "release_year":2015,
    "release_month":7,
    "release_day":17,
    "date_is_complete":true,
    "album":"Currents"
  },
  "audio_features":{
    "danceability":0.64,
    "energy":0.74,
    "key":4,
    "loudness":-4.083,
    "mode":1,
    "speechiness":0.0284,
    "acousticness":0.0115,
    "instrumentalness":0.00678,
    "liveness":0.167,
    "valence":0.785,
    "tempo":116.879,
    "id":"6K4t31amVTZDgR3sKmwUJJ",
    "time_signature":4
  }
}
```

## Get Spotify API Access Client ID and Client Secret

To access the Spotify API, you need to create a Spotify Developer account and obtain a Client ID and Client Secret. Follow these steps:

- Go to the Spotify Developer Dashboard and log in with your Spotify account.
- Click on "Create an app" and fill out the required information.
- Once you have created the app, you will see your Client ID and Client Secret on the app dashboard.
- Add them to your `env` file


## Model Features derived from the Spotify API

### Used Spotify API endpoints

The model features are created based on the responses from the endpoints below.

- `tracks`
- `audio_features`
- `audio_anaysis` (currenly not used)

### Model Features

| Column Name | Description | Data Type | Allowed Value Ranges |
|-------------|-------------|----------|----------------------|
| number_of_available_markets | The number of markets in which the track can be played | integer | 0-79 |
| release_year | The year the track was released | integer | 0 <= year <= current year |
| release_month | The month the track was released | integer | 1 <= month <= 12 |
| release_day | The day the track was released | integer | 1 <= day <= 31 |
| date_is_complete | Indicates if the release date is completely known | boolean | true/false |
| num_artists | The number of artists credited on the track | integer | n/a |
| duration_ms | The duration of the track in milliseconds | integer | n/a |
| explicit | Indicates if the track contains explicit content | boolean | true/false |
| popularity | The popularity of the track | integer | 0 <= popularity <= 100 |
| danceability | The danceability of the track | float | 0 <= danceability <= 1 |
| energy | The energy of the track | float | 0 <= energy <= 1 |
| loudness | The loudness of the track in decibels (dB) | float | -60 <= loudness <= 0 |
| mode | The modality (major or minor) of the track | integer | 0 = minor, 1 = major |
| speechiness | The presence of spoken words in the track | float | 0 <= speechiness <= 1 |
| acousticness | The acousticness of the track | float | 0 <= acousticness <= 1 |
| instrumentalness | The instrumentalness of the track | float | 0 <= instrumentalness <= 1 |
| liveness | The liveness of the track | float | 0 <= liveness <= 1 |
| valence | The valence of the track | float | 0 <= valence <= 1 |
| tempo | The tempo of the track in beats per minute (BPM) | float | 0 <= tempo <= 500 |
| time_signature | The time signature of the track | integer | 0 <= time_signature <= 7 |
| A | The key of the track with pitch class A | integer | 0 = not present, 1 = present |
| A#/Bb | The key of the track with pitch class A#/Bb | integer | 0 = not present, 1 = present |
| B | The key of the track with pitch class B | integer | 0 = not present, 1 = present |
| C | The key of the track with pitch class C | integer | 0 = not present, 1 = present |
| C#/Db | The key of the track with pitch class C#/Db | integer | 0 = not present, 1 = present |
| D | The key of the track with pitch class D | integer | 0 = not present, 1 = present |
| D#/Eb | The key of the track with pitch class D#/Eb | integer | 0 = not present, 1 = present |
| E | The key of the track with pitch class E | integer | 0 = not present, 1 = present |
| F | The key of the track with pitch class F | integer | 0 = not present, 1 = present |
| F#/Gb | The key of the track with pitch class F#/Gb | integer | 0 = not present, 1 = present |
| G | The key of the track with pitch class G | integer | 0 = not present, 1 = present |
| G#/Ab | The key of the track with pitch class G#/Ab | integer | 0 = not present, 1 = present |
| Unknown | The key of the track is unknown | integer | 0 = not present, 1 = present |

<!--

## How to create your own musicflow API?

This repository provides instructions on how to request Spotify streaming history data, download it and create a dataset using music_flow, train a machine learning model, and set up an API using an AWS account.

### Get Spotify API Access Client ID and Client Secret

To access the Spotify API, you need to create a Spotify Developer account and obtain a Client ID and Client Secret. Follow these steps:

- Go to the Spotify Developer Dashboard and log in with your Spotify account.
- Click on "Create an app" and fill out the required information.
- Once you have created the app, you will see your Client ID and Client Secret on the app dashboard.

### Request Spotify Streaming History

To request your Spotify streaming history, you need to follow these steps:

- Go to Spotify's Privacy Settings and log in with your Spotify account.
- Scroll down to "Download your data" and click on "Request".
- You will receive an email from Spotify when your data is ready to be downloaded.

### Download the Data and Creating a Dataset Using `music_flow`

Once you have received the email from Spotify, you can download your data and create a dataset using music_flow by following these steps:

- Download your data from Spotify and unzip the file.
- Install music_flow by running pip install music-flow.
- Create a Python script and use the music_flow library to load the data and create a dataset. Refer to the music_flow documentation for more information on how to do this.

### Train a Machine Learning Model

Once you have created your dataset, you can train a machine learning model by following these steps:

- Import your dataset into your machine learning environment.
- Preprocess the data as needed.
- Choose a machine learning algorithm and train the model.
- Test the model and evaluate its performance.

### Set Up API Using an AWS Account

To set up an API with AWS SAM, follow these steps:

- Install AWS SAM CLI by following the instructions provided here.
- Create a new SAM project using the sam init command.
- Write the code for your Lambda function and API gateway in the appropriate files (e.g., app.py and template.yaml).
- Build and package your SAM application using the sam build and sam package commands.
- Deploy your SAM application using the sam deploy command.
 -->



## Next steps and ongoing work

- Version model
- Add logging
- Allow for continous training
<!-- - Use data classes for sample -->
- Improve feature processing pipeline
<!-- - Improve api reponse for formatted feature -->
- [x] upload the request to S3 (add metadata from request IP, etc.)
- [] Move all configrations outside of code into a yaml file and settings classes
- Add Deep learning models
- [] add model baseline
- [] version the data
- [] add model versioning
- [ ] build a recommender option
- [ ] add mkdocs

<!--

TODO: make info graphics of the application
- use excalidraw


## Plan
- request streaming history from spotify
- find some random tracks (e.g kaggle datasets)
- calculate the numer of streams per track (=target values)
- download features for the tracks
- create the dataset containg the features and the number of streams
- train model using GridSearch
- save different model versions
- use API to serve model
- use API to predict number of streams per track


Using lifespan event on APIRoute() instead in FastAPI() #9664
https://github.com/tiangolo/fastapi/discussions/9664

https://github.com/ipinfo/python
https://github.com/shon/httpagentparser
-->



<!-- curl -XPOST "http://localhost:8080/2015-03-31/functions/function/invocations" -d '{}'

curl: (52) Empty reply from server -->
