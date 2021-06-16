#!/usr/bin/bash

get_fileid() {
    echo $(gdrive list --no-header --query "name = '$1' and trashed = false" --order "createdTime desc" --max 1 | grep -Eo '^[^ ]+')
}

set -x

thermopylaelogsId=$(get_fileid thermopylaelogs)
fileId=$(get_fileid $1)

if [[ $fileId == "" ]];
then
	gdrive upload --parent $thermopylaelogsId $1
else
	gdrive update $fileId $1
fi

set +x
