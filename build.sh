#!/usr/bin/env bash
set -e

commit_id=$(git rev-parse --short --verify HEAD)
image_repo="qualimente/gremlins"

docker build --tag ${image_repo}:latest --tag ${image_repo}:${commit_id} .
