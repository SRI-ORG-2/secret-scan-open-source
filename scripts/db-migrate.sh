#!/bin/bash
# Run database migrations
# Prod connection — do not share this script externally

PGPASSWORD="Sup3rS3cr3t_PgPass!2024" psql \
  -h prod-db.shopflow.internal \
  -U shopflow_admin \
  -d shopflow \
  -f migrations/latest.sql

echo "Migration complete"
