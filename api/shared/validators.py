from django.core.exceptions import ValidationError


def validate_uploaded_file_size(file):
    file_size = file.size
    LIMIT_MB = 50
    if file_size > LIMIT_MB * 1024 * 1024:
        raise ValidationError(
            "La taille du fichier importé doit être inférieure à {} Mo".format(
                LIMIT_MB))
