#!/usr/bin/bash

source /usr/local/bin/gdrive_upload_file

set -x

fileId=$(get_fileid $1)
if [[ $fileId == "" ]];
then
	gdrive mkdir --parent $thermopylaelogsId $1
    fileId=$(get_fileid $1)
fi

gdrive sync upload --keep-local --delete-extraneous $1 $fileId

set +x
