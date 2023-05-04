# Google Bioacoustics Embedding Model Service
A lightweight wrapper around the [Chirp module](https://github.com/google-research/chirp/) for generating embeddings from audio clips.

## Setup
This project will only work on Linux x64 architecture.
1. Install Docker
2. `docker build -t embed .`
3. `docker run -p 80:80 embed`
4. `curl --location --request POST 'http://localhost/embed' \
--form 'audio_file=@"tests/clap.wav"'`
