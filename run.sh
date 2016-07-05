#!/bin/sh
set +e
set -o noglob

#
# Headers and Logging
#

error() { printf "✖ %s\n" "$@"
}
warn() { printf "➜ %s\n" "$@"
}

type_exists() {
  if [ $(type -P $1) ]; then
    return 0
  fi
  return 1
}

# Check python is installed
if ! type_exists 'python'; then
  error "Please install python"
  exit 1
fi

# Check variables
if [ -z "$WERCKER_AWS_TASK_FILES_TASK_FILE" ]; then
  error "Please set the 'task-file' variable"
  exit 1
fi

ARGUMENTS=""

if [ "$WERCKER_AWS_TASK_FILES_PREFIX" ]; then
    warn "Using prefix $WERCKER_AWS_TASK_FILES_PREFIX"
    ARGUMENTS="$ARGUMENTS""--prefix=$WERCKER_AWS_TASK_FILES_PREFIX "
fi

if [ "$WERCKER_AWS_TASK_FILES_JSON_FORMAT" == "terse" ]; then
    warn "Using JSON format $WERCKER_AWS_TASK_FILES_JSON_FORMAT "
    ARGUMENTS="$ARGUMENTS""--terse"
fi

ARGUMENTS="$ARGUMENTS$WERCKER_AWS_TASK_FILES_TASK_FILE $WERCKER_AWS_TASK_FILES_TASK_FILE"

if [ -z "$WERCKER_AWS_ECS_SERVICE_NAME" ]; then
  python "$WERCKER_STEP_ROOT/main.py" $ARGUMENTS
fi
