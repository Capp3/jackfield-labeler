#! /usr/bin/env bash

# Install Xelatex
sudo apt-get install -y git texlive-full texlive-xetex

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Dependencies
uv sync

# Install pre-commit hooks
uv run pre-commit install --install-hooks
