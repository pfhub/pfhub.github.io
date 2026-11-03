#!/usr/bin/env python3
"""Maintainer helper for the Past Workshops pages.

  import [SRC]   one-time: rename/convert everything in "CHiMaD Workshop Files/"
  add N          add workshop N: convert --photo/--agenda, add a CSV row, write the stub page
  stubs          (re)write workshop-NN.md for every row in workshops.csv
  check          list workshops missing a photo, agenda, date or stub page

Page content is rendered at build time by workshops/wslib.py; the stubs written
here only exist so MyST discovers one page per workshop. Needs macOS `sips`;
PDF photos also need ImageMagick (`magick`).
"""
import argparse
import csv
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
WS = REPO / "workshops"
sys.path.insert(0, str(WS))
import wslib  # noqa: E402

DEFAULT_SRC = REPO / "CHiMaD Workshop Files"
PHOTO_MAX, THUMB_MAX, QUALITY = 1600, 400, 82

STUB = """---
kernelspec:
  name: python3
  display_name: Python 3
---

# {title}

```{{code-cell}} python
:tags: [remove-input]
from wslib import show_workshop
show_workshop({n})
```
{agenda}"""


def number_of(path):
    m = re.match(r"\d+", path.name)
    return int(m.group()) if m else None


def sips(src, dest, longest, fmt="jpeg"):
    subprocess.run(["sips", "-s", "format", fmt, "-s", "formatOptions", str(QUALITY),
                    "-Z", str(longest), str(src), "--out", str(dest)],
                   check=True, capture_output=True)


def import_photo(src, n):
    dest = WS / "photos" / f"ws{n:02d}.jpg"
    thumb = WS / "photos" / "thumbs" / f"ws{n:02d}.jpg"
    if src.suffix.lower() == ".pdf":
        with tempfile.TemporaryDirectory() as tmp:
            page = Path(tmp) / "page.png"
            subprocess.run(["magick", "-density", "200", f"{src}[0]", str(page)], check=True)
            sips(page, dest, PHOTO_MAX)
    else:
        sips(src, dest, PHOTO_MAX)
    sips(dest, thumb, THUMB_MAX)
    print(f"photo   {src.name} -> {dest.relative_to(REPO)}")


def import_agenda(src, n):
    for old in (WS / "agendas").glob(f"ws{n:02d}.*"):
        old.unlink()
    dest = WS / "agendas" / f"ws{n:02d}{src.suffix.lower()}"
    shutil.copyfile(src, dest)
    print(f"agenda  {src.name} -> {dest.relative_to(REPO)}")


def write_stub(row):
    n = row["number"]
    agenda = wslib.find_media("agendas", n)
    if agenda is None:
        block = "\nAgenda not available.\n"
    elif agenda.suffix.lower() == ".pdf":
        block = f"\n{{download}}`Download the agenda (PDF) <agendas/{agenda.name}>`\n"
    else:
        block = f"\n![Agenda](agendas/{agenda.name})\n"
    (WS / f"workshop-{n:02d}.md").write_text(
        STUB.format(title=row["title"], n=n, agenda=block))


def cmd_stubs(_args=None):
    rows = wslib.load()
    wanted = {f"workshop-{r['number']:02d}.md" for r in rows}
    for r in rows:
        write_stub(r)
    for old in WS.glob("workshop-*.md"):
        if old.name not in wanted:
            old.unlink()
            print(f"removed stale {old.name}")
    print(f"wrote {len(rows)} stubs")


def cmd_check(_args=None):
    problems = 0
    for r in sorted(wslib.load(), key=lambda r: r["number"]):
        n = r["number"]
        missing = [what for what, ok in (
            ("photo", wslib.find_media("photos", n)),
            ("thumbnail", wslib.find_media("photos/thumbs", n)),
            ("agenda", wslib.find_media("agendas", n)),
            ("start_date", r["start_date"]),
            ("stub page", (WS / f"workshop-{n:02d}.md").exists()),
        ) if not ok]
        if missing:
            problems += 1
            print(f"workshop {n:>2} ({r['roman']}): missing {', '.join(missing)}")
    print(f"{problems} workshop(s) with gaps")


def cmd_import(args):
    src = Path(args.src)
    for kind, importer in (("Photos", import_photo), ("Agendas", import_agenda)):
        for f in sorted((src / kind).iterdir()):
            n = number_of(f)
            if n is None or f.name.startswith("."):
                print(f"skipped {f}")
                continue
            importer(f, n)


def cmd_add(args):
    n = args.number
    if args.photo:
        import_photo(Path(args.photo).expanduser(), n)
    if args.agenda:
        import_agenda(Path(args.agenda).expanduser(), n)
    rows = wslib.load()
    if n in {r["number"] for r in rows}:
        print(f"workshops.csv already has workshop {n}; leaving the row alone")
    else:
        with open(wslib.CSV_PATH, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([n] + [""] * (len(wslib.COLUMNS) - 1))
        print(f"added a blank row for workshop {n} to workshops.csv -- fill it in")
    cmd_stubs()


def main():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("import")
    s.add_argument("src", nargs="?", default=str(DEFAULT_SRC))
    s.set_defaults(func=cmd_import)
    s = sub.add_parser("add")
    s.add_argument("number", type=int)
    s.add_argument("--photo")
    s.add_argument("--agenda")
    s.set_defaults(func=cmd_add)
    s = sub.add_parser("stubs")
    s.set_defaults(func=cmd_stubs)
    s = sub.add_parser("check")
    s.set_defaults(func=cmd_check)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
