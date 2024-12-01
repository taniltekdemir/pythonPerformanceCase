#!/usr/bin/env bash
host="$1"
port="$2"
shift 2
cmd="$@"

echo "Waiting for $host:$port..."

until pg_isready -h "$host" -p "$port"; do
  echo "Waiting for $host:$port..."
  sleep 2
done

echo "$host:$port is available. Starting application..."
exec $cmd