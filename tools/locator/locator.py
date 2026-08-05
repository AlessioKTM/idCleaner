from pathlib import Path

TO_IGNORE = [".git", "venv", ".venv", "__pycache__", "docker"]


def locate_file(target: str, mark: str = "main.py", current_dir = None, exclude = None) -> Path | None:
    root = _get_root(mark)
    target = _get_target(target)
    current_dir = _get_current_dir(current_dir, mark)

    try:
        for el in current_dir.iterdir():
            if el in TO_IGNORE + [exclude]:
                continue

            if el.name == target:
                return el

            if el.is_dir():
                r = locate_file(target, mark, current_dir=el, exclude=exclude)
                if r: return r

    except (PermissionError, FileNotFoundError):
        pass

    return None
# ========== ========== ==========

def _get_current_dir(current_dir, mark):
    if current_dir is None:
        return _get_root(mark)
    else:
        return Path(current_dir)

def _get_target(target):
    if isinstance(target, Path):
        return str(target)
    return str(target)

def _get_root(mark: str) -> Path:
    start = Path.cwd().resolve()

    if (start / mark).is_file():
        return start

    for parent in start.parents:
        if (parent / mark).is_file():
            return parent

    return start
