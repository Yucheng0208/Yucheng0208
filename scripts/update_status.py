"""Update date-dependent status text in the README files.

Each status lives between `<!-- status:KEY -->` and `<!-- /status -->` markers.
Run daily by .github/workflows/update-status.yml; pass --date YYYY-MM-DD to test.
"""
import argparse
import datetime as dt
import pathlib
import re
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent.parent
FILES = {"en": "README.md", "zh-TW": "README.zh-TW.md", "ja": "README.ja.md"}

# phase -> label per language; an empty label hides the status after the event
EVENTS = {
    "vcip2026": dict(
        start=dt.date(2026, 12, 13),
        end=dt.date(2026, 12, 16),
        before={"en": "To appear · Dec 13–16, Singapore", "zh-TW": "即將發表 · 12/13–16 新加坡", "ja": "発表予定 · 12月13–16日 シンガポール"},
        during={"en": "Presenting now · Singapore", "zh-TW": "發表中 · 新加坡", "ja": "発表中 · シンガポール"},
        after={"en": "", "zh-TW": "", "ja": ""},
    ),
}


def label(event, lang, today):
    if today < event["start"]:
        text = event["before"][lang]
    elif today <= event["end"]:
        text = event["during"][lang]
    else:
        text = event["after"][lang]
    return f" · {text}" if text else ""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", type=dt.date.fromisoformat,
                    default=dt.datetime.now(ZoneInfo("Asia/Taipei")).date())
    today = ap.parse_args().date

    for lang, name in FILES.items():
        path = ROOT / name
        text = path.read_text(encoding="utf-8")
        for key, event in EVENTS.items():
            pattern = re.compile(rf"(<!-- status:{key} -->).*?(<!-- /status -->)", re.S)
            text = pattern.sub(lambda m: m.group(1) + label(event, lang, today) + m.group(2), text)
        path.write_text(text, encoding="utf-8")
    print(f"statuses updated for {today}")


if __name__ == "__main__":
    main()
