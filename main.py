from threading import Thread, Event
from queue import Queue
from pathlib import Path
import os, sys

from src import init
from src.utils import handle_threads, THREAD_NAMES
from src.workers import load, mail
from tools.network.network import is_online
from tools.recorder.recorder import Recorder

BOOTSTRAP_SEQUENCE = [
    (is_online, {"raise_on_error": True}),
    (init.api, {}),
    (init.data, {}),
    (init.recorders, {})
]
_PRINT = True


def main():
    record = Recorder(Path(os.getenv("recorder_main_path")), _print=_PRINT)
    stopper = Event()
    queue_mail, queue_update = Queue(), Queue()

    json_loader = Thread(
        name = THREAD_NAMES[0],
        target = load.json_data,
        daemon = True,
        args = (stopper, queue_mail, queue_update)
    )

    mail_worker = Thread(
        name = THREAD_NAMES[1],
        target = mail.worker,
        daemon = True,
        args = (stopper, queue_mail, queue_update)
    )

    handle_threads([json_loader, mail_worker], stopper, record)
# ========== ==========

if __name__ == "__main__":
    with Recorder(Path(__file__).parent / "records" / "bootstrap.json", _print=_PRINT) as rec:
        for func, kwargs in BOOTSTRAP_SEQUENCE:
            try:
                func(**kwargs)
            except Exception as e:
                err_msg = f"Bootstrap failed during '{func.__name__}': {e}"
                rec.write(err_msg)
                sys.stderr.write(f"{err_msg}\n")
                sys.exit(1)

    main()
