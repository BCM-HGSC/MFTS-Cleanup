from datetime import date

from pytest import mark

from mftscleanup import __main__
from helpers import FakeShare


def test_auto_cleanup_shares_no_shares(scenario: FakeShare):
    """
    There are no shares.
    Invoke the top-level main function from within the pytest process.
    """
    today_str = date.today().isoformat()
    argv = [
        "auto",
        str(scenario.metadata_root),
    ]
    __main__.main(argv)


@mark.xfail(raises=NotImplementedError)
def test_auto_cleanup_shares_smoke(rt1234_initial: FakeShare):
    """
    There is one active share.
    Invoke the top-level main function from within the pytest process.
    """
    today_str = date.today().isoformat()
    argv = [
        "auto",
        str(rt1234_initial.scenario.metadata_root),
    ]
    __main__.main(argv)
    # TODO: Test side effects.
