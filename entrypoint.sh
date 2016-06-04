#!/bin/sh

#
# Validate input:
#   ENTROPY_FAULTS
#     - present
#     - valid and defined by image
#   ENTROPY_FREQUENCY
#     - present
#     - in whole seconds
#   ENTROPY_PROBABILITY
#     - present
#     - decimal less than or equal to 1
#

if [ -z "$ENTROPY_PROBABILITY" ]; then
  echo >&2 '[ERROR]: specify ENTROPY_PROBABILITY environment variable'
  exit 1
fi

if [ -z "$ENTROPY_FREQUENCY" ]; then
  echo >&2 '[ERROR]: specify ENTROPY_FREQUENCY environment variable'
  exit 1
fi

if [ -z "$ENTROPY_FAULTS" ]; then
  echo >&2 '[ERROR]: specify ENTROPY_FAULTS environment variable'
  exit 1
fi

#
# Generate profile
#
ENTROPY_CLEAR_WEIGHT="$(echo 1 - $ENTROPY_PROBABILITY | bc)"
ENTROPY_FAULT_WEIGHT=$ENTROPY_PROBABILITY
cat profile.tmpl | \
  sed "s/ENTROPY_SECONDS/${ENTROPY_FREQUENCY}/" | \
  sed "s/ENTROPY_FAULT_WEIGHT/${ENTROPY_FAULT_WEIGHT}/" | \
  sed "s/ENTROPY_CLEAR_WEIGHT/${ENTROPY_CLEAR_WEIGHT}/" | \
  sed "s/ENTROPY_FAULT/${ENTROPY_FAULTS}/" \
  > ./gremlins/profiles/entropy.py

printf "[%s, %s, %s]" $ENTROPY_FAULTS $ENTROPY_FREQUENCY $ENTROPY_PROBABILITY

#
# Start gremlins
#
exec "$@" # run the default command
