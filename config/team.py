TEAM_ROSTER = [
    {
        "name": "Manoj Kumar",
        "aliases": ["mk", "kumar", "manoj"],
        "github_username": "Manoj Kumar",
        "linear_display_name": "Manoj Kumar",
        "role": "Lead Engineer"
    },
    {
        "name": "Divya Krishna Salian",
        "aliases": ["divya", "dsalian", "dks"],
        "github_username": "dsalian",
        "linear_display_name": "Divya Krishna Salian",
        "role": "Engineer"
    }
]

def resolve_identity(name_or_alias: str) -> dict | None:
    """Given any alias, return the full team member profile."""
    query = name_or_alias.lower().strip()
    for member in TEAM_ROSTER:
        if query == member["name"].lower():
            return member
        if query in [a.lower() for a in member["aliases"]]:
            return member
    return None

def get_all_identities(name_or_alias: str) -> dict | None:
    """Return all platform identities for a person."""
    member = resolve_identity(name_or_alias)
    if not member:
        return None
    return {
        "name": member["name"],
        "github": member["github_username"],
        "linear": member["linear_display_name"]
    }