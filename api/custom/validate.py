
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.dateparse import parse_datetime, parse_date, parse_time
from base64 import b64decode, b64encode
import html


def validate_text(value, *args):
    return html.escape(value), None


def validate_boolean(value, *args):
    return value == "true" or value == "True", None


def validate_choice(value, choices, *args):
    clean_choices = [c.label for c in choices.choices.all()]
    return value, "{} n'est pas un choix valide".format(value) if value not in clean_choices else None


def validate_multichoice(value, choices, *args):
    clean_choices = [c.label for c in choices.choices.all()]
    for v in value:
        if v not in clean_choices:
            return value, "Un des choix n'est pas un choix valide."
    return value, None


def validate_date(value, *args):
    try:
        parsed = parse_date(value)
        if parsed is None:
            return value, "Ce n'est pas une date valide."
        return value, None
    except (ValueError, TypeError):
        return value, "Ce n'est pas une date valide."


def validate_time(value, *args):
    try:
        parsed = parse_time(value)
        if parsed is None:
            return value, "Ce n'est pas une heure valide."
        return value, None
    except (ValueError, TypeError):
        return value, "Ce n'est pas une heure valide."


def validate_datetime(value, *args):
    try:
        parsed = parse_datetime(value)
        if parsed is None:
            return value, "Ce n'est pas une date et une heure valide."
        return value, None
    except (ValueError, TypeError):
        return value, "Ce n'est pas une date et une heure valide."


def validate_file(value, *args):
    if isinstance(value, InMemoryUploadedFile):
        return value, None
    if isinstance(value, str):
        value_in_bytes = bytes(value.replace(
            "data:image/png;base64,", ""), 'ascii')
        if b64encode(b64decode(value_in_bytes)) != value_in_bytes:
            return value, "Ce n'est pas un fichier valide."
        return value, None
    return value, "Ce n'est pas un fichier valide."


validation_functions = {
    "text-input": validate_text,
    "password": validate_text,
    "checkbox": validate_boolean,
    "checkbox-group": validate_multichoice,
    "radio": validate_choice,
    "button": validate_boolean,
    "button-group": validate_choice,
    "select": validate_choice,
    "date": validate_date,
    "time": validate_time,
    "datetime": validate_datetime,
    "photo": validate_file,
    "drawing": validate_file,
}


def validate_field(field, value):
    return validation_functions[field.type](value, field.choices)


def validate_required_fields(data, form):
    errors = {}
    for field in form.fields.filter(required=True):
        if field.slug not in data.keys():
            errors[field.slug] = "Ce champ est obligatoire."
    return errors


def validate(data, form):
    clean_data = {}
    files = []
    errors = validate_required_fields(data, form)
    for key, value in data.items():
        field = form.fields.filter(slug=key).first()
        if field is None:
            errors[key] = "Ce champ n'est pas présent dans le formulaire"
        elif not field.is_readonly():
            clean_value, error = validate_field(field, value)
            if error is not None:
                errors[key] = error
            if clean_value is not None:
                is_file = field.type in ['photo', 'drawing']
                is_bool = field.type in ['checkbox', 'button']
                is_array = field.type in ['checkbox-group']
                clean_data[key] = {'value': clean_value,
                                   'is_file': is_file, 'is_bool': is_bool,
                                   'is_array': is_array, 'field': field}
                if is_file:
                    files.append(clean_value)
    return (clean_data, files, errors if bool(errors) else None)
