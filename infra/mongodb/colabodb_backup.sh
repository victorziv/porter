#!/bin/bash

OUTPUT_DIR=/data/mongobackup
PORT=27017
DB=colabo
S3_DESTINATION="s3://colabo.com_backup/automation/mongodb"

now=$(/bin/date +%Y%m%d%H%M)

DUMP_DIR="${OUTPUT_DIR}/${now}"

/usr/bin/mongodump --port $PORT --db=${DB}  --out=${DUMP_DIR}


# Backup the mongodb dump to AWS S3 storage
# --delete (boolean) Files that exist in the destination but not in the source are deleted during sync.
/usr/local/bin/aws s3 sync "${OUTPUT_DIR}/" "${S3_DESTINATION}/" --delete

