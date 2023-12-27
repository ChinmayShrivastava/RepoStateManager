def get_tair_url() -> str:
    return environ.get("TAIR_URL", "redis://localhost:6379")
