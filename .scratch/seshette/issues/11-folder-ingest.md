# 11: /datamap on a folder

**What to build:** A person points `/datamap` at a folder of text files and gets a datamap. Before any scribe runs, the top-level skill writes `documents`: one file is one document, its id comes from its path in the folder, its title comes from a heading or the filename when one is obvious, and its url is a `file://` link to the file. It skips, and reports, files that are not UTF-8 text, empty files, and hidden files and folders. It asks once whether to drop documents under about 20 words (showing a few) and once whether to keep one file per duplicate text, suggesting yes both times. Untitled points fall back to the first 10 or so words of their text. Callers that write `documents` themselves get the same cleaning advice as a warning.

**Blocked by:** 06 (Tracer bullet)

**Status:** ready-for-agent

- [ ] `/datamap` on a mixed test folder (text, a binary file, an empty file, a hidden folder, short files, duplicates) skips and asks exactly as described, and the run checker passes.
- [ ] Nothing is dropped or kept silently; skipped and dropped files are reported.
- [ ] Hovering an untitled point shows the first words of its text, and clicking a point opens its file.

Spec: `.scratch/seshette/spec.md`. Glossary: `docs/terminology.md`.
