#!/usr/bin/env bash

if [ -n "$AWS_BUCKET" ]; then
  cat << EOF > .s3cfg
[default]
access_key = ${AWS_ACCESS_KEY}
secret_key = ${AWS_SECRET_KEY}
EOF
  if [ -d world ]; then
    s3cmd sync world/ s3://${AWS_BUCKET}/world/
  else
    mkdir -p world
    cd world
    s3cmd get --recursive s3://${AWS_BUCKET}/world/
    cd ..
  fi
  rm .s3cfg
fi
