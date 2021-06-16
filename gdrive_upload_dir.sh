#!/usr/bin/bash

thermopylaelogsId=$(gdrive list | grep thermopylaelogs | grep -Eo '^[^ ]+')

fileId=$(gdrive list | grep $1 | grep -Eo '^[^ ]+')
if [ $? -ne 0 ]
then
	gdrive mkdir --parent $thermopylaelogsId $1
	fileId=$(gdrive list | grep $1 | grep -Eo '^[^ ]+')
fi

gdrive sync upload --keep-local --delete-extraneous $1 $fileId
