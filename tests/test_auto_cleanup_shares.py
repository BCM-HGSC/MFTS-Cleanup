from datetime import date

from pytest import mark

from mftscleanup.__main__ import main
from mftscleanup.cleanup import process_active_shares
from helpers import FakeShare, Scenario


def test_auto_cleanup_shares_no_shares(scenario: Scenario):
    """
    There are no shares.
    Invoke the top-level main function from within the pytest process.
    """
    today_str = date.today().isoformat()
    argv = [
        "auto",
        str(scenario.metadata_root),
    ]
    main(argv)


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
    main(argv)
    # TODO: Test side effects.


@mark.xfail(raises=NotImplementedError)
def test_process_active_shares_smoke(rt1234_initial: FakeShare):
    """
    There is one active share.
    Invoke the top-level main function from within the pytest process.
    """
    today = date.today()
    metadata_store = rt1234_initial.scenario.metadata_store
    process_active_shares(metadata_store, today, True)
    # TODO: Test side effects.
