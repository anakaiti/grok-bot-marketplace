#!/usr/bin/env python3
"""Archive recipes linked from the public Grok Bot marketplace."""

import argparse
import base64
from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import re
import sys
from tempfile import NamedTemporaryFile
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

PAGE = "https://x.ai/bot/marketplace"
ENDPOINT = "https://api2.cursor.sh/aiserver.v1.GrokBotService/GetPublicGrokBotMarketplaceListing"
ROOT = Path(__file__).resolve().parent
TIMEOUT_SECONDS = 35
MAX_ATTEMPTS = 4


class HttpsOnlyRedirectHandler(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        scheme = urlsplit(newurl).scheme
        if scheme != "https":
            raise URLError(f"blocked non-HTTPS redirect ({scheme or 'unknown'})")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


OPENER = build_opener(HttpsOnlyRedirectHandler)


def fetch(url, payload=None):
    parts = urlsplit(url)
    host = parts.hostname or "URL"
    if parts.scheme != "https":
        raise RuntimeError(f"{host}: non-HTTPS URL blocked")

    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode()
        headers = {
            "Content-Type": "application/json",
            "Connect-Protocol-Version": "1",
        }

    request = Request(url, data=data, headers=headers)
    last_error = None
    for attempt in range(MAX_ATTEMPTS):
        try:
            with OPENER.open(request, timeout=TIMEOUT_SECONDS) as response:
                return response.read()
        except HTTPError as error:
            last_error = f"HTTP {error.code}"
            if error.code != 429 and error.code < 500:
                break
        except (URLError, TimeoutError, OSError) as error:
            reason = getattr(error, "reason", error)
            last_error = str(reason).replace(url, host)
        if attempt + 1 < MAX_ATTEMPTS:
            time.sleep(2**attempt)
    raise RuntimeError(f"{host}: {last_error}")


def discover_slugs(html):
    return set(re.findall(r"/bot/marketplace/bots/([a-zA-Z0-9_-]+)", html))


def slugify(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "untitled"


DATA_JSON_PREFIX = "data:application/json;base64,"


def load_recipe(slug):
    response = json.loads(fetch(ENDPOINT, {"slug": slug}))
    template_url = response.get("templateGetUrl") if isinstance(response, dict) else None
    if not isinstance(template_url, str):
        raise ValueError("listing response is missing templateGetUrl")
    if template_url.startswith(DATA_JSON_PREFIX):
        raw = base64.b64decode(template_url[len(DATA_JSON_PREFIX):])
    else:
        raw = fetch(template_url)
    recipe = json.loads(raw)
    validate_recipe(recipe)
    listing = response.get("listing")
    if isinstance(listing, dict):
        recipe["listing"] = listing
    return recipe


def validate_recipe(recipe):
    profile = recipe.get("profile") if isinstance(recipe, dict) else None
    if not isinstance(profile, dict) or not isinstance(profile.get("name"), str):
        raise ValueError("recipe is missing a profile name")
    for field, text_key in (("skills", "content"), ("routines", "content"), ("plugins", "name")):
        items = recipe.get(field)
        if items is None:
            continue
        if not isinstance(items, list) or any(
            not isinstance(item, dict)
            or not isinstance(item.get(text_key), str)
            or not isinstance(item.get("name"), str)
            for item in items
        ):
            raise ValueError(f"invalid recipe field: {field}")
        if field == "plugins" and any(
            type(item.get("pluginId")) not in (str, int) for item in items
        ):
            raise ValueError("invalid plugin ID")


def json_bytes(value):
    return (json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + "\n").encode()


def save(root, relative, content):
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_bytes() == content:
        return
    with NamedTemporaryFile(dir=path.parent, delete=False) as temporary:
        temp_path = Path(temporary.name)
        try:
            temporary.write(content)
            temporary.close()
            os.chmod(temp_path, 0o644)
            temp_path.replace(path)
        finally:
            temp_path.unlink(missing_ok=True)


def archive(root, slug, recipe):
    bot_dir = root / "bots" / slug
    bodies = {}
    for field in ("skills", "routines"):
        used = set()
        for item in recipe.get(field) or []:
            base = slugify(item["name"])
            stem = base
            suffix = 2
            while stem in used:
                stem = f"{base}-{suffix}"
                suffix += 1
            used.add(stem)
            relative = f"{field}/{stem}.md"
            item["contentFile"] = relative
            bodies[relative] = item.pop("content").encode()

    manifest = json_bytes(recipe)
    for relative, content in bodies.items():
        save(bot_dir, relative, content)
    save(bot_dir, "recipe.json", manifest)

    for field in ("skills", "routines"):
        folder = bot_dir / field
        if not folder.is_dir():
            continue
        expected = {
            Path(relative).name
            for relative in bodies
            if relative.startswith(f"{field}/")
        }
        for existing in folder.glob("*.md"):
            if existing.name not in expected:
                existing.unlink()
        if not any(folder.iterdir()):
            folder.rmdir()


def update_catalog(root, slugs):
    bots = {}
    plugins = {}
    for path in sorted((root / "bots").glob("*/recipe.json")):
        slug = path.parent.name
        recipe = json.loads(path.read_bytes())
        listing = recipe.get("listing") if isinstance(recipe.get("listing"), dict) else {}
        entry = {
            "name": recipe["profile"]["name"],
            "recipe": f"bots/{slug}/recipe.json",
            "source": f"{PAGE}/bots/{slug}",
        }
        categories = listing.get("categories")
        if isinstance(categories, list) and all(isinstance(cat, str) for cat in categories):
            entry["categories"] = sorted(categories)
        creator = listing.get("creator")
        if isinstance(creator, dict) and isinstance(creator.get("name"), str):
            entry["creator"] = creator["name"]
        bots[slug] = entry

        for plugin in recipe.get("plugins") or []:
            plugin_entry = plugins.setdefault(str(plugin["pluginId"]), {"names": set(), "bots": set()})
            plugin_entry["names"].add(plugin["name"])
            plugin_entry["bots"].add(slug)

    plugin_index = {
        key: {field: sorted(values) for field, values in entry.items()}
        for key, entry in plugins.items()
    }
    save(
        root,
        "catalog.json",
        json_bytes({
            "listed": sorted(slugs & bots.keys()),
            "bots": bots,
            "pluginReferences": plugin_index,
        }),
    )


def sync(root):
    slugs = discover_slugs(fetch(PAGE).decode("utf-8", errors="replace"))
    if not slugs:
        raise RuntimeError("No marketplace bot links found. Existing archive kept.")

    failures = []
    with ThreadPoolExecutor(max_workers=6) as pool:
        pending = {slug: pool.submit(load_recipe, slug) for slug in sorted(slugs)}
        for slug, future in pending.items():
            try:
                archive(root, slug, future.result())
                print(f"Synced {slug}", flush=True)
            except Exception as error:
                failures.append(slug)
                print(f"Failed {slug}: {error}", file=sys.stderr, flush=True)
    update_catalog(root, slugs)
    return bool(failures)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT, help="Archive directory")
    try:
        raise SystemExit(sync(parser.parse_args().output))
    except RuntimeError as error:
        raise SystemExit(str(error)) from None
