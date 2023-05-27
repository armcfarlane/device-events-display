#!/usr/bin/env bash
#
[ -n "$DEBUG" ] && set -x

BOLD_RED='\033[1:31m'
NO_COLOR='\033[0m'

function die() {
    >&2 echo -e "${BOLD_RED}error:${NO_COLOR} $@"
    exit 1
}

if [ -z "$EVENTS_DISPLAY_SERVICE_PORT" ]; then
    die "You must set the mandatory environment variable \"EVENTS_DISPLAY_SERVICE_PORT\"."
fi

startup_command="uvicorn app.main:app --host 0.0.0.0 --port $EVENTS_DISPLAY_SERVICE_PORT"

if [ -n "$EVENTS_DISPLAY_LOG_LEVEL" ]; then
    # Change log level value to lower case.
    echo "EVENTS_DISPLAY_LOG_LEVEL: \"$EVENTS_DISPLAY_LOG_LEVEL\""
    log_level=$(echo "${EVENTS_DISPLAY_LOG_LEVEL,,}")
    startup_command="${startup_command} --log-level $log_level"
fi

echo "Attempting to execute the command: $startup_command..."
eval "$startup_command"
