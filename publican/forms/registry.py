"""The registry of all installed forms."""

def all_forms():
    """So, not actually a registry at this point, by a long shot."""
    from .us import form_940, form_941
    return [form_940, form_941]
