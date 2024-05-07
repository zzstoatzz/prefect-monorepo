import pytest
from prefect import flow


def success_hook(flow, flow_run, state):
    print("hook called")


def fail_hook(flow, flow_run, state):
    print("hook called")


@flow(on_completion=[success_hook], on_failure=[fail_hook])
def foo(should_fail: bool = False):
    if should_fail:
        raise ValueError("foo failed")


def test_hooks_called(caplog):
    with caplog.at_level("INFO"):
        foo()
        assert "Running hook 'success_hook'" in caplog.text

    with caplog.at_level("INFO"):
        with pytest.raises(ValueError, match="foo failed"):
            foo(should_fail=True)
        assert "Running hook 'fail_hook'" in caplog.text
