import logging

from rich.logging import RichHandler

from genai_bench.logging import LoggingManager


def test_headless_mode_no_console_handler(monkeypatch, tmp_path):
    """Test that HEADLESS=true results in no console handlers."""
    monkeypatch.setenv("HEADLESS", "true")

    # Create LoggingManager for benchmark with temp log dir
    _ = LoggingManager("benchmark", layout=None, live=None, log_dir=str(tmp_path))

    root_logger = logging.getLogger()
    console_handlers = [
        h
        for h in root_logger.handlers
        if isinstance(h, (logging.StreamHandler, RichHandler))
        and not isinstance(h, logging.FileHandler)
        and type(h).__name__
        not in ["LogCaptureHandler", "WorkerRichHandler"]  # Exclude test handlers
    ]

    assert (
        len(console_handlers) == 0
    ), "Should have no console handlers in headless mode"

    # Verify file handler exists
    file_handlers = [
        h for h in root_logger.handlers if isinstance(h, logging.FileHandler)
    ]
    assert len(file_handlers) > 0, "Should have file handler"


def test_enable_ui_false_has_console_handler(monkeypatch, tmp_path):
    """Test that ENABLE_UI=false still has console handler (backward compat)."""
    monkeypatch.setenv("ENABLE_UI", "false")
    monkeypatch.setenv("HEADLESS", "false")  # Explicitly set to false

    # Reset logging to clean state
    logging.root.handlers = []

    _ = LoggingManager("benchmark", layout=None, live=None, log_dir=str(tmp_path))

    root_logger = logging.getLogger()
    console_handlers = [
        h
        for h in root_logger.handlers
        if isinstance(h, logging.StreamHandler)
        and not isinstance(h, logging.FileHandler)
        and type(h).__name__
        not in ["LogCaptureHandler", "WorkerRichHandler"]  # Exclude test handlers
    ]

    assert len(console_handlers) > 0, "ENABLE_UI=false should keep console logging"


def test_headless_overrides_enable_ui(monkeypatch, tmp_path):
    """Test that HEADLESS=true overrides ENABLE_UI=true."""
    monkeypatch.setenv("HEADLESS", "true")
    monkeypatch.setenv("ENABLE_UI", "true")

    # Reset logging to clean state
    logging.root.handlers = []

    _ = LoggingManager("benchmark", layout=None, live=None, log_dir=str(tmp_path))

    root_logger = logging.getLogger()
    console_handlers = [
        h
        for h in root_logger.handlers
        if isinstance(h, (logging.StreamHandler, RichHandler))
        and not isinstance(h, logging.FileHandler)
        and type(h).__name__
        not in ["LogCaptureHandler", "WorkerRichHandler"]  # Exclude test handlers
    ]

    assert len(console_handlers) == 0, "HEADLESS should override ENABLE_UI"
