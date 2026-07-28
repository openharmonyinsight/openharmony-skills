#!/usr/bin/env python3
"""
File locking utility for concurrent batch writes.

Usage:
    from batch_lock import FileLock

    with FileLock('completed.json.lock', timeout=30):
        data = load_json('completed.json')
        data['new_key'] = 'new_value'
        save_json('completed.json', data)
"""

import os
import time
import sys

if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')


class FileLock:
    def __init__(self, lock_path, timeout=30, poll_interval=0.1):
        self.lock_path = lock_path
        self.timeout = timeout
        self.poll_interval = poll_interval
        self._acquired = False

    def acquire(self):
        deadline = time.time() + self.timeout
        while time.time() < deadline:
            try:
                fd = os.open(self.lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(fd, f"{os.getpid()}\n{time.time()}\n".encode())
                os.close(fd)
                self._acquired = True
                return
            except FileExistsError:
                try:
                    mtime = os.path.getmtime(self.lock_path)
                    if time.time() - mtime > self.timeout:
                        os.remove(self.lock_path)
                        continue
                except FileNotFoundError:
                    continue
            time.sleep(self.poll_interval)
        raise TimeoutError(f"Could not acquire lock: {self.lock_path}")

    def release(self):
        if self._acquired:
            try:
                os.remove(self.lock_path)
            except FileNotFoundError:
                pass
            self._acquired = False

    def __enter__(self):
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()
        return False
