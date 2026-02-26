# Active Menu Template Tags - Usage Guide

## Available Template Tags

Your project has custom template tags in `main/templatetags/active_menu.py` for handling active menu states.

---

## 1. `{% active_menu %}` - Single Menu Items

**Purpose**: Adds 'active' class to a menu link when on that page.

**Usage**:
```django
{% load active_menu %}

<!-- Single URL -->
<a href="{% url 'professor_list' %}" class="nav-link {% active_menu 'professor_list' %}">
    Professor
</a>

<!-- Multiple URLs (active for list, detail, create, update pages) -->
<a href="{% url 'estudante_list' %}" class="nav-link {% active_menu 'estudante_list' 'estudante_detail' 'estudante_create' 'estudante_update' %}">
    Estudante
</a>
```

---

## 2. `{% menu_open %}` - Dropdown Parent Items

**Purpose**: Adds 'menu-open' class to keep dropdown expanded when viewing child pages.

**Usage**:
```django
<!-- Horariu dropdown - stays open when viewing any horariu-related page -->
<li class="nav-item {% menu_open 'horariu_list' 'horariu_detail' 'loron_list' 'loron_detail' 'horas_list' 'horas_detail' 'horariuexame_list' 'horariuvalor_list' %}">
    <a href="#" class="nav-link">
        <i class="nav-icon fas fa-calendar"></i>
        <p>Horariu <i class="right fas fa-angle-left"></i></p>
    </a>
    <ul class="nav nav-treeview">
        <!-- Child menu items -->
    </ul>
</li>
```

---

## 3. `{% active_or_open %}` - Parent Link Highlighting

**Purpose**: Highlights parent menu link when any child page is active.

**Usage**:
```django
<li class="nav-item {% menu_open 'horariu_list' 'loron_list' 'horas_list' %}">
    <!-- Parent link gets 'active' class when any child is active -->
    <a href="#" class="nav-link {% active_or_open 'horariu_list' 'loron_list' 'horas_list' %}">
        <i class="nav-icon fas fa-calendar"></i>
        <p>Horariu <i class="right fas fa-angle-left"></i></p>
    </a>
    <ul class="nav nav-treeview">
        <li class="nav-item">
            <a href="{% url 'loron_list' %}" class="nav-link {% active_menu 'loron_list' 'loron_detail' %}">
                <i class="far fa-circle nav-icon"></i>
                <p>Loron</p>
            </a>
        </li>
    </ul>
</li>
```

---

## Complete Sidebar Example

```django
{% load active_menu %}

<aside class="main-sidebar sidebar-dark-primary elevation-4">
    <div class="sidebar">
        <nav class="mt-2">
            <ul class="nav nav-pills nav-sidebar flex-column" data-widget="treeview" role="menu">

                <!-- Single Menu Item (No Dropdown) -->
                <li class="nav-item">
                    <a href="{% url 'professor_list' %}" class="nav-link {% active_menu 'professor_list' 'professor_detail' 'professor_create' 'professor_update' 'professor_delete' %}">
                        <i class="nav-icon fas fa-chalkboard-teacher"></i>
                        <p>Professor</p>
                    </a>
                </li>

                <!-- Single Menu Item -->
                <li class="nav-item">
                    <a href="{% url 'estudante_list' %}" class="nav-link {% active_menu 'estudante_list' 'estudante_detail' 'estudante_create' 'estudante_update' %}">
                        <i class="nav-icon fas fa-user-graduate"></i>
                        <p>Estudante</p>
                    </a>
                </li>

                <!-- Dropdown Menu -->
                <li class="nav-item {% menu_open 'horariu_list' 'horariu_detail' 'horariu_create' 'loron_list' 'loron_detail' 'loron_create' 'horas_list' 'horas_detail' 'horas_create' 'horariuexame_list' 'horariuexame_detail' 'horariuvalor_list' 'horariuvalor_detail' %}">
                    <a href="#" class="nav-link {% active_or_open 'horariu_list' 'horariu_detail' 'loron_list' 'loron_detail' 'horas_list' 'horas_detail' 'horariuexame_list' 'horariuvalor_list' %}">
                        <i class="nav-icon fas fa-calendar-alt"></i>
                        <p>
                            Horariu
                            <i class="right fas fa-angle-left"></i>
                        </p>
                    </a>
                    <ul class="nav nav-treeview">
                        <li class="nav-item">
                            <a href="{% url 'horariu_list' %}" class="nav-link {% active_menu 'horariu_list' 'horariu_detail' 'horariu_create' 'horariu_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Horariu</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'loron_list' %}" class="nav-link {% active_menu 'loron_list' 'loron_detail' 'loron_create' 'loron_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Loron</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'horas_list' %}" class="nav-link {% active_menu 'horas_list' 'horas_detail' 'horas_create' 'horas_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Oras</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'horariuexame_list' %}" class="nav-link {% active_menu 'horariuexame_list' 'horariuexame_detail' 'horariuexame_create' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Exame</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'horariuvalor_list' %}" class="nav-link {% active_menu 'horariuvalor_list' 'horariuvalor_detail' 'horariuvalor_create' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Valor</p>
                            </a>
                        </li>
                    </ul>
                </li>

                <!-- Dadus Dropdown -->
                <li class="nav-item {% menu_open 'distrito_list' 'subdistrito_list' 'suco_list' 'aldeia_list' 'ano_list' 'periodo_list' 'departamentu_list' 'classe_list' 'turma_list' 'materia_list' %}">
                    <a href="#" class="nav-link {% active_or_open 'distrito_list' 'subdistrito_list' 'suco_list' 'aldeia_list' 'ano_list' 'periodo_list' 'departamentu_list' 'classe_list' 'turma_list' 'materia_list' %}">
                        <i class="nav-icon fas fa-database"></i>
                        <p>
                            Dadus
                            <i class="right fas fa-angle-left"></i>
                        </p>
                    </a>
                    <ul class="nav nav-treeview">
                        <li class="nav-item">
                            <a href="{% url 'distrito_list' %}" class="nav-link {% active_menu 'distrito_list' 'distrito_create' 'distrito_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Distritu</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'classe_list' %}" class="nav-link {% active_menu 'classe_list' 'classe_create' 'classe_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Klase</p>
                            </a>
                        </li>
                        <li class="nav-item">
                            <a href="{% url 'materia_list' %}" class="nav-link {% active_menu 'materia_list' 'materia_create' 'materia_update' %}">
                                <i class="far fa-circle nav-icon"></i>
                                <p>Materia</p>
                            </a>
                        </li>
                    </ul>
                </li>

                <!-- Valor Menu -->
                <li class="nav-item">
                    <a href="{% url 'valor_list' %}" class="nav-link {% active_menu 'valor_list' 'valor_create' 'valor_update' 'estudante_valor_detail' 'valor_graph' %}">
                        <i class="nav-icon fas fa-star"></i>
                        <p>Valor</p>
                    </a>
                </li>

            </ul>
        </nav>
    </div>
</aside>
```

---

## Important Notes

1. **Always load the tag**: Put `{% load active_menu %}` at the top of your sidebar template

2. **List all related URLs**: Include all URL names for CRUD operations:
   - `list`, `detail`, `create`, `update`, `delete`
   - This ensures menu stays active on all related pages

3. **AdminLTE Classes**:
   - `active` - highlights the current menu item
   - `menu-open` - keeps dropdown expanded

4. **For dropdowns**, you need BOTH tags:
   - `{% menu_open %}` on the `<li class="nav-item">` to expand dropdown
   - `{% active_or_open %}` on the `<a class="nav-link">` to highlight parent link
   - `{% active_menu %}` on each child link

---

## Quick Reference

| Tag | Where to Use | Purpose |
|-----|-------------|---------|
| `{% active_menu 'url1' 'url2' %}` | Single menu links (`<a>`) | Highlights current page |
| `{% menu_open 'url1' 'url2' %}` | Dropdown parent (`<li>`) | Keeps dropdown expanded |
| `{% active_or_open 'url1' 'url2' %}` | Dropdown parent link (`<a>`) | Highlights parent when child active |

---

## Testing

After implementing, test by:
1. Visiting a page (e.g., `/horariu/loron/`)
2. Check sidebar - "Horariu" dropdown should be expanded
3. "Loron" link should have blue/active styling
4. Parent "Horariu" link should also be highlighted

---

Generated: 2025-02-25
