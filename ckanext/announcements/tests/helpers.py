def get_user_env(user_dict):
    """Get the environment to use for a given user."""
    return {"Authorization": user_dict["token"]}
