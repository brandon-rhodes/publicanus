"""The registry of all installed forms."""

def all_forms():
    """So, not actually a registry at this point, by a long shot."""
    from .us import irs_941
    return [irs_941]
