from algopy import ARC4Contract, BoxMap, Bytes, Global, Txn, arc4


class CertRegistry(ARC4Contract):
    """Store SHA-256 certificate digests and their public holder labels."""

    def __init__(self) -> None:
        self.certs = BoxMap(Bytes, arc4.String, key_prefix=b"cert_")

    @arc4.abimethod
    def issue(self, cert_hash: Bytes, holder: arc4.String) -> None:
        """Register a 32-byte SHA-256 digest for a holder label."""
        assert Txn.sender == Global.creator_address, "Only the contract creator can issue certificates"
        assert cert_hash.length == 32, "Certificate hash must be 32 bytes"
        assert cert_hash not in self.certs, "Certificate hash already issued"
        self.certs[cert_hash] = holder

    @arc4.abimethod(readonly=True)
    def verify(self, cert_hash: Bytes) -> arc4.String:
        """Return the holder label for a previously registered digest."""
        assert cert_hash.length == 32, "Certificate hash must be 32 bytes"
        assert cert_hash in self.certs, "Certificate not found"
        return self.certs[cert_hash]
