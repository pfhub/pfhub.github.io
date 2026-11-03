"""Render helpers for the Past Workshops pages.

Imported by the ``{code-cell}`` blocks in ``workshops.md`` and ``workshop-NN.md``.
All data comes from ``workshops.csv`` plus the files named ``wsNN.*`` in
``photos/``, ``photos/thumbs/`` and ``agendas/``. Paths are relative to this
folder, which is the working directory of the cells during a build.
"""
import base64
import csv
import html
from pathlib import Path

from IPython.display import HTML, display

HERE = Path(__file__).resolve().parent
CSV_PATH = HERE / "workshops.csv"
COLUMNS = ["number", "roman", "title", "start_date", "end_date", "location",
           "format", "summary", "photo_caption"]
DEFAULT_TITLE = "CHiMaD Phase Field Methods {roman}"
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def roman(n):
    out = ""
    for value, sym in [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"),
                       (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"),
                       (5, "V"), (4, "IV"), (1, "I")]:
        while n >= value:
            out += sym
            n -= value
    return out


def load():
    """Return workshops as dicts keyed by column, newest (highest number) first."""
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f)]
    for r in rows:
        r["number"] = int(r["number"])
        r["roman"] = r["roman"] or roman(r["number"])
        r["title"] = r["title"] or DEFAULT_TITLE.format(roman=r["roman"])
    return sorted(rows, key=lambda r: r["number"], reverse=True)


def find_media(kind, number):
    """Path of ``<kind>/wsNN.*`` (kind: photos, photos/thumbs, agendas), or None."""
    matches = sorted((HERE / kind).glob(f"ws{number:02d}.*"))
    return matches[0] if matches else None


def _parse(d):
    parts = [int(p) for p in d.split("-")]
    return parts + [None] * (3 - len(parts))


def format_dates(start, end):
    """'2019-11-05','2019-11-07' -> 'November 5-7, 2019'. Partial dates are allowed."""
    if not start:
        return ""
    y1, m1, d1 = _parse(start)
    if not end or end == start:
        y2, m2, d2 = y1, m1, d1
    else:
        y2, m2, d2 = _parse(end)
    if m1 is None:
        return str(y1) if y1 == y2 else f"{y1}–{y2}"
    if d1 is None:
        return f"{MONTHS[m1 - 1]} {y1}"
    first = f"{MONTHS[m1 - 1]} {d1}"
    if (y1, m1, d1) == (y2, m2, d2):
        return f"{first}, {y1}"
    if (y1, m1) == (y2, m2):
        return f"{first}–{d2}, {y1}"
    if y1 == y2:
        return f"{first} – {MONTHS[m2 - 1]} {d2}, {y1}"
    return f"{first}, {y1} – {MONTHS[m2 - 1]} {d2}, {y2}"


def _year(r):
    return r["start_date"][:4] if r["start_date"] else ""


def _b64(path):
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")


def _img_src(path):
    if path is None:
        return None
    mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
    return f"data:{mime};base64,{_b64(path)}"


def _meta_line(r, with_format=False):
    bits = [format_dates(r["start_date"], r["end_date"]), r["location"]]
    if with_format:
        bits.append(r["format"].capitalize())
    return " · ".join(html.escape(b) for b in bits if b)


def _placeholder(r, cls):
    return f'<div class="{cls} ws-placeholder">{html.escape(r["roman"])}</div>'


def timeline():
    """Newest-first timeline; each entry links to /workshop-NN."""
    items = []
    last_year = None
    for r in load():
        n = r["number"]
        year = _year(r)
        shown_year = year if year != last_year else ""
        last_year = year
        thumb = find_media("photos/thumbs", n) or find_media("photos", n)
        title = html.escape(r["title"])
        if thumb is not None:
            pic = f'<img class="ws-thumb" src="{_img_src(thumb)}" alt="{title}">'
        else:
            pic = _placeholder(r, "ws-thumb")
        badge = f'<span class="ws-badge">{html.escape(r["format"])}</span>' if r["format"] else ""
        items.append(f'''
<a class="ws-item" href="/workshop-{n:02d}" target="_self">
  <div class="ws-year">{shown_year}</div>
  <div class="ws-card">
    {pic}
    <div class="ws-body">
      <p class="ws-title">{title}</p>
      <p class="ws-meta">{_meta_line(r)}</p>
      {badge}
    </div>
  </div>
</a>''')
    display(HTML(f'<div class="ws-timeline">{"".join(items)}</div>'))


def show_workshop(number):
    """Header, previous/next links, summary and photo for one workshop page."""
    rows = load()
    by_num = {r["number"]: r for r in rows}
    r = by_num[number]
    nums = sorted(by_num)
    i = nums.index(number)

    def link(n, text):
        return f'<a href="/workshop-{n:02d}" target="_self">{text}</a>'

    prev_html = (link(nums[i - 1], f"← {by_num[nums[i - 1]]['roman']}")
                 if i > 0 else "<span></span>")
    next_html = (link(nums[i + 1], f"{by_num[nums[i + 1]]['roman']} →")
                 if i < len(nums) - 1 else "<span></span>")
    nav = f'<div class="ws-nav">{prev_html}<a href="/workshops" target="_self">All workshops</a>{next_html}</div>'

    photo = find_media("photos", number)
    if photo is not None:
        caption = (f'<p class="ws-caption">{html.escape(r["photo_caption"])}</p>'
                   if r["photo_caption"] else "")
        pic = (f'<figure class="ws-photo"><img src="{_img_src(photo)}" '
               f'alt="{html.escape(r["title"])}">{caption}</figure>')
    else:
        pic = ""
    summary = f'<p class="ws-summary">{html.escape(r["summary"])}</p>' if r["summary"] else ""
    display(HTML(f'''<div class="ws-detail">
{nav}
<p class="ws-meta">{_meta_line(r, with_format=True)}</p>
{summary}
{pic}
</div>'''))
