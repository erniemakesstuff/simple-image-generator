Simple image generator that calls Lexica art to download AI generated images.

Exposes server API for poller to invoke.

# Usage
Start shell environment
`pipenv shell`
`python main.py`

Note: Running on 5051 port to avoid localhost collision when running as sidecar.
Set env if running locally outside container:
`export SHARED_MEDIA_VOLUME_PATH="/Users/owner/tmp_media/"`
## venvs
Creating virtual env if not present `python3 -m venv .venv`
Activate venv shell `. ./.venv/bin/activate`
Set VisualStudioCode interpreter to your .venv path.

## Setting new dependencies
`pipenv requirements > requirements.txt`

# ECR Upload
`aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 971422718801.dkr.ecr.us-west-2.amazonaws.com`
`docker build -t bezalel-truevine-simple-image-generator .`
`docker tag bezalel-truevine-simple-image-generator:latest 971422718801.dkr.ecr.us-west-2.amazonaws.com/bezalel-truevine-simple-image-generator:latest`
`docker push 971422718801.dkr.ecr.us-west-2.amazonaws.com/bezalel-truevine-simple-image-generator:latest`

