"""Tests for the build_env_epilog helper in cli.py."""

from workspace_cli.cli import build_env_epilog


def test_build_env_epilog_all_vars_when_no_command():
    """build_env_epilog(None) returns all three env vars."""
    epilog = build_env_epilog(None)
    assert "WORKSPACE_CATALOG_URL" in epilog
    assert "WORKSPACE_SKIP_UPDATE" in epilog
    assert "WORKSPACE_DEBUG_UPDATE" in epilog


def test_build_env_epilog_setup_devcontainer_includes_catalog_url():
    """setup-devcontainer shows WORKSPACE_CATALOG_URL plus globals."""
    epilog = build_env_epilog("setup-devcontainer")
    assert "WORKSPACE_CATALOG_URL" in epilog
    assert "WORKSPACE_SKIP_UPDATE" in epilog
    assert "WORKSPACE_DEBUG_UPDATE" in epilog


def test_build_env_epilog_catalog_includes_catalog_url():
    """catalog shows WORKSPACE_CATALOG_URL plus globals."""
    epilog = build_env_epilog("catalog")
    assert "WORKSPACE_CATALOG_URL" in epilog
    assert "WORKSPACE_SKIP_UPDATE" in epilog
    assert "WORKSPACE_DEBUG_UPDATE" in epilog


def test_build_env_epilog_code_only_globals():
    """code command shows only global env vars."""
    epilog = build_env_epilog("code")
    assert "WORKSPACE_CATALOG_URL" not in epilog
    assert "WORKSPACE_SKIP_UPDATE" in epilog
    assert "WORKSPACE_DEBUG_UPDATE" in epilog


def test_build_env_epilog_template_only_globals():
    """template command shows only global env vars."""
    epilog = build_env_epilog("template")
    assert "WORKSPACE_CATALOG_URL" not in epilog
    assert "WORKSPACE_SKIP_UPDATE" in epilog
    assert "WORKSPACE_DEBUG_UPDATE" in epilog


def test_build_env_epilog_starts_with_header():
    """Epilog starts with 'environment variables:' header."""
    epilog = build_env_epilog(None)
    assert epilog.startswith("environment variables:")


def test_build_env_epilog_descriptions_present():
    """Each env var line includes its description."""
    epilog = build_env_epilog(None)
    assert "Override the default catalog repository URL" in epilog
    assert "disable automatic update checks" in epilog
    assert "debug logging for update checks" in epilog
