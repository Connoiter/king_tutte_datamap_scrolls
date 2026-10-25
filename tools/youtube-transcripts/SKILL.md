---
name: youtube-transcripts
description: YouTube transcripts — pull a video's captions plus metadata into one Markdown file per talk. Use when asked to transcribe, fetch or archive YouTube talks, or to add a talk to a transcript collection.
---

# YouTube transcripts

Turns a list of YouTube videos into one Markdown file each: YAML front matter
(title, speakers, event, channel, upload date, duration, license, transcript
source), the video description, chapters, and the transcript in ~1-minute
paragraphs, each led by a `[[mm:ss]](https://youtu.be/ID?t=N)` timestamp link.

The tool is [`scripts/fetch_transcripts.py`](scripts/fetch_transcripts.py). It
carries its own dependencies (`youtube-transcript-api`, `yt-dlp`) as inline
script metadata, so `uv run` needs no install.

## Steps

1. **Add the talks to the talk list**, a JSON array of
   `{"id", "file", "speakers", "event"}` that lives beside the output files
   (in this repo: `docs/talks/by_tutte/talks.json`). Done when every new
   video has an entry whose speakers and event you have *confirmed* (see
   Metadata below), and whose `file` stem follows `speaker_at_venue_year`.
2. **Run the fetch** from the repo root:
   ```bash
   uv run tools/youtube-transcripts/scripts/fetch_transcripts.py docs/talks/by_tutte/talks.json docs/talks/by_tutte
   ```
   Existing files are skipped, so the run only fetches new entries. Done when
   it exits 0; on exit 1, read the `FAIL` lines (Rate limits below).
3. **Spot-check** one new file: front matter parses, chapters present when
   the video has them, transcript paragraphs read sensibly.
4. **Link each new file** from the collection's index (in this repo:
   `docs/talks/index.md`, oldest first by `upload_date`).

## Rate limits

YouTube throttles by IP. After ~20 back-to-back transcript fetches it began
answering `IpBlocked` to `youtube-transcript-api` and HTTP 429 to `yt-dlp
--write-auto-subs`; `yt-dlp --dump-json` metadata kept working throughout.

- The block covers both caption routes, so switching tools buys nothing. Stop,
  tell the user which files failed, and rerun later; the skip-existing
  behaviour makes the rerun resume cleanly.
- Keep batches near 20 and keep the pause between fetches (`PAUSE_SECONDS`).

## Metadata

YouTube metadata names the channel, rarely the speaker or venue, so the talk
list supplies both.

- Read the video **description** before writing an entry: it often names the
  real venue (e.g. a PyData channel upload whose description says "PyData DC
  2016").
- Confirm the target speaker actually appears. A related video on a host's
  channel may feature only the host.
- `upload_date` is when it was posted, which can trail the event by months;
  put the event date in `event` when it differs.

## Caption quality

Most talks have only auto-generated captions (`transcript_source` says
which). Expect misheard proper nouns: "Tata Institute" for Tutte, "Cypi" for
SciPy, "evoke" for EVōC. Keep the transcript verbatim; it is a record of the
captions.

## Licensing

`license` is read from YouTube; "Standard YouTube License" means not Creative
Commons. Surface that to the user when the collection has a licensing policy
(this repo's CLAUDE.md does).
