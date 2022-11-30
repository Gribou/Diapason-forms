#!/bin/bash

# Fait un dump de base de données et le stocke dans backups/database_dumps
# Garde seulement les 10 derniers
# Les media sont sauvegardés dans backups/media_exports

TIME_OF_BACKUP=$(exec date +%Y%m%d_%H%M%S)
DIR_FOR_BACKUP=../backups/database_dumps
DIR_FOR_MEDIA=../backups/media_exports
FILE_NAME=efne_$TIME_OF_BACKUP.json

mkdir -p $DIR_FOR_BACKUP
python manage.py dumpdata \
    --exclude auth.permission \
    --exclude contenttypes \
    --exclude admin.logentry \
    --exclude=sessions.session \
    --natural-primary --natural-foreign \
    --indent 4 \
    > $DIR_FOR_BACKUP/$FILE_NAME

# on supprime les sauvegardes trop anciennes : on garde seulement les 10 dernières
ls -tr $DIR_FOR_BACKUP/*.json | head -n -10 | xargs --no-run-if-empty rm

# sauvegarde des fichiers media
# Les fichiers qui ne sont plus présents dans /media seront aussi supprimés de la sauvegarde
mkdir -p $DIR_FOR_MEDIA
rsync -a --delete media/ $DIR_FOR_MEDIA