# permissions.py
"""
System-wide permissions definitions for CalmPOS.
Each permission is an instance of the Permission class, with a unique slug, name, description, and related module.
"""

from dataclasses import dataclass
from typing import Optional, List, Dict

@dataclass(frozen=True)
class Permission:
    """
    Represents a system permission.
    :param slug: Unique ALL_CAPS_WITH_UNDERSCORES string identifier for the permission.
    :param name: Human-readable name for the permission.
    :param description: Description of what the permission allows.
    :param module: The module or app this permission is related to.
    """
    slug: str
    name: str
    description: str
    module: str

class Permissions:
    ACCESS_USER_MANAGEMENT = "ACCESS_USER_MANAGEMENT"
    CREATE_USER = "CREATE_USER"
    UPDATE_USER = "UPDATE_USER"
    DELETE_USER = "DELETE_USER"
    VIEW_USER = "VIEW_USER"
    PROCESS_SALES = "PROCESS_SALES"
    MANAGE_INVENTORY = "MANAGE_INVENTORY"
    # Add more as needed

PERMISSIONS: Dict[str, Permission] = {
    Permissions.ACCESS_USER_MANAGEMENT: Permission(
        slug=Permissions.ACCESS_USER_MANAGEMENT,
        name="Access User Management",
        description="Access the user management module.",
        module="accounts"
    ),
    Permissions.CREATE_USER: Permission(
        slug=Permissions.CREATE_USER,
        name="Create User",
        description="Create new user accounts.",
        module="accounts"
    ),
    Permissions.UPDATE_USER: Permission(
        slug=Permissions.UPDATE_USER,
        name="Update User",
        description="Update existing user accounts.",
        module="accounts"
    ),
    Permissions.DELETE_USER: Permission(
        slug=Permissions.DELETE_USER,
        name="Delete User",
        description="Delete user accounts.",
        module="accounts"
    ),
    Permissions.VIEW_USER: Permission(
        slug=Permissions.VIEW_USER,
        name="View User",
        description="View user accounts and details.",
        module="accounts"
    ),
    Permissions.PROCESS_SALES: Permission(
        slug=Permissions.PROCESS_SALES,
        name="Process Sales",
        description="Process sales transactions at the POS.",
        module="sales"
    ),
    Permissions.MANAGE_INVENTORY: Permission(
        slug=Permissions.MANAGE_INVENTORY,
        name="Manage Inventory",
        description="Add, update, or delete inventory items.",
        module="inventory"
    ),
    # Add more as needed
}

def get_permission(slug: str) -> Optional[Permission]:
    """
    Retrieve a Permission object by its slug.
    :param slug: The ALL_CAPS_WITH_UNDERSCORES permission slug.
    :return: Permission object if found, else None.
    """
    return PERMISSIONS.get(slug)

def get_permission_by_slug(slug: str) -> Optional[Permission]:
    """
    Alias for get_permission. Provided for compatibility.
    :param slug: The permission slug.
    :return: Permission object if found, else None.
    """
    return get_permission(slug)

def list_all_permissions() -> List[Permission]:
    """
    List all defined Permission objects.
    :return: List of all Permission objects.
    """
    return list(PERMISSIONS.values())

def list_permissions_by_module(module: str) -> List[Permission]:
    """
    List all permissions for a given module/app.
    :param module: The module name (e.g., 'accounts', 'sales').
    :return: List of Permission objects for the module.
    """
    return [perm for perm in PERMISSIONS.values() if perm.module == module]

def is_valid_permission_slug(slug: str) -> bool:
    """
    Check if a slug is a valid, defined permission.
    :param slug: The permission slug to check.
    :return: True if the slug is valid, else False.
    """
    return slug in PERMISSIONS 