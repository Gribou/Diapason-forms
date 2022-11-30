#!/bin/sh

# creates an .env file for react building in Gitlab Pipeline (when .env is not reachable because in .gitignore but env variables customizable in Gitlab settings)

set -e;

touch web/.env

echo "REACT_APP_DEBUG=0" >> web/.env
echo "REACT_APP_STATE_ENCRYPTION_KEY=$REACT_APP_STATE_ENCRYPTION_KEY" >> web/.env

if [ $SUBDIRECTORY == "root" ]; then
    echo "PUBLIC_URL=/" >> web/.env
    echo "REACT_APP_BACKEND_HOST=" >> web/.env
else
    echo "PUBLIC_URL=/${SUBDIRECTORY}" >> web/.env
    echo "REACT_APP_BACKEND_HOST=/${SUBDIRECTORY}" >> web/.env
fi

