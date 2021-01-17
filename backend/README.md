# Backend

### Dependencies

- MySQL 8.0
- GCP Storage Bucket

### API keys

You will need:
 - a Spotify API key: https://developer.spotify.com/documentation/web-api/
 - GCP key: https://cloud.google.com/iam/docs/creating-managing-service-account-keys

Copy `.env.example` into `.env`. Add API keys accordingly

### Virtual env

```
mkdir venv
python3 -m venv venv/
```


### Requirements

```
python3 -m pip install -r requirements.txt
```

### Run the backend with

```
export FLASK_APP=main.py
python3 -m flask run
```

## APIs

http://mashme.tech/api/cached-songs

- Fetch the list of cached songs ready for the user to mash

`curl -X POST http://34.73.177.14/api/mix/2KGe_4leh_Y%3Bf4zdkP11BHU`

- Generate mashup for two existing songs

`curl -X POST http://34.73.177.14/api/mix/2KGe_4leh_Y%3Bforever%20young%20alphaville`

- Generate a mashup for a new song