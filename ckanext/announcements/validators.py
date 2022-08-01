from ckan.plugins import toolkit


def validate_announcement(data_dict):
    errors = {}
    if not data_dict.get("from_date"):
        errors["from_date"] = ["'From date' is required"]
    if not data_dict.get("to_date"):
        errors["to_date"] = ["'To date' is required"]
    if not data_dict.get("message"):
        errors["message"] = ["A 'Message' is required"]
    if errors:
        raise toolkit.ValidationError(errors)
