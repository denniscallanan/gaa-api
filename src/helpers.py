
def get_field_args(obj, new_field_map=None, discarded_fields=None, nested_structure=True):

    attributes = obj.__dict__
    if nested_structure:
        attributes = attributes['__data__']
    field_map = new_field_map or {}
    fields_to_discard = discarded_fields or set([])

    field_args = {}
    for k in list(attributes.keys()):
        if k not in fields_to_discard:
            if k in field_map and field_map[k] is not None:
                field_args[field_map[k]] = attributes[k]
            else:
                field_args[k] = attributes[k]
    return field_args
