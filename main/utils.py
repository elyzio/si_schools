def get_user_group(user):
    """
    Get the primary group name for a user.
    Returns the first group name if user has groups, otherwise None.
    """
    if user.is_authenticated and user.groups.exists():
        return user.groups.first().name
    return None


def get_user_groups(user):
    """
    Get all group names for a user.
    Returns a list of group names.
    """
    if user.is_authenticated:
        return list(user.groups.values_list('name', flat=True))
    return []


def is_user_in_group(user, group_name):
    """
    Check if user belongs to a specific group.

    Args:
        user: Django User object
        group_name: String name of the group

    Returns:
        Boolean indicating if user is in the group
    """
    if user.is_authenticated:
        return user.groups.filter(name=group_name).exists()
    return False


def get_user_role(user):
    """
    Get the user's role based on their group.
    Priority order: Admin > Director > Secretaria > Professor > Estudante

    Returns:
        String: 'admin', 'director', 'secretaria', 'professor', 'estudante', or None
    """
    if not user.is_authenticated:
        return None

    if user.is_superuser:
        return 'admin'

    # Define priority order
    role_priority = ['Admin', 'Director', 'Secretaria', 'Professor', 'Estudante']

    user_groups = user.groups.values_list('name', flat=True)

    for role in role_priority:
        if role in user_groups:
            return role.lower()

    return None
