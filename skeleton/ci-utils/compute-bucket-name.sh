#!/bin/sh

compute_bucket_name() {
    local domain="$1"
    local name="$2"
    local environment="$3"

    local bucket_name_without_hash="${domain}-${name}-${environment}"
    bucket_name_without_hash=$(echo "$bucket_name_without_hash" | tr -d ' ' | tr '[:upper:]' '[:lower:]')

    local hash=$(echo -n "$bucket_name_without_hash" | sha256sum | cut -c1-5)

    if [ $(echo -n ${bucket_name_without_hash} | wc -m) -gt 58 ]; then
        echo "${bucket_name_without_hash:0:58}${hash}"
    else
        echo "${bucket_name_without_hash}${hash}"
    fi
}