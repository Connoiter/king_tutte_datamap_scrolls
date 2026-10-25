# /// script
# requires-python = ">=3.10"
# dependencies = ["youtube-transcript-api>=1.0", "yt-dlp"]
# ///
"""Write one Markdown file per YouTube video: YAML front matter, description,
chapters and a timestamped transcript.

usage: uv run fetch_transcripts.py TALKS_JSON OUT_DIR

TALKS_JSON is a list of {"id", "file", "speakers", "event"} objects; "file" is
the output filename stem. Videos whose file already exists in OUT_DIR are
skipped, so rerunning only fetches what is missing. Exits 1 if any fetch failed.
"""
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi

PARAGRAPH_SECONDS = 60
PAUSE_SECONDS = 3


def ts(seconds):
    s = int(seconds)
    h, m, s = s // 3600, s % 3600 // 60, s % 60
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m:02d}:{s:02d}"


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def fetch_meta(vid):
    out = subprocess.run(
        [sys.executable, "-m", "yt_dlp", "--no-update", "--skip-download", "--dump-json",
         "--", f"https://www.youtube.com/watch?v={vid}"],
        check=True, capture_output=True, text=True,
    )
    return json.loads(out.stdout)


def paragraphs(snippets, vid):
    out, buf, start = [], [], None
    for sn in snippets:
        text = sn.text.replace("\n", " ").strip()
        if not text:
            continue
        if start is None:
            start = sn.start
        buf.append(text)
        if sn.start - start >= PARAGRAPH_SECONDS:
            out.append((start, " ".join(buf)))
            buf, start = [], None
    if buf:
        out.append((start, " ".join(buf)))
    return [f"[[{ts(t)}]](https://youtu.be/{vid}?t={int(t)}) {p}" for t, p in out]


def render(meta, speakers, event, transcript):
    vid = meta["id"]
    up = meta["upload_date"]
    lines = [
        "---",
        f"title: {yaml_str(meta['title'])}",
        "speakers:",
        *[f"  - {yaml_str(s)}" for s in speakers],
        f"event: {yaml_str(event)}",
        f"youtube_id: {yaml_str(vid)}",
        f"url: https://www.youtube.com/watch?v={vid}",
        f"channel: {yaml_str(meta.get('channel'))}",
        f"channel_url: {meta.get('channel_url')}",
        f"upload_date: {up[:4]}-{up[4:6]}-{up[6:]}",
        f"duration: {yaml_str(meta.get('duration_string'))}",
        f"license: {yaml_str(meta.get('license') or 'Standard YouTube License')}",
        f"transcript_source: {yaml_str(transcript['source'])}",
        f"retrieved: {date.today().isoformat()}",
        "---",
        "",
        f"# {meta['title']}",
        "",
        f"- **Speakers:** {', '.join(speakers)}",
        f"- **Event:** {event}",
        f"- **Video:** <https://www.youtube.com/watch?v={vid}>",
        "",
        "## Description",
        "",
        *[f"> {l}".rstrip() for l in (meta.get("description") or "").splitlines()],
        "",
    ]
    if meta.get("chapters"):
        lines += ["## Chapters", ""]
        lines += [f"- [{ts(c['start_time'])}](https://youtu.be/{vid}?t={int(c['start_time'])}) {c['title']}"
                  for c in meta["chapters"]]
        lines.append("")
    lines += ["## Transcript", ""]
    for p in transcript["paragraphs"]:
        lines += [p, ""]
    return "\n".join(lines)


def main(talks_json, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    api = YouTubeTranscriptApi()
    failed = 0
    for talk in json.loads(talks_json.read_text()):
        vid, stem = talk["id"], talk["file"]
        out = out_dir / f"{stem}.md"
        if out.exists():
            continue
        try:
            meta = fetch_meta(vid)
            t = api.fetch(vid, languages=["en", "en-US", "en-GB"])
        except Exception as e:
            msg = str(e).strip().splitlines()
            print(f"FAIL   {stem}: {type(e).__name__}{': ' + msg[0] if msg else ''}")
            failed += 1
            continue
        kind = "auto-generated" if t.is_generated else "uploader-provided"
        transcript = {
            "source": f"YouTube {kind} captions ({t.language_code}), via youtube-transcript-api",
            "paragraphs": paragraphs(t.snippets, vid),
        }
        out.write_text(render(meta, talk["speakers"], talk["event"], transcript))
        print(f"wrote  {stem} ({kind}, {len(t.snippets)} snippets)")
        time.sleep(PAUSE_SECONDS)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]))
