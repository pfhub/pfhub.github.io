# PFHub website

Source for the PFHub community site, the landing and community pages for phase-field simulation benchmarking. The benchmarks themselves live in [pfhub/pfhub-benchmarks](https://github.com/pfhub/pfhub-benchmarks). The site is built with [MyST](https://mystmd.org) via `jupyter-book` and deployed to GitHub Pages from `main`.

This file is for people working on the repo and is not part of the published site. The site's home page is `index.md`.

## Setup

You need Node.js (for `jupyter-book`) and Python 3.

```bash
npm install -g jupyter-book
pip install -r requirements.txt
```

Python is required because pages are executed at build time (the community page and the Past Workshops pages are generated from data files).

## Build and preview

```bash
# build to _build/html/
jupyter-book build --html --execute

# preview locally (--execute is required: without it the community and workshop
# pages show no content, because that content is produced by running code)
jupyter-book start --execute
```

MyST caches executed pages by their source, not by the data files they read. After editing a CSV or any image or helper code, clear the cache or you will see old content:

```bash
jupyter-book clean --execute --html -y && jupyter-book build --html --execute
```

Pushing to `main` builds and deploys automatically (`.github/workflows/deploy.yml`). CI starts without a cache, so deployed pages always reflect the current files.

## Updating content

### Community members

Edit `about/people.csv` (`name,description,images,github,orcid,email`). Put the photo in `images/` and give just its filename in the `images` column. An empty cell hides that field.

### Past workshops

Everything for the workshop pages lives in `workshops/`:

| Path | What it is |
|------|------------|
| `workshops/workshops.csv` | One row per workshop: `number,roman,title,start_date,end_date,location,format,summary,photo_caption` |
| `workshops/photos/wsNN.jpg` | Group photo (`photos/thumbs/wsNN.jpg` is the small version used on the timeline) |
| `workshops/agendas/wsNN.pdf` | Agenda (a `.png` also works) |
| `workshops/workshop-NN.md` | Small page for each workshop; filled in automatically at build time |

Dates are ISO format (`2026-05-19`); a month (`2015-10`) or just a year (`2015`) is also fine. Empty cells are hidden on the page, and `roman` and `title` are worked out from `number` if left blank. Workshops are shown newest first by `number`.

**Add a new workshop**

```bash
python scripts/workshops_tool.py add 21 --photo ~/Downloads/group.HEIC --agenda ~/Downloads/agenda.pdf
```

This converts and renames the photo (HEIC, PNG, JPG or a PDF all work), copies the agenda, adds an empty row for workshop 21 to `workshops.csv`, and creates `workshops/workshop-21.md`. Then fill in the new CSV row, rebuild (clearing the cache as above), and commit the CSV, the `photos/` and `agendas/` files, and the new `workshop-21.md`.

`--photo` and `--agenda` are optional. A workshop without a photo shows a placeholder, and one without an agenda says so.

**Other tasks**

```bash
python scripts/workshops_tool.py check    # list workshops missing a photo, agenda or date
python scripts/workshops_tool.py stubs    # rewrite every workshop-NN.md (e.g. after an agenda changes from .pdf to .png)
```

The tool uses macOS `sips` for image conversion (and ImageMagick's `magick` only for PDF photos), so run it on a Mac. To change a photo or agenda without the tool, replace the file using the same `wsNN` name; if the agenda's extension changed, run `stubs`.

### Pages and navigation

Pages are `.md` files or notebooks. Page addresses use the filename only, so filenames must be unique across folders. The menus are listed by hand in `myst.yml`, so a new page needs an entry there to appear in the navigation.
