# apple-music-converter

I got tired of paying for both Apple Music and Spotify, so I built this to see what I'd actually miss if I dropped one. It pulls my Last.fm history and checks what's available in Apple Music's catalog, then spits out a report of gaps.

## install

pip install -r requirements.txt

## usage

python convert.py --lastfm-user myusername --apple-token "Bearer abc..."

Cache lives in ~/.cache/apple-music-converter/ so re-runs are fast. Delete that dir if you want a fresh pull.

<!-- verified: 2026-10-05 -->
