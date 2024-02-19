#!/bin/bash

# Retrieve the latest Git SHA
GIT_SHA=$(git rev-parse HEAD)

# Update values.yaml with the new Git SHA
sed -i "s/^  tag: .*$/  tag: \"$GIT_SHA\"/" values.yaml
