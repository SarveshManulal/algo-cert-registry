import pytest
from algopy import Bytes, arc4
from algopy_testing import algopy_testing_context

from smart_contracts.cert_registry.contract import CertRegistry


def test_creator_can_issue_and_verify_a_certificate() -> None:
    with algopy_testing_context() as context:
        contract = CertRegistry()
        digest = Bytes(b"a" * 32)
        holder = arc4.String("Ada Lovelace")

        contract.issue(digest, holder)

        assert contract.verify(digest) == holder


def test_non_creator_cannot_issue() -> None:
    with algopy_testing_context() as context:
        contract = CertRegistry()
        outsider = context.any.account()

        with pytest.raises(AssertionError, match="Only the contract creator"):
            with context.txn.create_group(active_txn_overrides={"sender": outsider}):
                contract.issue(Bytes(b"b" * 32), arc4.String("Unauthorized"))


def test_verify_missing_digest_fails() -> None:
    with algopy_testing_context():
        contract = CertRegistry()

        with pytest.raises(AssertionError, match="Certificate not found"):
            contract.verify(Bytes(b"c" * 32))


def test_issue_rejects_non_sha256_digest_size() -> None:
    with algopy_testing_context():
        contract = CertRegistry()

        with pytest.raises(AssertionError, match="Certificate hash must be 32 bytes"):
            contract.issue(Bytes(b"too-short"), arc4.String("Invalid"))


def test_digest_cannot_be_issued_twice() -> None:
    with algopy_testing_context():
        contract = CertRegistry()
        digest = Bytes(b"d" * 32)
        contract.issue(digest, arc4.String("First holder"))

        with pytest.raises(AssertionError, match="Certificate hash already issued"):
            contract.issue(digest, arc4.String("Second holder"))
