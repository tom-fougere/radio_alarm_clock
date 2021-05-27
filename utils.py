def get_value_from_dict(item_dict, wanted_field, default_value=''):
    """
    Get the value from a dictionary selecting the field. A default value is set if the field don't exist
    :param item_dict: dictionary to watch, dict
    :param wanted_field: field to search in the dictionary, string
    :param default_value: default value if the wanted field don't exist
    :return:
        - value: value of the dictionary with the wanted field
    """

    value = default_value
    if wanted_field in item_dict:
        value = item_dict[wanted_field]

    return value