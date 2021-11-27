ARG VARIANT="3"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

RUN su vscode -c "pipx install poetry==1.1.11" 2>&1
