#!/bin/sh
seed="$1"
/usr/bin/openssl enc -aes-256-ctr -pass pass:"$seed" -nosalt </dev/zero 2>/dev/null
