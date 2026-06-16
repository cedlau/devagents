"""Fetch an open-access paper PDF by arXiv ID or DOI.

Used by the `paper-fetch` recipe to chase references found in a paper's
bibliography, without leaving the local environment. Resolves arXiv IDs
directly against arxiv.org, and DOIs via the OpenAlex API which exposes
open-access PDF URLs when available.

Paywalled papers cannot be retrieved by this script; in that case it
exits with a non-zero status and prints an explicit message so the
caller (typically the `researcher` agent) can fall back to asking the
user for the PDF.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


# arXiv new-style: 4-digit YYMM + . + 4 or 5 digits, optional version suffix.
_ARXIV_NEW_RE = re.compile(r"^(?:arXiv:)?(\d{4}\.\d{4,5})(v\d+)?$", re.IGNORECASE)

# arXiv legacy: archive[.subj]/YYMMNNN, e.g. cs.CL/0701001, math/0202001.
_ARXIV_OLD_RE = re.compile(r"^(?:arXiv:)?([a-z\-]+(?:\.[A-Z]{2})?/\d{7})$", re.IGNORECASE)

# DOI: prefix 10.<registrant>/<suffix>. Suffix accepts most printable chars.
_DOI_RE = re.compile(r"^(?:doi:|https?://(?:dx\.)?doi\.org/)?(10\.\d{4,9}/\S+)$", re.IGNORECASE)


def _classify(identifier: str) -> tuple[str, str]:
    """Detect the identifier kind and return its normalized form.

    Returns:
        A pair ``(kind, normalized)`` where ``kind`` is ``"arxiv"`` or
        ``"doi"`` and ``normalized`` is the bare identifier (no scheme,
        no version suffix for arXiv).

    Raises:
        ValueError: if the identifier matches none of the known patterns.
    """
    identifier = identifier.strip()
    if (m := _ARXIV_NEW_RE.match(identifier)):
        return "arxiv", m.group(1)
    if (m := _ARXIV_OLD_RE.match(identifier)):
        return "arxiv", m.group(1)
    if (m := _DOI_RE.match(identifier)):
        return "doi", m.group(1)
    raise ValueError(
        f"Unrecognized identifier: {identifier!r}. "
        "Expected an arXiv ID (e.g. 2301.12345) or a DOI (e.g. 10.1038/nature12345)."
    )


def _download(url: str, dest: Path, user_agent: str, timeout: int = 30) -> None:
    """Stream ``url`` to ``dest``. Raises on HTTP / URL errors."""
    req = Request(url, headers={"User-Agent": user_agent})
    with urlopen(req, timeout=timeout) as resp:
        dest.write_bytes(resp.read())


def fetch_arxiv(arxiv_id: str, output_dir: Path, user_agent: str) -> Path:
    """Download the PDF of an arXiv paper."""
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    safe = arxiv_id.replace("/", "_")
    dest = output_dir / f"arxiv_{safe}.pdf"
    _download(url, dest, user_agent)
    return dest


def _resolve_openalex_pdf_url(doi: str, user_agent: str, timeout: int = 30) -> str:
    """Query OpenAlex for the open-access PDF URL of a DOI.

    Raises:
        RuntimeError: if OpenAlex returns no open-access PDF URL.
    """
    api_url = f"https://api.openalex.org/works/doi:{doi}"
    req = Request(
        api_url,
        headers={"User-Agent": user_agent, "Accept": "application/json"},
    )
    with urlopen(req, timeout=timeout) as resp:
        payload = json.loads(resp.read())

    # OpenAlex exposes several candidate locations; prefer the curated best_oa_location.
    candidates = []
    best = payload.get("best_oa_location") or {}
    if best.get("pdf_url"):
        candidates.append(best["pdf_url"])
    primary = payload.get("primary_location") or {}
    if primary.get("pdf_url"):
        candidates.append(primary["pdf_url"])
    for loc in payload.get("locations") or []:
        if isinstance(loc, dict) and loc.get("pdf_url"):
            candidates.append(loc["pdf_url"])

    for url in candidates:
        return url

    raise RuntimeError(
        f"No open-access PDF URL exposed by OpenAlex for DOI {doi}. "
        "The paper may be paywalled or not yet indexed."
    )


def fetch_via_openalex(doi: str, output_dir: Path, user_agent: str) -> Path:
    """Resolve a DOI through OpenAlex and download the open-access PDF."""
    pdf_url = _resolve_openalex_pdf_url(doi, user_agent)
    safe = doi.replace("/", "_")
    dest = output_dir / f"doi_{safe}.pdf"
    _download(pdf_url, dest, user_agent)
    return dest


def fetch(identifier: str, output_dir: Path, user_agent: str) -> Path:
    """Dispatch fetch based on identifier kind. Returns the local PDF path."""
    kind, normalized = _classify(identifier)
    if kind == "arxiv":
        return fetch_arxiv(normalized, output_dir, user_agent)
    return fetch_via_openalex(normalized, output_dir, user_agent)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch an open-access paper PDF by arXiv ID or DOI.",
    )
    parser.add_argument(
        "identifier",
        help="arXiv ID (e.g. 2301.12345, cs.CL/0701001) or DOI (e.g. 10.1038/nature12345).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path.cwd(),
        help="Directory where the PDF will be saved (default: current directory).",
    )
    parser.add_argument(
        "--user-agent",
        default="researcher-agent/0.1 (https://github.com/anthropics/claude-code)",
        help="User-Agent header. Set to a contact-bearing string when running at scale.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    try:
        path = fetch(args.identifier, args.output_dir, args.user_agent)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)
    except (HTTPError, URLError) as exc:
        print(f"Error: network failure — {exc}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)

    # Stdout = just the path, for clean pipelining into pdf_to_text.py.
    print(path)
