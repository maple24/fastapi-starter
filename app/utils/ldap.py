"""
LDAP authentication utilities
Handles LDAP connection, authentication, and user information retrieval
"""

import ssl

from ldap3 import ALL, SUBTREE, Connection, Server, Tls
from ldap3.core.exceptions import LDAPBindError, LDAPException

from app.core.config import Settings


class LDAPAuthenticationError(Exception):
    """Custom exception for LDAP authentication errors"""


class LDAPConnectionError(Exception):
    """Custom exception for LDAP connection errors"""


def create_ldap_server(settings: Settings) -> Server:
    """
    Create and configure LDAP server connection

    Args:
        settings: Application settings containing LDAP configuration

    Returns:
        Configured LDAP Server instance

    Raises:
        LDAPConnectionError: If server configuration is invalid
    """
    if not settings.LDAP_SERVER:
        raise LDAPConnectionError("LDAP_SERVER is not configured")

    # Configure TLS if SSL is enabled
    tls_config = None
    if settings.LDAP_USE_SSL:
        tls_config = Tls(
            validate=ssl.CERT_REQUIRED,
            version=ssl.PROTOCOL_TLSv1_2,
        )

    try:
        server = Server(
            settings.LDAP_SERVER,
            port=settings.LDAP_PORT,
            use_ssl=settings.LDAP_USE_SSL,
            tls=tls_config,
            get_info=ALL,
            connect_timeout=settings.LDAP_TIMEOUT,
        )
        return server
    except Exception as e:
        raise LDAPConnectionError(f"Failed to create LDAP server: {str(e)}") from e


def _search_ldap_user(
    server: Server,
    settings: Settings,
    username: str,
) -> tuple[str, dict[str, str]] | None:
    """
    Search for user in LDAP directory

    Returns:
        Tuple of (user_dn, user_info) or None if not found
    """
    # First, bind with service account to search for user
    if settings.LDAP_BIND_DN and settings.LDAP_BIND_PASSWORD:
        bind_conn = Connection(
            server,
            user=settings.LDAP_BIND_DN,
            password=settings.LDAP_BIND_PASSWORD,
            auto_bind=True,
        )
    else:
        # Anonymous bind for search
        bind_conn = Connection(server, auto_bind=True)

    # Search for user
    search_filter = settings.LDAP_USER_FILTER.format(username=username)
    base_dn = settings.LDAP_BASE_DN or ""
    bind_conn.search(
        search_base=base_dn,
        search_filter=search_filter,
        search_scope=SUBTREE,
        attributes=[settings.LDAP_ATTR_EMAIL, settings.LDAP_ATTR_FULLNAME],
    )

    if not bind_conn.entries:
        bind_conn.unbind()
        return None

    # Get user DN
    user_entry = bind_conn.entries[0]
    user_dn = user_entry.entry_dn

    # Extract user attributes
    email = None
    full_name = None

    if hasattr(user_entry, settings.LDAP_ATTR_EMAIL):
        email_attr = getattr(user_entry, settings.LDAP_ATTR_EMAIL)
        if email_attr:
            email = str(email_attr.value)

    if hasattr(user_entry, settings.LDAP_ATTR_FULLNAME):
        fullname_attr = getattr(user_entry, settings.LDAP_ATTR_FULLNAME)
        if fullname_attr:
            full_name = str(fullname_attr.value)

    bind_conn.unbind()

    user_info = {
        "email": email or f"{username}@unknown",
        "full_name": full_name or username,
        "username": username,
    }

    return user_dn, user_info


def authenticate_ldap_user(
    username: str,
    password: str,
    settings: Settings,
) -> dict[str, str] | None:
    """
    Authenticate user against LDAP server and retrieve user information

    Args:
        username: Username to authenticate
        password: User password
        settings: Application settings containing LDAP configuration

    Returns:
        Dictionary containing user information (email, full_name) if authentication succeeds
        None if authentication fails

    Raises:
        LDAPConnectionError: If connection to LDAP server fails
        LDAPAuthenticationError: If LDAP authentication fails
    """
    if not settings.LDAP_ENABLED:
        raise LDAPAuthenticationError("LDAP authentication is not enabled")

    if not username or not password:
        return None

    try:
        # Create LDAP server
        server = create_ldap_server(settings)

        # Search for user
        search_result = _search_ldap_user(server, settings, username)
        if not search_result:
            return None

        user_dn, user_info = search_result

        # Now authenticate with user's credentials
        user_conn = Connection(
            server,
            user=user_dn,
            password=password,
            raise_exceptions=False,
        )

        if not user_conn.bind():
            return None

        user_conn.unbind()

        # Return user information
        return user_info

    except LDAPBindError as e:
        raise LDAPAuthenticationError(f"LDAP bind failed: {str(e)}") from e
    except LDAPException as e:
        raise LDAPConnectionError(f"LDAP error: {str(e)}") from e
    except Exception as e:
        raise LDAPAuthenticationError(f"Authentication error: {str(e)}") from e


def test_ldap_connection(settings: Settings) -> bool:
    """
    Test LDAP server connection

    Args:
        settings: Application settings containing LDAP configuration

    Returns:
        True if connection succeeds, False otherwise
    """
    try:
        server = create_ldap_server(settings)
        conn = Connection(server)
        result = conn.bind()
        conn.unbind()
        return result
    except Exception:
        return False
