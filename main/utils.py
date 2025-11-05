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

def InttoRoman(num):
    """
    Converts an Integer to Roman Number
    num: An integer between 1 and 3999
    """
    if num is None:
        return "-"
    if not isinstance(num, int) or not (1 <= num <= 3999):
        return "Input must be an integer between 1 and 3999."

    roman_map = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'), 
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'), 
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]

    roman_numeral = ""
    for value, symbol in roman_map:
        while num >= value:
            roman_numeral += symbol
            num -= value
    return roman_numeral
