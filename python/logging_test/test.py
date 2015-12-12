#!/usr/bin/env python
"""Testing how Loggers are referenced."""
import logging


def get_log1():
    """Get a logger.

    Returns:
        Logger object.
    """
    return logging.getLogger(__name__)


def get_log2():
    """Get a second logger.

    Returns:
        Logger object.
    """
    return logging.getLogger(__name__)


def main():
    """Main."""
    logging.basicConfig()

    log = logging.getLogger(__name__)

    log1 = get_log1()
    log2 = get_log2()

    assert log == log1
    assert log == log2
    assert log1 == log2


if __name__ == '__main__':
    main()
