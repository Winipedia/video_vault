"""module."""

import pytest


@pytest.mark.skip(reason="skipping bc build is not easy to test")
def test_do_build() -> None:
    """Test func for build."""
    raise NotImplementedError
