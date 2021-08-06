#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
readonly HA_CONFIG_TEMPLATE="${SCRIPT_DIR}/configuration.yaml"
readonly HA_CONFIG_DIR="${HOME}/ha-dev-config"

if [ ! -e "${HA_CONFIG_DIR}" ]; then
  mkdir -p "${HA_CONFIG_DIR}"
fi

if [ -f "${HA_CONFIG_TEMPLATE}" ]; then
  cp "${HA_CONFIG_TEMPLATE}" "${HA_CONFIG_DIR}"
fi

if [ ! -e "${HA_CONFIG_DIR}/custom_components" ]; then
  ln -s "${SCRIPT_DIR}/../custom_components" "${HA_CONFIG_DIR}/custom_components"
fi

cd "${SCRIPT_DIR}/.."
poetry run hass --verbose --config "${HA_CONFIG_DIR}"
