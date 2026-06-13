from __future__ import annotations

import json
from pathlib import Path


REPO_DIR = Path(__file__).resolve().parents[1]
ROOT_DIR = REPO_DIR.parent
DATA_FILE = REPO_DIR / "data" / "entries.json"
REPORT_DATA = (
    ROOT_DIR
    / "已生成文件"
    / "养老金资讯-国际养老金动态（20260607-20260613）-单周"
    / "report_data_20260607_20260613.json"
)

START = "2026-06-07"
END = "2026-06-13"

CATEGORY_MAP = {
    "20260613-au-apra-longevity": "投资治理",
    "20260610-uk-db-surplus": "政策咨询",
    "20260610-fr-aspa-online": "行政管理",
    "20260609-uk-transfer-scams": "政策咨询",
    "20260609-uk-waspi-decision": "行政安排",
    "20260609-kr-basic-pension-forum": "政策讨论",
}

IMPORTANCE_MAP = {
    "20260613-au-apra-longevity": 3,
    "20260610-uk-db-surplus": 4,
    "20260610-fr-aspa-online": 3,
    "20260609-uk-transfer-scams": 4,
    "20260609-uk-waspi-decision": 3,
    "20260609-kr-basic-pension-forum": 3,
}


def meta_text(entry: dict) -> str:
    extra = ""
    if entry.get("supplemental_urls"):
        extra = "；补充核验页（URL）：" + "；".join(entry["supplemental_urls"])
    ready_suffix = "。"
    if "咨询" in entry["nature"] or "讨论" in entry["nature"]:
        ready_suffix = f"，但需标注为{entry['nature']}，不得表述为已落地政策。"
    return (
        f"原始详情页（URL）：{entry['url']}{extra}。"
        f"原文发布日期：{entry['original_pub_date']}；政策生效日期：{entry['policy_effective_date']}；"
        f"是否属于本期窗口：是；是否已经核验：是；是否可以进入正式稿：是{ready_suffix}"
    )


def main() -> None:
    site_data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    report_data = json.loads(REPORT_DATA.read_text(encoding="utf-8"))

    entries = site_data["entries"]
    entries = [
        entry
        for entry in entries
        if not (START <= entry.get("date", "") <= END and entry.get("url") in {r["url"] for r in report_data["entries"]})
    ]

    max_id = max(int(entry["id"]) for entry in entries if isinstance(entry.get("id"), int))
    new_entries = []
    for idx, report_entry in enumerate(report_data["entries"], 1):
        numeric_id = max_id + idx
        verification_note = meta_text(report_entry)
        content = f"{report_entry['summary']} 原文引述：“{report_entry['quote']}”。{verification_note}"
        new_entries.append(
            {
                "id": numeric_id,
                "country": report_entry["country"],
                "title": report_entry["title"],
                "content": content,
                "date": report_entry["original_pub_date"][:10],
                "category": CATEGORY_MAP[report_entry["id"]],
                "importance": IMPORTANCE_MAP[report_entry["id"]],
                "source": report_entry["source"],
                "url": report_entry["url"],
                "extra_url": "；".join(report_entry.get("supplemental_urls", [])),
                "original_pub_date": report_entry["original_pub_date"],
                "policy_effective_date": report_entry["policy_effective_date"],
                "in_report_window": True,
                "verified": True,
                "ready_for_report": True,
                "verification_note": verification_note,
            }
        )

    entries.extend(new_entries)
    site_data["entries"] = entries
    site_data["metadata"]["last_updated"] = "2026-06-13"
    site_data["metadata"]["report_period_end"] = "2026-06-13"
    site_data["metadata"]["total_entries"] = len(entries)
    site_data["metadata"]["data_version"] = "6.4-20260613-weekly"

    DATA_FILE.write_text(json.dumps(site_data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"added {len(new_entries)} entries")
    print(f"total {len(entries)}")
    for entry in new_entries:
        print(entry["id"], entry["date"], entry["country"], entry["title"])


if __name__ == "__main__":
    main()
