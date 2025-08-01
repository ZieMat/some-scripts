#!/bin/bash

package="$1"

if [ -z "$package"]; then
    echo "Usage: $0 <package-name>"
    exit 1
fi

apt-get update
apt-cache policy "$package"