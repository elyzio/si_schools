from django import template

register = template.Library()


@register.simple_tag
def user_group(user):
    """
    Get user's primary group/role.
    Priority: Admin > Director > Secretaria > Professor > Estudante
    """
    if not user.is_authenticated:
        return 'guest'

    if user.is_superuser:
        return 'admin'

    if user.groups.filter(name='admin').exists():
        return 'admin'
    elif user.groups.filter(name='director').exists():
        return 'director'
    elif user.groups.filter(name='secretaria').exists():
        return 'secretaria'
    elif user.groups.filter(name='professor').exists():
        return 'professor'
    elif user.groups.filter(name='estudante').exists():
        return 'estudante'

    return 'default'


@register.filter
def has_group(user, group_name):
    """
    Check if user belongs to a specific group.
    Usage: {% if request.user|has_group:"Admin" %}
    """
    if not user.is_authenticated:
        return False
    return user.groups.filter(name=group_name).exists()


@register.simple_tag
def is_admin(user):
    """Check if user is admin"""
    return user.is_authenticated and (user.is_superuser or user.groups.filter(name='admin').exists())


@register.simple_tag
def is_director(user):
    """Check if user is director"""
    return user.is_authenticated and user.groups.filter(name='director').exists()


@register.simple_tag
def is_secretaria(user):
    """Check if user is secretaria"""
    return user.is_authenticated and user.groups.filter(name='secretaria').exists()


@register.simple_tag
def is_professor(user):
    """Check if user is professor"""
    return user.is_authenticated and user.groups.filter(name='professor').exists()


@register.simple_tag
def is_estudante(user):
    """Check if user is estudante"""
    return user.is_authenticated and user.groups.filter(name='estudante').exists()
