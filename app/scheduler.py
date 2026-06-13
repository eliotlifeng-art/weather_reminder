import threading
import time
from datetime import datetime


class ReminderScheduler:
    def __init__(self, db):
        self.db = db
        self._running = False
        self._thread = None
        self._callback = None
        self._notified_today = set()

    def set_callback(self, callback):
        self._callback = callback

    def start(self):
        if self._running:
            return
        self._running = True
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()

    def stop(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=2)

    def _run(self):
        while self._running:
            now = datetime.now()
            current_key = f"{now.hour}:{now.minute}"

            if now.hour == 0 and now.minute == 0:
                self._notified_today.clear()

            reminders = self.db.get_reminders()
            for r in reminders:
                if not r["enabled"]:
                    continue
                r_key = f"{r['hour']}:{r['minute']}"
                if r_key == current_key and r_key not in self._notified_today:
                    self._notified_today.add(r_key)
                    if self._callback:
                        self._callback(r)

            time.sleep(30)

    def trigger_now(self):
        if self._callback:
            self._callback({"hour": -1, "minute": -1, "label": "manual"})
