from rest_framework import parsers


class NestedMultipartParser(parsers.MultiPartParser):
    """
    Parser for processing nested field values as well as multipart files.

    """

    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream=stream,
                               media_type=media_type,
                               parser_context=parser_context)
        data = {}
        for key, value in result.data.items():
            root_key = self._get_root_key(key)
            data[root_key] = self._append_anything(data.get(root_key, None),
                                                   key[len(root_key):], value)
        for key, file in result.files.items():
            root_key = self._get_root_key(key)
            data[root_key] = self._append_anything(data.get(root_key, None),
                                                   key[len(root_key):], file)
        return parsers.DataAndFiles(data, {})

    def _get_root_key(self, key):
        return key.split(".")[0].split("[")[0]

    def _is_last_child(self, key):
        return "[" not in key and "." not in key

    def _get_child_list_index(self, key):
        if key[0] == "[":
            split_index = key.index("]")
            return (int(key[1:split_index]), key[split_index + 1:])
        else:
            return (None, key)

    def _get_child_dict_key(self, key):
        if key[0] == ".":
            child_key = self._get_root_key(key[1:])
            return (child_key, key[len(child_key) + 1:])
        else:
            return (None, key)

    def _append_anything(self, existing_data_for_key, key, value):
        if key == "":
            return value
        (child_index, remaining_keys) = self._get_child_list_index(key)
        if child_index is not None:
            return self._build_child_list(existing_data_for_key, child_index,
                                          value, remaining_keys)
        (child_key, remaining_keys) = self._get_child_dict_key(key)
        if child_key is not None:
            return self._build_child_dict(existing_data_for_key, child_key,
                                          value, remaining_keys)

    def _build_child_list(self, existing_list, index, value, remaining_keys):
        # pad existing data to be able to write at 'index'
        if existing_list is None:
            existing_list = []
        if len(existing_list) < index + 1:
            existing_list = existing_list + \
                [{}] * (index + 1 - len(existing_list))
        if not remaining_keys:
            existing_list[index] = value
        else:
            existing_list[index] = self._append_anything(
                existing_list[index], remaining_keys, value)
        return existing_list

    def _build_child_dict(self, existing_dict, key, value, remaining_keys):
        if existing_dict is None:
            existing_dict = {}
        if not remaining_keys:
            existing_dict[key] = value
        else:
            existing_dict[key] = self._append_anything(
                existing_dict.get(key, None), remaining_keys, value)
        return existing_dict
