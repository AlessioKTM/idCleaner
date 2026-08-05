import socket

PORT = 53
PROVIDERS = {
    "cloudflare": ("1.1.1.1", PORT),
    "google": ("8.8.8.8", PORT)
}

def is_online(which: str = "cloudflare", timeout: float = 3, retries: int = 3, raise_on_error: bool = False) -> bool:
    host, port = PROVIDERS.get(which, PROVIDERS["cloudflare"])

    for _ in range(retries):
        try:
            with socket.create_connection((host, port), timeout):
                return True
        except OSError:
            pass

    if raise_on_error:
        raise ConnectionError("Network connection unavailable.")

    return False
