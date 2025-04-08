import ctypes
import sys
import threading
import time
from contextlib import contextmanager

from prefect import flow


@flow(timeout_seconds=5)
def main():
    """Original Prefect flow (expected to not timeout on Windows)."""
    print("--- Running Prefect Flow (Expected to NOT timeout on Windows) ---")
    start_time = time.monotonic()
    try:
        # Sleep longer than the @flow timeout
        time.sleep(6)
        end_time = time.monotonic()
        print(
            f"Prefect flow finished NORMALLY after {end_time - start_time:.2f} seconds."
        )
    except Exception as e:
        # On Windows, this likely won't be a timeout error from Prefect's sync cancel
        end_time = time.monotonic()
        print(
            f"Prefect flow caught exception {type(e).__name__} after {end_time - start_time:.2f} seconds."
        )
    print("------------------------------------------------------------------")


# --- Alternative Timeout Implementation using ctypes --- #


class TimeoutInterrupt(BaseException):
    """Exception raised specifically for our ctypes-based timeout."""

    pass


def _interrupt_thread(thread_ident: int):
    """Raise TimeoutInterrupt in the specified thread using ctypes."""
    # Attempt to raise TimeoutInterrupt in the target thread.
    # Returns the number of threads state modified.
    # If it returns 0, the thread_ident was invalid (thread finished?).
    # If it returns >1, something went wrong.
    # If it returns 1, the exception was scheduled.
    result = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(thread_ident), ctypes.py_object(TimeoutInterrupt)
    )
    if result > 1:
        # If more than one thread state was modified, it's an error.
        # Attempt to revert by setting the exception to NULL (0).
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread_ident), 0)
        print(
            f"Warning: PyThreadState_SetAsyncExc failed for thread {thread_ident}, result: {result}",
            file=sys.stderr,
        )
    # No action needed if result is 0 or 1. If 0, thread might be gone. If 1, it worked.


@contextmanager
def sync_timeout(seconds: float | None):
    """
    A context manager to enforce a timeout on synchronous code using ctypes.

    Uses a watcher thread to inject TimeoutInterrupt into the timed thread.
    Note: May not interrupt blocking C calls (e.g., time.sleep) immediately.
    """
    if seconds is None or seconds < 0:  # Negative timeout means no timeout
        yield
        return
    if seconds == 0:  # Zero timeout raises immediately
        raise TimeoutError("Code block timed out immediately (timeout=0 seconds)")

    target_thread_ident = threading.current_thread().ident
    if target_thread_ident is None:
        # Should not happen for a running thread, but defensively check.
        raise RuntimeError("Cannot apply timeout to a thread without an ID.")

    interrupt_event = threading.Event()  # Used to signal monitor thread to stop
    monitor_thread = None

    def _monitor():
        """Target function for the watcher thread."""
        # Wait for the specified timeout OR until the event is set
        if not interrupt_event.wait(timeout=seconds):
            # Event was NOT set, meaning the timeout duration elapsed.
            # print(f"Debug: Timeout triggered for thread {target_thread_ident}")
            try:
                _interrupt_thread(target_thread_ident)
            except ValueError:
                # This could happen if the thread ID became invalid, though unlikely.
                # print(f"Debug: Error interrupting thread {target_thread_ident} (ValueError)")
                pass  # Ignore if thread is already gone
        # else:
        # print(f"Debug: Monitor finished naturally for thread {target_thread_ident}")
        # Event was set, meaning the main block finished before timeout.

    try:
        monitor_thread = threading.Thread(
            target=_monitor,
            daemon=True,  # Allow program to exit even if monitor is stuck
            name=f"SyncTimeoutMonitor-{target_thread_ident}",
        )
        monitor_thread.start()
        yield  # Execute the 'with' block
    except TimeoutInterrupt:
        # Only raise TimeoutError if the monitor thread actually triggered the interrupt
        # (i.e., the interrupt_event wasn't set by the finally block finishing first)
        if not interrupt_event.is_set():
            raise TimeoutError(
                f"Code block timed out after {seconds} seconds"
            ) from None
        # If event IS set, it means we caught TimeoutInterrupt during cleanup/race condition, ignore it.
    finally:
        # print(f"Debug: Cleaning up timeout for thread {target_thread_ident}")
        # Ensure the monitor thread is signaled to exit
        interrupt_event.set()
        if monitor_thread and monitor_thread.is_alive():
            # Give the monitor thread a moment to exit cleanly
            monitor_thread.join(timeout=0.1)
            # if monitor_thread.is_alive():
            #     print(f"Warning: Monitor thread {monitor_thread.name} did not exit cleanly.", file=sys.stderr)


# --- Example Usage for sync_timeout ---


def potentially_long_running_task(duration: float):
    """Task that uses time.sleep()."""
    print(f"  Task started (sleep {duration}s)...", end="", flush=True)
    start = time.monotonic()
    try:
        time.sleep(duration)
        end = time.monotonic()
        print(f" finished normally after {end - start:.2f}s.")
    except BaseException as e:
        # Catch BaseException to see our custom TimeoutInterrupt
        end = time.monotonic()
        print(f" interrupted by {type(e).__name__} after {end - start:.2f}s.")
        raise  # Re-raise the caught exception


def cpu_bound_task(iterations: int):
    """Task that performs CPU work."""
    print(f"  CPU-bound task started ({iterations} iterations)...", end="", flush=True)
    start = time.monotonic()
    count = 0
    try:
        for i in range(iterations):
            count += i  # Simple Python work, GIL released periodically
        end = time.monotonic()
        print(f" finished normally after {end - start:.2f}s.")
    except BaseException as e:
        end = time.monotonic()
        print(f" interrupted by {type(e).__name__} after {end - start:.2f}s.")
        raise


# --- Main Execution ---

if __name__ == "__main__":
    # 1. Run the original Prefect flow
    # We expect this to NOT honor the timeout on Windows due to NullCancelScope

    try:
        main()
    except Exception as e:
        if sys.platform == "win32":
            print(f"  Caught expected exception: {type(e).__name__}: {e}")
        else:
            print(f"  Caught unexpected exception: {type(e).__name__}: {e}")

    # 2. Run examples using the ctypes-based sync_timeout
    print("\n--- Running sync_timeout Examples (Expected to work, with caveats) ---")
    print(f"Running on: {sys.platform}")

    print("\nTest 1: Task finishes before timeout")
    try:
        with sync_timeout(3):
            potentially_long_running_task(1)
    except TimeoutError as e:
        print(f"  Caught UNEXPECTED timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nTest 2: Task times out (using time.sleep)")
    try:
        # Note: time.sleep might not be interrupted exactly at 1s.
        # The exception is raised *after* sleep finishes or releases GIL.
        with sync_timeout(1):
            potentially_long_running_task(3)
    except TimeoutError as e:
        print(f"  Caught EXPECTED timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nTest 3: Task times out (CPU-bound)")
    try:
        # CPU-bound tasks are generally more responsive to this type of timeout.
        with sync_timeout(0.5):
            cpu_bound_task(300_000_000)  # Adjust count based on machine speed
    except TimeoutError as e:
        print(f"  Caught EXPECTED timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nTest 4: No timeout specified (None)")
    try:
        with sync_timeout(None):
            potentially_long_running_task(0.5)
        print("  Finished Test 4 successfully.")
    except TimeoutError as e:
        print(f"  Caught UNEXPECTED timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nTest 5: Zero timeout")
    try:
        with sync_timeout(0):
            print("  This line should NOT be printed.")
            potentially_long_running_task(1)
    except TimeoutError as e:
        print(f"  Caught EXPECTED immediate timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nTest 6: Negative timeout")
    try:
        with sync_timeout(-1):
            potentially_long_running_task(0.5)
        print("  Finished Test 6 successfully (negative treated as no timeout).")
    except TimeoutError as e:
        print(f"  Caught UNEXPECTED timeout: {e}")
    except Exception as e:
        print(f"  Caught other exception: {type(e).__name__}: {e}")

    print("\nScript finished.")
