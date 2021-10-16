#!/bin/bash
cd /usr/src/app && uvicorn app.apis.api_v1:app --host 0.0.0.0 --port 80 --reload;