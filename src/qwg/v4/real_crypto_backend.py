from __future__ import annotations

from collections.abc import Callable
import base64
import binascii
from typing import Any, Protocol

from qwg.v4 import COMPONENT_ROLE
from qwg.v4.signing import COMPONENT_VERDICT_DOMAIN
from qwg.v4.trust_profile import require_non_empty_str, require_positive_int, require_supported_algorithm

REAL_CRYPTO_SIGNATURE_INPUT_PREFIX = "DGB-SHIELD-V4-REAL-CRYPTO-SIGNATURE-INPUT"
REAL_SIGNATURE_ENCODING_PREFIX = "b64u:"
_BASE64URL_ALPHABET = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_")
_TEST_ONLY_MARKERS = ("test-only",)
_TEST_ONLY_PREFIXES = ("test-",)
_ALLOWED_DOMAIN_TAGS = frozenset({COMPONENT_VERDICT_DOMAIN})


class QwgV4RealCryptoBackendError(ValueError):
    """Base fail-closed error for QWG Shield v4 real crypto backend wiring."""


class QwgV4RealCryptoBackendUnavailable(QwgV4RealCryptoBackendError):
    """Raised when a required production backend or algorithm is unavailable."""


class QwgV4RealCryptoMaterialError(QwgV4RealCryptoBackendError):
    """Raised when deterministic TEST-ONLY material reaches the real backend."""


class QwgV4RealCryptoBackend(Protocol):
    """Minimal production crypto backend contract for QWG v4 evidence.

    Implementations may wrap liboqs, an HSM, a FIPS-validated module, or another
    deployment-controlled backend. This protocol intentionally avoids importing a
    concrete PQC library so CI cannot silently depend on local machine crypto state.
    """

    backend_name: str
    backend_version: str
    supported_algorithms: tuple[str, ...]

    def sign_message(self, *, algorithm: str, private_key_reference: str, message: bytes) -> str:
        """Return a real signature encoding for the supplied message."""

    def verify_signature(self, *, algorithm: str, public_key: str, message: bytes, signature: str) -> bool:
        """Return True only when the signature verifies under the supplied public key."""


RealCryptoSignatureVerifier = Callable[[dict[str, Any], dict[str, Any]], bool]




def _require_hash(value: Any, *, field: str) -> str:
    clean = require_non_empty_str(value, field=field)
    if len(clean) != 64:
        raise QwgV4RealCryptoBackendError(f"{field} must be 64-character sha256 hex")
    try:
        int(clean, 16)
    except ValueError as exc:
        raise QwgV4RealCryptoBackendError(f"{field} must be sha256 hex") from exc
    if clean != clean.lower():
        raise QwgV4RealCryptoBackendError(f"{field} must be lowercase sha256 hex")
    return clean


def _reject_test_only_text(value: str, *, field: str) -> None:
    clean = value.strip().lower()
    if any(marker in clean for marker in _TEST_ONLY_MARKERS) or any(clean.startswith(prefix) for prefix in _TEST_ONLY_PREFIXES):
        raise QwgV4RealCryptoMaterialError(f"{field} must not contain test-only material")


def encode_binary_signature_material(raw: bytes, *, field: str = "signature") -> str:
    """Encode real binary signature/key material as explicit unpadded base64url."""

    if not isinstance(raw, bytes) or not raw:
        raise QwgV4RealCryptoBackendError(f"{field} bytes must be non-empty")
    encoded = base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")
    return f"{REAL_SIGNATURE_ENCODING_PREFIX}{encoded}"


def decode_binary_signature_material(encoded: Any, *, field: str = "signature") -> bytes:
    """Decode an explicit ``b64u:`` signature/key encoding into bytes."""

    clean = require_non_empty_str(encoded, field=field)
    if not clean.startswith(REAL_SIGNATURE_ENCODING_PREFIX):
        raise QwgV4RealCryptoBackendError(f"{field} must use b64u encoding")
    body = clean[len(REAL_SIGNATURE_ENCODING_PREFIX) :]
    if not body:
        raise QwgV4RealCryptoBackendError(f"{field} b64u payload must be non-empty")
    if "=" in body:
        raise QwgV4RealCryptoBackendError(f"{field} b64u payload must be unpadded")
    if set(body) - _BASE64URL_ALPHABET:
        raise QwgV4RealCryptoBackendError(f"{field} b64u payload is invalid")
    try:
        decoded = base64.urlsafe_b64decode(body + "=" * (-len(body) % 4))
    except (binascii.Error, ValueError) as exc:
        raise QwgV4RealCryptoBackendError(f"{field} b64u payload is invalid") from exc
    return decoded


def reject_test_only_private_key_reference(private_key_reference: str) -> str:
    clean = require_non_empty_str(private_key_reference, field="private_key_reference")
    _reject_test_only_text(clean, field="private_key_reference")
    return clean


def reject_test_only_key_material(key: dict[str, Any]) -> None:
    """Fail closed if deterministic-test keys reach the real backend boundary."""

    _reject_test_only_text(require_non_empty_str(key.get("key_id"), field="key_id"), field="key_id")
    _reject_test_only_text(require_non_empty_str(key.get("public_key"), field="public_key"), field="public_key")


def build_real_crypto_signature_input(
    *,
    algorithm: str,
    domain_tag: str,
    signed_payload_hash: str,
    key_id: str,
    key_version: int,
) -> bytes:
    """Build the exact production-signature message bytes for QWG Shield v4.

    The signed payload hash is already domain-separated over the canonical QWG
    verdict payload. The real-signature input binds that hash to the concrete
    signature entry, algorithm, key id, and key version so entries cannot be
    spliced across bundles.
    """

    clean_algorithm = require_supported_algorithm(algorithm)
    clean_domain = require_non_empty_str(domain_tag, field="domain_tag")
    if clean_domain not in _ALLOWED_DOMAIN_TAGS:
        raise QwgV4RealCryptoBackendError("domain_tag must be the QWG Shield v4 component signing domain")
    clean_hash = _require_hash(signed_payload_hash, field="signed_payload_hash")
    clean_key_id = require_non_empty_str(key_id, field="key_id")
    clean_key_version = require_positive_int(key_version, field="key_version")
    return "\n".join(
        (
            REAL_CRYPTO_SIGNATURE_INPUT_PREFIX,
            clean_domain,
            clean_hash,
            clean_algorithm,
            clean_key_id,
            str(clean_key_version),
        )
    ).encode("utf-8")


def _require_backend_supports_algorithm(backend: QwgV4RealCryptoBackend, algorithm: str) -> None:
    try:
        supported = tuple(getattr(backend, "supported_algorithms", ()))
    except Exception as exc:
        raise QwgV4RealCryptoBackendError("real crypto backend algorithm discovery failed closed") from exc
    if algorithm not in supported:
        raise QwgV4RealCryptoBackendUnavailable("real crypto backend does not support required algorithm")


def _call_backend_sign(
    backend: QwgV4RealCryptoBackend,
    *,
    algorithm: str,
    private_key_reference: str,
    message: bytes,
) -> str:
    try:
        return backend.sign_message(algorithm=algorithm, private_key_reference=private_key_reference, message=message)
    except QwgV4RealCryptoBackendError:
        raise
    except Exception as exc:
        raise QwgV4RealCryptoBackendError("real crypto backend sign failed closed") from exc


def _call_backend_verify(
    backend: QwgV4RealCryptoBackend,
    *,
    algorithm: str,
    public_key: str,
    message: bytes,
    signature: str,
) -> bool:
    try:
        verified = backend.verify_signature(
            algorithm=algorithm,
            public_key=public_key,
            message=message,
            signature=signature,
        )
    except QwgV4RealCryptoBackendError:
        raise
    except Exception as exc:
        raise QwgV4RealCryptoBackendError("real crypto backend verify failed closed") from exc
    if not isinstance(verified, bool):
        raise QwgV4RealCryptoBackendError("real crypto backend verify must return bool")
    return verified


def build_signature_entry_with_real_backend(
    *,
    algorithm: str,
    domain_tag: str,
    signed_payload_hash: str,
    key_id: str,
    key_version: int,
    private_key_reference: str,
    backend: QwgV4RealCryptoBackend,
) -> dict[str, Any]:
    """Build a QWG Shield v4 signature entry using a real backend implementation."""

    message = build_real_crypto_signature_input(
        algorithm=algorithm,
        domain_tag=domain_tag,
        signed_payload_hash=signed_payload_hash,
        key_id=key_id,
        key_version=key_version,
    )
    clean_private_ref = reject_test_only_private_key_reference(private_key_reference)
    _require_backend_supports_algorithm(backend, algorithm)
    signature = _call_backend_sign(
        backend,
        algorithm=algorithm,
        private_key_reference=clean_private_ref,
        message=message,
    )
    clean_signature = require_non_empty_str(signature, field="signature")
    decode_binary_signature_material(clean_signature, field="signature")
    return {
        "algorithm": algorithm,
        "key_id": key_id,
        "key_version": key_version,
        "signed_payload_hash": signed_payload_hash,
        "domain_tag": domain_tag,
        "signature": clean_signature,
    }


def _validated_key_fields(key: dict[str, Any], *, algorithm: str, key_id: str, key_version: int) -> dict[str, Any]:
    if not isinstance(key, dict):
        raise QwgV4RealCryptoBackendError("registry key must be dict")
    role = require_non_empty_str(key.get("role"), field="role")
    if role != COMPONENT_ROLE:
        raise QwgV4RealCryptoBackendError("registry key role mismatch")
    key_algorithm = require_supported_algorithm(key.get("algorithm"))
    key_key_id = require_non_empty_str(key.get("key_id"), field="key_id")
    key_key_version = require_positive_int(key.get("key_version"), field="key_version")
    if (key_algorithm, key_key_id, key_key_version) != (algorithm, key_id, key_version):
        raise QwgV4RealCryptoBackendError("signature entry does not match registry key")
    public_key = require_non_empty_str(key.get("public_key"), field="public_key")
    reject_test_only_key_material(key)
    decode_binary_signature_material(public_key, field="public_key")
    return {"role": role, "algorithm": key_algorithm, "key_id": key_key_id, "key_version": key_key_version, "public_key": public_key}


def verify_signature_entry_with_real_backend(
    entry: dict[str, Any],
    key: dict[str, Any],
    *,
    backend: QwgV4RealCryptoBackend,
) -> bool:
    """Verify one QWG Shield v4 signature entry with a production backend."""

    if not isinstance(entry, dict):
        raise QwgV4RealCryptoBackendError("signature entry must be dict")
    algorithm = require_supported_algorithm(entry.get("algorithm"))
    key_id = require_non_empty_str(entry.get("key_id"), field="key_id")
    key_version = require_positive_int(entry.get("key_version"), field="key_version")
    checked_key = _validated_key_fields(key, algorithm=algorithm, key_id=key_id, key_version=key_version)
    _require_backend_supports_algorithm(backend, algorithm)
    message = build_real_crypto_signature_input(
        algorithm=algorithm,
        domain_tag=require_non_empty_str(entry.get("domain_tag"), field="domain_tag"),
        signed_payload_hash=_require_hash(entry.get("signed_payload_hash"), field="signed_payload_hash"),
        key_id=key_id,
        key_version=key_version,
    )
    signature = require_non_empty_str(entry.get("signature"), field="signature")
    decode_binary_signature_material(signature, field="signature")
    return _call_backend_verify(
        backend,
        algorithm=algorithm,
        public_key=checked_key["public_key"],
        message=message,
        signature=signature,
    )


def make_real_crypto_signature_verifier(backend: QwgV4RealCryptoBackend) -> RealCryptoSignatureVerifier:
    """Adapt a real crypto backend to the existing QWG v4 bundle verifier callback."""

    def _verify(entry: dict[str, Any], key: dict[str, Any]) -> bool:
        return verify_signature_entry_with_real_backend(entry, key, backend=backend)

    return _verify
