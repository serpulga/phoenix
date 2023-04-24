from unittest.mock import Mock, patch

from phoenix.services.parallel import executor_pool


def test_executor_pool():
    SENTINEL = "SENTINEL"
    with patch("main.app.state") as mock_appstate:
        mock_appstate.configure_mock(executor_pool=SENTINEL)

        assert executor_pool() == SENTINEL
