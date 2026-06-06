import json
import re
import runpy
from pathlib import Path

from docx import Document


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
DATA_PATH = ROOT / "data" / "entries.json"
PREVIOUS_DOCX = WORKSPACE / "之前的养老金动态word文件" / "养老金资讯-国际养老金动态（20260524-20260530）(单周).docx"
CURRENT_SCRIPT = (
    WORKSPACE
    / "已生成文件"
    / "养老金资讯-国际养老金动态（20260531-20260606）-单周"
    / "generate_word_report.py"
)


def clean_heading(text):
    text = re.sub(r"^（\d+）", "", text.strip())
    text = text.replace("*", "").strip()
    if "|" in text:
        country, title = [part.strip() for part in text.split("|", 1)]
    else:
        country, title = "", text
    return country, title


def parse_source(source_text):
    source_text = source_text.strip()
    source = source_text.replace("资料来源：", "", 1)
    dates = re.findall(r"2026-\d{2}-\d{2}", source)
    date = dates[0] if dates else "2026-05-30"
    source = re.sub(r"，2026-\d{2}-\d{2}", "", source)
    source = re.sub(r"；2026-\d{2}-\d{2}", "", source)
    return source.strip("；， "), date


def extract_previous_word_entries():
    doc = Document(PREVIOUS_DOCX)
    entries = []
    section = "政策与管理"
    paragraphs = [p.text.strip() for p in doc.paragraphs]
    i = 0
    while i < len(paragraphs):
        text = paragraphs[i]
        if text == "二、养老金投资":
            section = "投资动态"
            i += 1
            continue
        if re.match(r"^（\d+）", text):
            country, title = clean_heading(text)
            body = paragraphs[i + 1] if i + 1 < len(paragraphs) else ""
            source_line = paragraphs[i + 2] if i + 2 < len(paragraphs) else ""
            source, date = parse_source(source_line)
            entries.append(
                {
                    "country": country,
                    "title": title,
                    "content": body,
                    "date": date,
                    "category": section,
                    "importance": 4 if "*" in text else 3,
                    "source": source or "养老金资讯-国际养老金动态Word报告",
                    "url": "",
                    "source_document": str(PREVIOUS_DOCX),
                    "source_url_missing": True,
                    "verified": False,
                    "ready_for_report": True,
                    "verification_note": "来自用户指定的2026-05-24至2026-05-30 Word政策文件；原文件未提供具体原文URL。",
                }
            )
            i += 3
        else:
            i += 1
    return entries


def extract_current_entries():
    ns = runpy.run_path(str(CURRENT_SCRIPT))
    entries = []
    for entry in ns["POLICY_ENTRIES"] + ns["INVESTMENT_ENTRIES"]:
        entries.append(
            {
                "country": entry["country"],
                "title": entry["title"].split("|", 1)[-1].strip(),
                "content": entry["body"],
                "date": entry["date"],
                "category": entry["category"],
                "importance": entry["importance"],
                "source": entry["source"],
                "url": entry["url"],
                "extra_url": entry.get("extra_url", ""),
                "original_pub_date": entry["date"],
                "policy_effective_date": "详见原文",
                "in_report_window": True,
                "verified": True,
                "ready_for_report": True,
                "verification_note": "已下载并核验具体原文详情页；按新版短简报报告同步更新。",
            }
        )
    return entries


def main():
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    existing = [
        entry
        for entry in data["entries"]
        if not ("2026-05-24" <= entry.get("date", "") <= "2026-06-06")
    ]

    new_entries = extract_previous_word_entries() + extract_current_entries()
    next_id = max(entry["id"] for entry in existing) + 1
    for offset, entry in enumerate(new_entries):
        entry["id"] = next_id + offset

    data["entries"] = existing + new_entries
    meta = data["metadata"]
    meta["last_updated"] = "2026-06-06"
    meta["report_period_end"] = "2026-06-06"
    meta["total_entries"] = len(data["entries"])
    meta["data_version"] = "6.1-20260606-two-week-site-update"

    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"updated {DATA_PATH}; previous={len(extract_previous_word_entries())}; "
        f"current={len(extract_current_entries())}; total={len(data['entries'])}"
    )


if __name__ == "__main__":
    main()
