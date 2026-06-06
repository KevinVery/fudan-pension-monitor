import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "entries.json"


NEW_ENTRIES = [
    {
        "id": 341,
        "country": "英国",
        "title": "英格兰地方议员首次可选择加入地方政府养老金计划",
        "content": (
            "英国政府精算署2026年6月2日发布官方消息称，英格兰地方议员已可加入地方政府养老金计划（LGPS）。"
            "新规将地方议员、市长、副市长和伦敦议会成员纳入适用范围，相关服务年限自5月地方选举后的首个星期一开始可计入计划，"
            "加入方式为自愿选择加入。该条属于公共部门养老金覆盖范围扩展，原文同时说明政府精算署的分析为政策变化提供了成本证据。"
            "正式核验结论为：原文发布日期属于2026年5月31日至6月6日本期窗口，政策生效日期早于窗口但官方说明在本期发布；"
            "本条可进入正式稿，但不推断具体新增财政支出规模。"
        ),
        "date": "2026-06-02",
        "category": "政策调整",
        "importance": 4,
        "source": "英国政府精算署（Government Actuary's Department）",
        "url": "https://www.gov.uk/government/news/councillors-in-england-access-the-local-government-pension-scheme",
        "original_pub_date": "2026-06-02",
        "policy_effective_date": "2026年5月地方选举后的首个星期一，原文未列具体日历日",
        "in_report_window": True,
        "verified": True,
        "ready_for_report": True,
        "verification_note": "已下载并核验官方详情页；不是机构首页或列表页。",
    },
    {
        "id": 342,
        "country": "英国",
        "title": "职业养老金保存权益修正规则将允许向授权集合缴费计划无同意转移",
        "content": (
            "英国工作与养老金部2026年6月3日更新官方咨询结果页面，发布《2026年职业养老金计划保存权益修正规则》相关内容。"
            "规则将允许相关成员的货币购买权益在特定条件下、未经成员同意转移至已根据《2021年养老金计划法》第一部分授权的集合货币购买计划。"
            "该规则将于2026年7月31日生效。其政策含义在于为集合缴费型养老金制度补齐权益转移和接收计划资格规则，"
            "但不能被表述为已经发生大规模转移或成员待遇已经改变。"
        ),
        "date": "2026-06-03",
        "category": "法规更新",
        "importance": 4,
        "source": "英国工作与养老金部（Department for Work and Pensions）",
        "url": "https://www.gov.uk/government/consultations/retirement-collective-defined-contribution-pension-schemes/outcome/the-occupational-pension-schemes-preservation-of-benefit-amendment-regulations-2026",
        "original_pub_date": "2026-06-03",
        "policy_effective_date": "2026-07-31",
        "in_report_window": True,
        "verified": True,
        "ready_for_report": True,
        "verification_note": "已下载并核验官方详情页；条目仅保留该规则本身，未混入其他养老金法案议题。",
    },
    {
        "id": 343,
        "country": "英国",
        "title": "关系终止财务救济改革咨询将养老金分割和退休需要纳入重点评估",
        "content": (
            "英国司法部2026年6月5日发布“A Fairer End to Relationships”咨询文件及平等影响评估。"
            "文件并非已经生效的养老金改革，但在养老金和长期保障部分明确讨论养老金分割不足、退休收入需要和性别养老金差距。"
            "平等影响评估引用研究指出，离婚人群中达成养老金分割安排的比例较低，并显示女性缴费型养老金账户规模显著低于男性。"
            "该条应以“养老金相关政策咨询”口径记录，不能写成养老金分割规则已经改革或已经实施自动评定机制。"
        ),
        "date": "2026-06-05",
        "category": "政策咨询",
        "importance": 3,
        "source": "英国司法部（Ministry of Justice）",
        "url": "https://www.gov.uk/government/consultations/a-fairer-end-to-relationships/a-fairer-end-to-relationships-consultation-document",
        "original_pub_date": "2026-06-05",
        "policy_effective_date": "不适用，咨询阶段",
        "in_report_window": True,
        "verified": True,
        "ready_for_report": True,
        "verification_note": "已下载并核验咨询文件及平等影响评估；进入网站时明确标注为咨询阶段。",
    },
]


def main() -> None:
    data = json.loads(DATA_PATH.read_text(encoding="utf-8"))
    entries = data["entries"]

    new_urls = {entry["url"] for entry in NEW_ENTRIES}
    new_ids = {entry["id"] for entry in NEW_ENTRIES}
    entries = [
        entry
        for entry in entries
        if entry.get("id") not in new_ids and entry.get("url") not in new_urls
    ]
    entries.extend(NEW_ENTRIES)

    data["entries"] = entries
    metadata = data["metadata"]
    metadata["last_updated"] = "2026-06-06"
    metadata["report_period_end"] = "2026-06-06"
    metadata["total_entries"] = len(entries)
    metadata["data_version"] = "6.0-20260606-weekly-original-source-update"

    DATA_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"updated {DATA_PATH} with {len(NEW_ENTRIES)} entries; total={len(entries)}")


if __name__ == "__main__":
    main()
