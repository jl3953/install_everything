#!/usr/bin/bash

thermopylaelogsId=$(gdrive list | grep thermopylaelogs | grep -Eo '^[^ ]+')

fileId=$(gdrive list | grep $1 | grep -Eo '^[^ ]+')
if [ $? -ne 0 ]
then
	gdrive upload --parent $thermopylaelogsId $1
else
	gdrive update $fileId $1
fi
