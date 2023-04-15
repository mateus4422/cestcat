#!/bin/bash
set -e

# If the STREAMLIT_API_KEY environment variable is not set, then exit.
if [[ -z "${STREAMLIT_API_KEY}" ]]; then
  echo "The STREAMLIT_API_KEY environment variable is not set. Exiting."
  exit 1
fi

# Copy over the token to the streamlit folder.
echo "Setting up Streamlit API key."
mkdir -p ~/.streamlit
echo "\
[general]\n\
email = \"\"\n\
" > ~/.streamlit/credentials.toml
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
