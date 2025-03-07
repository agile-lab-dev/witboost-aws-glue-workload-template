#!/bin/sh

compute_bucket_name() {
    local domain="$1"
    local dpName="$2"
    local componentName= "$3"
    local environment="$4"

    local bucket_name_without_hash="${domain}-${dpName}-${componentName}-${environment}"
    bucket_name_without_hash=$(echo "$bucket_name_without_hash" | tr -d ' ' | tr '[:upper:]' '[:lower:]')

    local hash=$(echo -n "$bucket_name_without_hash" | sha256sum | cut -c1-5)

    if [ $(echo -n ${bucket_name_without_hash} | wc -m) -gt 58 ]; then
        echo "${bucket_name_without_hash:0:58}${hash}"
    else
        echo "${bucket_name_without_hash}${hash}"
    fi
}