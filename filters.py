# filters.py
# Helper functions for filtering (mainly used by logger, but kept separate for organization)

# This file is mostly a placeholder since filtering logic is in logger.py
# But we keep it for project structure completeness


def validate_ip(ip_string):
    """Basic IP validation"""
    if not ip_string or ip_string.strip() == "":
        return True

    parts = ip_string.split(".")
    if len(parts) != 4:
        return False
    try:
        for part in parts:
            if int(part) < 0 or int(part) > 255:
                return False
        return True
    except ValueError:
        return False
