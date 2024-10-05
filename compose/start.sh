#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

alembic upgrade head
uvicorn app:app --reload --host $APP_HOST --port $APP_PORT --log-level info --workers 1
