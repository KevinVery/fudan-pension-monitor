#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Update entries.json - remove non-authoritative entries, add verified May 10-16 entries."""

import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'entries.json')

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

# ============================================================
# STEP 1: Remove non-authoritative entries
# ============================================================
# Remove entry ID 4 (Korea crypto - wublock123.com, non-authoritative)
# Remove entry ID 5 (China 22连涨 - 自媒体分析, explicitly non-official)
entries = [e for e in data['entries'] if e['id'] not in [4, 5]]

# Also remove entry 9 (Germany 4.24% - duplicate info, blog source)
# Entry 9 overlaps with entry 29 (which covers pension level safeguard more comprehensively)
# Keep entry 29 instead
entries = [e for e in entries if e['id'] != 9]

# ============================================================
# STEP 2: Add new verified entries (May 10-16, 2026)
# ============================================================

new_entries = [
    {
        "country": "澳大利亚",
        "title": "2026-27财年联邦预算案发布：超级年金Division 296税制7月生效，Payday Super改革确认",
        "content": "澳大利亚财长Jim Chalmers于2026年5月13日公布2026-27财年联邦预算案，确认多项超级年金重大变革：Division 296税制自7月1日起对总超级余额超300万澳元者增收30%附加税（预计影响约8万人，四年增收22亿澳元）；优惠缴费上限从30,000澳元上调至32,500澳元；Payday Super改革7月1日生效，雇主须在每个发薪后7个工作日内缴纳超级保证金（SG费率12%），替代原有季度缴纳周期。预算案包括总计640亿澳元节支措施。超级年金绩效测试现代化改革方案也已提出，拟调整新兴资产类别基准以鼓励投资住房、能源等。",
        "date": "2026-05-13",
        "category": "政策调整",
        "importance": 4,
        "source": "澳大利亚财政部 / ATO / Morningstar Australia",
        "url": "https://treasury.gov.au/policy-topics/superannuation"
    },
    {
        "country": "荷兰",
        "title": "三大工会发出罢工最后通牒，加快AOW退休年龄上调计划被宣布"政治死亡"",
        "content": "荷兰三大工会FNV、CNV和VCP于2026年5月11日联合向少数派内阁发出30天最后通牒：须撤回加快AOW国家养老金年龄上调的法律修正案，并放弃削减失业金和残疾金的计划，否则将发动全国性罢工。FNV主席Hans Spekman表示"这关乎人民的生存"。5月14日NRC商报报道该计划已"政治死亡"。内阁转向探索替代方案，包括"AOW的财政化"——让退休者逐步缴纳更多所得税，预计到2040年可增收50亿欧元/年。首批覆盖约950万劳动者的基金已完成新DC体系转换。DNB估算转型过程基金预计减持1,000至1,500亿欧元政府债券。",
        "date": "2026-05-11",
        "category": "政策改革",
        "importance": 5,
        "source": "荷兰中央政府(Rijksoverheid) / DutchNews.nl / NRC",
        "url": "https://www.rijksoverheid.nl/onderwerpen/pensioen/nieuws"
    },
    {
        "country": "法国",
        "title": "养老金改革暂停实施令正式公布：1968年出生者退休年龄回调至63岁9个月",
        "content": "法国政府于2026年5月7-8日在《官方公报》公布两项实施令（2026-344号和2026-345号），将2023年养老金改革暂停措施具体化。1968年出生者法定退休年龄从64岁回调至63岁9个月，1964-1967年出生者享有不同程度回调（62岁9个月至63岁6个月），仅1969年及之后出生者仍须64岁退休。暂停基于《2026年社会保障融资法》自9月1日生效，持续至2027年总统大选后。成本估算为2026年4亿欧元、2027年18亿欧元。长期职业生涯提前退休和残疾劳动者提前退休的实施细则同步公布。总理宣布召开"养老金与工作全国会议"寻求未来改革共识。",
        "date": "2026-05-08",
        "category": "政策改革",
        "importance": 5,
        "source": "法国官方公报(Journal Officiel) / Service-Public / Capital",
        "url": "https://www.legifrance.gouv.fr"
    },
    {
        "country": "德国",
        "title": "联邦参议院批准私人养老金改革法案，新体系2027年1月全面启动",
        "content": "德国联邦参议院（Bundesrat）于2026年5月8日最终批准《养老保障改革法案》（Altersvorsorgereformgesetz），完成全部立法程序。新体系自2027年1月1日启动：提供三种产品选择（无保证储蓄账户/ETF、80%保证组合、100%保证存款账户）；国家补贴最高540欧元/年；儿童补贴每孩300欧元/年；首次将自雇者和公务员纳入补贴范围；标准产品成本费用上限设为1.0%。"养老保障委员会"预计2026年夏季前提交法定养老保险长期改革方案。此前内阁批准的2027年预算框架拟削减联邦对法定养老保险补贴40亿欧元，DRV警告将导致缴费率上升。",
        "date": "2026-05-08",
        "category": "政策改革",
        "importance": 5,
        "source": "德国联邦劳动和社会事务部(BMAS) / 德国法定养老保险(DRV) / WSB-Berater",
        "url": "https://www.bmas.de/DE/Service/Presse/Meldungen/Rente/rente-meldungen.html"
    },
    {
        "country": "意大利",
        "title": "2027年起退休年龄因预期寿命调整上调：最长可达67岁5个月",
        "content": "基于ISTAT发布的预期寿命数据，意大利自2027年起养老金领取年龄将自动上调：老年养老金2027年升至67岁1个月、2028年67岁3个月、2029年67岁5个月；纯缴费制退休年龄从71岁升至71岁1个月（2027年）至71岁5个月（2029年）；普通提前退休缴费年限要求男性增至42年11个月、女性41年11个月（2027年）。精算调整不适用于重体力劳动和苦累工种（2027-2028年维持不变）。Isopensione自2027年起最大提前年限从7年缩减至4年。意大利养老金支出占GDP约18%（OECD均值为12%），OECD经济调查敦促探索中期削减第一支柱养老金成本的方案。",
        "date": "2026-05-15",
        "category": "政策改革",
        "importance": 4,
        "source": "意大利国家社会保障局(INPS) / Panorama / Il Mondo del Lavoro",
        "url": "https://www.inps.it/it/it/inps-comunica/notizie.html"
    },
    {
        "country": "英国",
        "title": "国家养老金年龄66→67过渡配套措施公布，养老金信贷改革方案启动公众咨询",
        "content": "英国DWP于2026年5月中旬公布国家养老金年龄66→67过渡期配套措施。数据显示截至5月约13%的60-65岁受影响人群仍不知晓此项变化。政府同步推出"重返工作岗位支持计划"，为在达到养老金年龄前失业的60岁以上人群提供最长12个月收入补贴（每周最高120英镑）和再培训券（最高1,000英镑）。养老金信贷改革方案于5月12日启动公众咨询，拟引入基于HMRC数据的"自动评定"机制，目标将领取率从63%提高至80%以上。2026/27财年全额新国家养老金为每周241.30英镑（年12,547英镑），已极度接近个税免征额12,570英镑。",
        "date": "2026-05-12",
        "category": "政策调整",
        "importance": 4,
        "source": "英国工作与养老金部(DWP) / GOV.UK / 伯明翰邮报",
        "url": "https://www.gov.uk/government/organisations/department-for-work-pensions"
    },
    {
        "country": "巴西",
        "title": "INSS公布2026年最新标准：最低养老金上调至1,621雷亚尔，排队人数从310万降至260万",
        "content": "巴西国家社会保险局（INSS）于2026年5月13日公布2026年最新养老金标准：最低养老金上调6.79%至1,621雷亚尔/月，最高养老金上限上调3.9%至8,475.55雷亚尔/月。5月支付按社保号码末位数字分批进行。INSS福利申请排队人数从2月历史峰值310万人降至4月的260万人（降幅约16%），改善归因于限制重复申请、企业数字通道系统上线（5月15日生效的INSS第156号令）等行政改革。2019年养老金改革过渡规则继续推进：2026年积分制要求男性103分、女性93分；渐进式最低年龄男性64岁6个月+35年缴费、女性59岁6个月+30年缴费。",
        "date": "2026-05-13",
        "category": "政策调整",
        "importance": 3,
        "source": "巴西国家社会保险局(INSS) / Agência Gov / IG Economia",
        "url": "https://www.gov.br/inss/pt-br/noticias"
    },
    {
        "country": "印度",
        "title": "马哈拉施特拉邦公布修订版NPS实施细则，PFRDA允许NPS资金配置另类投资基金",
        "content": "马哈拉施特拉邦政府于2026年5月6-8日发布修订版国民养老金计划（Revised NPS）实施细则，允许现有NPS参保雇员在2026年12月31日前转入修订版计划。核心条款：缴费满20年以上者退休时获最后工资50%的保证养老金加物价补贴，最低保证养老金7,500卢比/月。泰米尔纳德邦首席部长斯大林此前于5月2日宣布推出TAPS保证养老金计划，实质恢复OPS待遇。全印铁路联合会秘书长表示仅约30万雇员选择UPS，超70万仍在观望。同时，PFRDA新规允许NPS最多1%资产（约1,700亿卢比/20亿美元）配置另类投资基金（AIF），为私募股权和风险资本打开通道。",
        "date": "2026-05-08",
        "category": "政策改革",
        "importance": 4,
        "source": "印度经济时报 / 商业标准报 / PFRDA / AIRF",
        "url": "https://pfrda.org.in/media/press-releases"
    }
]

entries.extend(new_entries)

# ============================================================
# STEP 3: Re-index IDs
# ============================================================
for i, entry in enumerate(entries):
    entry['id'] = i + 1

# ============================================================
# STEP 4: Update metadata
# ============================================================
data['metadata']['last_updated'] = '2026-05-16'
data['metadata']['report_period_end'] = '2026-05-16'
data['metadata']['total_entries'] = len(entries)
data['metadata']['data_version'] = '4.0-may16-update'

# ============================================================
# STEP 5: Save
# ============================================================
data['entries'] = entries

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Updated entries.json: {len(entries)} entries (removed non-authoritative, added May 10-16 entries)")
print(f"Period: {data['metadata']['report_period_start']} ~ {data['metadata']['report_period_end']}")
print(f"Countries covered: {len(set(e['country'] for e in entries))}")

# Country breakdown
country_count = {}
for e in entries:
    country_count[e['country']] = country_count.get(e['country'], 0) + 1
for c, n in sorted(country_count.items(), key=lambda x: -x[1]):
    print(f"  {c}: {n}")
