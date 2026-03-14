from django import template
from .menu_groups import MENU_GROUPS

register = template.Library()


def _get_current_url_name(context):
    request = context.get('request')

    if not request:
        return None

    return getattr(
        getattr(request, 'resolver_match', None),
        'url_name',
        None
    )


def _matches_route_pattern(current_url_name, pattern):
    if pattern.endswith('*'):
        return current_url_name.startswith(pattern[:-1])
    return current_url_name == pattern


def _is_group_active(current_url_name, group_key):
    patterns = MENU_GROUPS.get(group_key, ())
    return any(_matches_route_pattern(current_url_name, pattern) for pattern in patterns)


@register.simple_tag(takes_context=True)
def active_menu(context, *url_names, css_class='active'):
    """
    Template tag to mark menu items as active based on current URL name.

    Usage:
        Single URL:
            {% active_menu 'home' %}
            {% active_menu 'profile' 'custom-active-class' %}

        Multiple URLs:
            {% active_menu 'students_list' 'students_add' 'students_edit' %}
            {% active_menu 'news_list' 'news_add' 'news_edit' 'active-link' %}

    Args:
        context: Django template context (automatic)
        *url_names: One or more URL names to check against current URL
        css_class: CSS class to return when active (default: 'active')

    Returns:
        The css_class if current URL matches any of the url_names, empty string otherwise.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    # If last argument looks like a custom CSS class (doesn't contain underscore/dash pattern of URL names)
    # and we have more than one argument, treat it as custom class
    if len(url_names) > 1 and ' ' not in url_names[-1] and '-' in url_names[-1]:
        # Could be a custom class if it's the only one with dashes and no underscores
        potential_class = url_names[-1]
        potential_urls = url_names[:-1]

        # Check if any of the potential URLs match
        if current_url_name in potential_urls:
            return potential_class
        elif current_url_name in url_names:
            # It wasn't a class, it was a URL name
            return css_class
    else:
        # Standard behavior: check if current URL is in the list
        if current_url_name in url_names:
            return css_class

    return ''


@register.simple_tag(takes_context=True)
def is_active(context, *url_names):
    """
    Template tag to check if current URL matches any of the given URL names.
    Returns True/False instead of CSS class.

    Usage:
        {% is_active 'home' as home_active %}
        {% if home_active %}...{% endif %}

        {% is_active 'students_list' 'students_add' as students_active %}

    Args:
        context: Django template context (automatic)
        *url_names: One or more URL names to check against current URL

    Returns:
        True if current URL matches any url_names, False otherwise.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return False

    return current_url_name in url_names


@register.simple_tag(takes_context=True)
def active_app(context, *app_names, css_class='active'):
    """
    Template tag to mark dropdown/section menus as active based on current app name.
    Perfect for making entire app sections active (e.g., dropdown menus).

    Usage:
        Single app:
            {% active_app 'estudante' %}
            {% active_app 'professor' 'menu-open' %}

        Multiple apps:
            {% active_app 'estudante' 'professor' %}
            {% active_app 'turma' 'disciplina' 'active-dropdown' %}

    Args:
        context: Django template context (automatic)
        *app_names: One or more app names to check against current app
        css_class: CSS class to return when active (default: 'active')

    Returns:
        The css_class if current app matches any of the app_names, empty string otherwise.
    """
    request = context.get('request')

    if not request:
        return ''

    # Get current app name from resolver_match
    current_app_name = getattr(
        getattr(request, 'resolver_match', None),
        'app_name',
        None
    )

    if not current_app_name:
        return ''

    # If last argument looks like a custom CSS class
    if len(app_names) > 1 and ' ' not in app_names[-1] and '-' in app_names[-1]:
        potential_class = app_names[-1]
        potential_apps = app_names[:-1]

        if current_app_name in potential_apps:
            return potential_class
        elif current_app_name in app_names:
            return css_class
    else:
        if current_app_name in app_names:
            return css_class

    return ''


@register.simple_tag(takes_context=True)
def is_active_app(context, *app_names):
    """
    Template tag to check if current app matches any of the given app names.
    Returns True/False. Useful for conditional logic in dropdown menus.

    Usage:
        {% is_active_app 'estudante' as student_section %}
        {% if student_section %}
            <ul class="dropdown-menu show">...</ul>
        {% endif %}

        {% is_active_app 'estudante' 'professor' as academic_section %}

    Args:
        context: Django template context (automatic)
        *app_names: One or more app names to check against current app

    Returns:
        True if current app matches any app_names, False otherwise.
    """
    request = context.get('request')

    if not request:
        return False

    current_app_name = getattr(
        getattr(request, 'resolver_match', None),
        'app_name',
        None
    )

    if not current_app_name:
        return False

    return current_app_name in app_names


@register.simple_tag(takes_context=True)
def menu_open(context, *url_names):
    """
    Template tag for AdminLTE dropdown menus - adds 'menu-open' class when any child URL is active.
    Perfect for keeping parent menus expanded when viewing child pages.

    Usage:
        For Horariu dropdown with children (loron, horas, etc):
            <li class="nav-item {% menu_open 'horariu_list' 'loron_list' 'loron_detail' 'horas_list' 'horas_detail' %}">

        For Professor dropdown:
            <li class="nav-item {% menu_open 'professor_list' 'professor_detail' 'professorclasse_list' %}">

    Args:
        context: Django template context (automatic)
        *url_names: All URL names belonging to this menu section (parent + children)

    Returns:
        'menu-open' if current URL matches any url_names, empty string otherwise.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    return 'menu-open' if current_url_name in url_names else ''


@register.simple_tag(takes_context=True)
def active_or_open(context, *url_names):
    """
    Combined tag that returns 'active' for direct match, 'menu-open' for parent with active child.
    Useful for dropdown parent links that should be highlighted when any child is active.

    Usage:
        <a href="#" class="nav-link {% active_or_open 'horariu_list' 'loron_list' 'horas_list' %}">

    Args:
        context: Django template context (automatic)
        *url_names: All URL names for this menu item and its children

    Returns:
        'active' if current URL matches any url_names, empty string otherwise.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    return 'active' if current_url_name in url_names else ''


@register.simple_tag(takes_context=True)
def active_group(context, group_key, css_class='active'):
    """
    Template tag to mark a menu item as active based on a named route group.

    Usage:
        {% active_group 'nav.estudante.valor' %}
        {% active_group 'nav.estudante.valor' 'custom-active' %}
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    return css_class if _is_group_active(current_url_name, group_key) else ''


@register.simple_tag(takes_context=True)
def menu_open_group(context, group_key):
    """
    Template tag for AdminLTE parent menu expansion based on a named route group.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    return 'menu-open' if _is_group_active(current_url_name, group_key) else ''


@register.simple_tag(takes_context=True)
def active_or_open_group(context, group_key):
    """
    Template tag for parent nav-link highlighting based on a named route group.
    """
    current_url_name = _get_current_url_name(context)

    if not current_url_name:
        return ''

    return 'active' if _is_group_active(current_url_name, group_key) else ''
