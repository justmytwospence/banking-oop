import logging

logger = logging.getLogger(__name__)


def split_name(name):
    try:
        names = name.split(" ")
        assert len(names) == 2
        return names[0], names[1]
    except Exception as e:
        logger.error(f"Only one first and last name supported.")
        return None
