from hellraiser_trainer.utils.job_queue import JobQueue


def test_register_and_drain_updates_state():
    q = JobQueue()
    q.register("read", lambda: {"health": 100, "pins": 3})
    q.dispatch("read")
    q.drain()
    assert q.last_state() == {"health": 100, "pins": 3}


def test_dispatch_unknown_job_is_noop():
    q = JobQueue()
    q.dispatch("missing")
    q.drain()
    assert q.last_state() == {}