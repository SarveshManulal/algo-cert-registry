# CertSeal

> Algorand smart contract for registering and verifying SHA-256 certificate hashes on-chain.

A small Algorand smart contract that lets the contract creator register a certificate’s SHA-256 digest and a public holder label. Anyone can verify a digest against the registry without uploading the certificate itself.

## How it works

- `issue(cert_hash, holder)` accepts a 32-byte SHA-256 digest and holder label. Only the account that created the app can issue entries. Duplicate digests are rejected.
- `verify(cert_hash)` is a read-only ARC-4 method that returns the stored holder label or fails if the digest is not registered.
- Entries are stored in a `BoxMap`, so the registry is not limited to Algorand’s small global-state key limit. Box storage requires app-account minimum balance and the calling transaction must include the relevant box reference. The deployment helper seeds the app account with 1 ALGO on first deployment; additional entries may require additional balance.

The digest and holder label are public on-chain data. Do not store certificate files, personal details, or other confidential information in this app. Use an opaque label if the holder’s identity should not be public. This starter is for demonstration and has not had a security audit.

## Requirements

- Python 3.12 or later
- AlgoKit CLI 2.x
- Git
- Docker Desktop only if you want to run LocalNet; the included tests are offline and do not require Docker
- VS Code is recommended

On Windows, install AlgoKit from PowerShell with `irm https://cli.algokit.io/install.ps1 | iex`, then restart the terminal. The Python template uses Poetry; if needed, install it with `uv tool install poetry`.

## Build and test

From this project directory:

```powershell
algokit project bootstrap all
algokit project run build
algokit project run test
```

The offline tests cover creator-only issuance, digest size validation, duplicate rejection, successful verification, and missing records. You can also start LocalNet with `algokit localnet start` if Docker is installed.

## TestNet deployment

1. Switch your wallet to Algorand TestNet and obtain test ALGO from the [TestNet dispenser](https://bank.testnet.algorand.network/testnet/fund).
2. Build the contract with `algokit project run build`.
3. Deploy from this directory with `algokit project deploy testnet`. AlgoKit will prompt for the deployer mnemonic if it is not already available in the environment.
4. Enter secrets only into the trusted terminal prompt. Never send a recovery phrase to anyone, paste it into chat, commit it, or add it to a tracked file. TestNet accounts are still controlled by their keys; use a dedicated throwaway account.
5. Save the printed App ID and open it in the [TestNet explorer](https://lora.algokit.io/testnet). Capture a screenshot of the live app and a successful verification call for your submission.

The deployment helper creates the app and transfers 1 ALGO to its app account as an initial box-storage reserve. The deployer needs enough TestNet ALGO for app creation and this transfer. Each new box increases the app account’s minimum balance, so a larger registry needs additional funding.

## Submission checklist

GitHub repository: [SarveshManulal/algo-cert-registry](https://github.com/SarveshManulal/algo-cert-registry) (public).

After TestNet deployment, add the live App ID, explorer URL, and a screenshot of a successful certificate lookup here. The deployment must use a TestNet account you control; never share its mnemonic.
