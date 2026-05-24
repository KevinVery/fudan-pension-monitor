"""
============================================================
  [Skill] 全球养老金政策动态追踪 - 周度更新工作流
  用法: python scripts/weekly_skill.py
============================================================

这是一个"技能(Skill)"脚本，整合了周度更新的完整流程：
  1. 展示所有权威数据源清单
  2. 检查现有条目数据概览
  3. 使用WebFetch验证新政策信息
  4. 引导添加新条目
  5. 生成Word周报
  6. 部署到GitHub Pages

数据文件: data/entries.json
"""

import json
import os
import sys
import subprocess
from datetime import date, datetime

# Windows GBK encoding fix
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass
os.environ['PYTHONIOENCODING'] = 'utf-8'

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'data', 'entries.json')

# ============================================================
# 权威数据源清单（来自 AI工作流文件/ 的综合整理）
# 涵盖16国官方政府、社保机构、统计部门
# ============================================================
COUNTRY_SOURCES = {
    '美国': [
        ('SSA社会保障署', 'https://www.ssa.gov/news/en/newsletter/index.html'),
        ('SSA新闻稿', 'https://www.ssa.gov/news/en/press/releases/index.html'),
        ('IRS退休计划', 'https://www.irs.gov/retirement-plans/employee-plans-news'),
        ('PBGC养老金担保', 'https://www.pbgc.gov/news'),
        ('DOL劳工部', 'https://www.dol.gov/agencies/ebsa'),
    ],
    '英国': [
        ('GOV.UK养老金', 'https://www.gov.uk/government/collections/hm-revenue-and-customs-pension-schemes-newsletters'),
        ('TPR养老金监管局', 'https://www.thepensionsregulator.gov.uk/en/media-hub/press-releases'),
        ('PPF养老金保护基金', 'https://www.ppf.co.uk/news'),
        ('DWP工作养老金部', 'https://www.gov.uk/government/organisations/department-for-work-pensions'),
    ],
    '加拿大': [
        ('OSFI联邦监管', 'https://www.osfi-bsif.gc.ca/en/supervision/pensions/infopensions-newsletters'),
        ('Treasury Board', 'https://www.canada.ca/en/treasury-board-secretariat/services/pension-plan/news-notices-pensions-benefits.html'),
        ('Retraite Québec', 'https://www.retraitequebec.gouv.qc.ca/en/salle_presse/Pages/salle-de-presse.aspx'),
        ('ESDC统计', 'https://www.canada.ca/en/employment-social-development/programs/pensions/pension/statistics.html'),
    ],
    '澳大利亚': [
        ('Services Australia', 'https://www.servicesaustralia.gov.au/news-for-retirement-years'),
        ('DSS社会服务部', 'https://ministers.dss.gov.au/tanya-plibersek/media-releases'),
        ('Treasury财政部', 'https://treasury.gov.au/policy-topics/superannuation'),
        ('ATO税务局', 'https://www.ato.gov.au/tax-and-super-professionals/for-superannuation-professionals/super-funds-newsroom'),
        ('APRA审慎监管局', 'https://www.apra.gov.au/news-and-publications/39'),
    ],
    '日本': [
        ('厚生劳动省年金局', 'https://www.mhlw.go.jp/stf/houdou/bukyoku/nenkin.html'),
        ('日本年金机构', 'https://www.nenkin.go.jp/allNewsList.html'),
        ('GPIF', 'https://www.gpif.go.jp/'),
    ],
    '德国': [
        ('BMAS劳动社会部', 'https://www.bmas.de/DE/Service/Presse/Meldungen/Rente/rente-meldungen.html'),
        ('DRV法定养老保险', 'https://www.deutsche-rentenversicherung.de/DRV/DE/Ueber-uns-und-Presse/Presse/Meldungen/aktuelles_node.html'),
        ('DRV新闻稿', 'https://www.deutsche-rentenversicherung.de/DRV/DE/Ueber-uns-und-Presse/Presse/Pressemitteilungen/pressemitteilungen_node.html'),
        ('Destatis统计局', 'https://www.destatis.de/DE/Im-Fokus/Rente/_inhalt.html'),
    ],
    '法国': [
        ('Service-Public', 'https://www.service-public.fr/particuliers/actualites'),
        ('Info Retraite', 'https://www.info-retraite.fr/portail-info/sites/PortailInformationnel/home/actualites-1.html'),
        ('Assurance retraite', 'https://www.lassuranceretraite.fr/portail-info/hors-menu/toutes-les-actualites.html'),
        ('Agirc-Arrco', 'https://www.agirc-arrco.fr/nous-connaitre/nos-actualites/'),
    ],
    '意大利': [
        ('INPS', 'https://www.inps.it/it/it/inps-comunica/notizie.html'),
        ('劳动部', 'https://www.lavoro.gov.it/temi-e-priorita/previdenza/Pagine/default'),
    ],
    '中国': [
        ('国务院政策库', 'https://sousuo.www.gov.cn/zcwjk/policyDocumentLibrary?orpro=&q=养老&t=zhengcelibrary'),
        ('人社部', 'https://chrm.mohrss.gov.cn/'),
        ('统计局', 'https://www.stats.gov.cn/sj/'),
        ('财政部', 'http://www.mof.gov.cn/zhengwuxinxi/caizhengxinwen/'),
    ],
    '韩国': [
        ('保健福祉部', 'https://www.mohw.go.kr/board.es?bid=0027&mid=a10503010100'),
        ('NPS国民年金', 'https://www.nps.or.kr/allNewsList.html'),
        ('NPS新闻稿', 'https://www.nps.or.kr/info/press/index.html'),
    ],
    '巴西': [
        ('INSS', 'https://www.gov.br/inss/pt-br/noticias'),
        ('Previdência社保部', 'https://www.gov.br/previdencia/pt-br/noticias'),
        ('PREVIC监管局', 'https://www.gov.br/previc/pt-br/noticias'),
    ],
    '印度': [
        ('DoPPW养老金部', 'https://doppw.gov.in/en/news'),
        ('PFRDA监管局', 'https://pfrda.org.in/media/press-releases'),
        ('EPFO公积金局', 'https://www.epfindia.gov.in/site_en/Press_Release.php'),
    ],
    '荷兰': [
        ('Rijksoverheid', 'https://www.rijksoverheid.nl/onderwerpen/algemene-ouderdomswet-aow'),
        ('SVB社保银行', 'https://www.svb.nl/nl/aow'),
    ],
    '阿根廷': [
        ('ANSES', 'https://www.anses.gob.ar/noticias'),
        ('Boletín Oficial', 'https://www.boletinoficial.gob.ar/seccion/primera'),
    ],
    '俄罗斯': [
        ('政府官网', 'https://government.ru/'),
        ('劳动部', 'https://mintrud.gov.ru/'),
        ('社会基金', 'https://sfr.gov.ru/'),
    ],
    '墨西哥': [
        ('IMSS社保局', 'https://www.imss.gob.mx/pensiones'),
        ('CONSAR', 'https://www.gob.mx/consar'),
        ('DOF官方公报', 'https://www.dof.gob.mx/'),
    ],
}

# 国家关键词（用于搜索和验证）
COUNTRY_KEYWORDS = {
    '美国': ['Social Security', 'COLA', '401(k)', 'Social Security Trust Fund', 'Retirement Earnings Test',
             'SSA', 'PBGC', 'multi-employer pension', 'SECURE Act'],
    '英国': ['state pension', 'triple lock', 'auto-enrolment', 'automatic enrolment', 'pension scheme',
             'DWP', 'Pension Schemes Act', 'Pension Regulator', 'PPF'],
    '加拿大': ['CPP', 'OAS', 'Old Age Security', 'Guaranteed Income Supplement', 'RRSP',
              'TFSA', 'CPP2', 'QPP', 'GIS'],
    '澳大利亚': ['superannuation', 'super guarantee', 'SG', 'payday super', 'MySuper',
                'retirement income', 'SMSF', 'Age Pension', 'ATO super'],
    '日本': ['公的年金', '国民年金', '厚生年金', 'GPIF', '年金改革', '確定拠出年金',
             'iDeCo', '年金制度'],
    '德国': ['Rente', 'gesetzliche Rentenversicherung', 'Rentenversicherung', 'Rentenpaket',
             'Rentenbeitrag', 'Mütterrente', 'Betriebsrente', 'Riester-Rente'],
    '法国': ['retraite', 'pension', 'réforme des retraites', 'Agirc-Arrco', 'minimum contributif'],
    '意大利': ['pensioni', 'INPS', 'previdenza', 'Quota 103', 'APE sociale', 'Opzione donna'],
    '中国': ['养老金', '养老保险', '个人养老金', '延迟退休', '基本养老保险',
             '第三支柱', '社保基金', '城乡居民养老保险'],
    '韩国': ['국민연금', 'NPS', '기초연금', '퇴직연금', '연금개혁', '노령연금'],
    '巴西': ['INSS', 'aposentadoria', 'Previdência Social', 'RGPS', 'BPC', 'pensão'],
    '印度': ['NPS', 'EPFO', 'EPS', 'pension', 'DoPPW', 'PFRDA', 'OPS', 'retirement benefits'],
    '荷兰': ['AOW', 'pensioen', 'AOW-leeftijd', 'SVB', 'Algemene Ouderdomswet'],
    '阿根廷': ['ANSES', 'jubilación', 'PUAM', 'movilidad', 'haberes previsionales'],
    '俄罗斯': ['пенсия', 'пенсионное обеспечение', 'индексация', 'СФР', 'страховая пенсия'],
    '墨西哥': ['AFORE', 'CONSAR', 'IMSS', 'ISSSTE', 'pensión', 'SAR', 'SIEFORE'],
}

# 搜索关键词（英文/中文混合，用于WebSearch）
SEARCH_QUERIES = [
    # 通用养老金政策
    'pension reform 2026',
    'pension policy 2026',
    'social security reform 2026',
    'retirement age 2026',
    'public pension fund investment 2026',

    # OECD/国际组织
    'OECD pension 2026',
    'World Bank pension 2026',
    'ILO social security 2026',

    # 各国专题
    'Social Security COLA 2026',
    'state pension triple lock 2026',
    'CPP OAS 2026 Canada',
    'superannuation guarantee Australia 2026',
    'GPIF Japan 2026',
    'NPS South Korea 2026',
    'INSS Brazil 2026',
    'ANSES Argentina 2026',
]


def print_header(text):
    """打印分区标题"""
    width = 68
    line = "=" * width
    print(f"\n{line}")
    print(f"  {text}")
    print(f"{line}")


def load_entries():
    """加载当前条目数据"""
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def show_dashboard():
    """显示当前数据看板"""
    data = load_entries()
    entries = data['entries']
    meta = data['metadata']

    print(f"\n[数据看板] 当前数据看板")
    print(f"  总条目: {meta['total_entries']} 条")
    print(f"  覆盖国家: {meta['countries_covered']} 个")
    print(f"  报告周期: {meta['report_period_start']} ~ {meta['report_period_end']}")
    print(f"  最后更新: {meta['last_updated']}")

    # 按国家统计
    print(f"\n  各国条目数:")
    country_count = {}
    for e in entries:
        country_count[e['country']] = country_count.get(e['country'], 0) + 1
    for c, n in sorted(country_count.items(), key=lambda x: -x[1]):
        print(f"    {c}: {n} 条")

    # 按分类统计
    print(f"\n  分类分布:")
    cat_count = {}
    for e in entries:
        cat_count[e['category']] = cat_count.get(e['category'], 0) + 1
    for c, n in sorted(cat_count.items(), key=lambda x: -x[1]):
        print(f"    {c}: {n} 条")

    return entries, meta


def list_sources():
    """列出所有权威数据源"""
    print_header("[Sources] 16国权威数据源清单")
    print("  以下为官方政府/社保机构数据源，供WebFetch验证使用：")
    for country, sources in COUNTRY_SOURCES.items():
        print(f"\n  【{country}】")
        for name, url in sources:
            print(f"    • {name}: {url}")


def show_weekly_workflow():
    """显示周度更新流程"""
    print_header("[Workflow] 周度更新工作流")
    print("""
  步骤 1: 搜索 — 使用16国关键词搜索最新动态
          python scripts/weekly_skill.py --search

  步骤 2: 验证 — 对候选条目使用WebFetch验证权威来源
          (使用 WebFetch 工具在Claude Code中操作)

  步骤 3: 添加 — 使用交互式工具添加新条目
          python scripts/add_entry.py

  步骤 4: 生成 — 生成Word周报
          python scripts/generate_report.py

  步骤 5: 部署 — 推送到GitHub Pages
          scripts\\deploy.bat
    """)


def show_keywords():
    """显示各国搜索关键词"""
    print_header("[Keywords] 16国搜索关键词")
    for country, keywords in COUNTRY_KEYWORDS.items():
        kw_str = ' | '.join(keywords[:5])
        extra = f" +{len(keywords)-5} more" if len(keywords) > 5 else ''
        print(f"  {country}: {kw_str}{extra}")


def generate_search_urls():
    """生成WebFetch用的URL列表"""
    print_header("[URLs] WebFetch URL清单")
    print("  以下URL可用于WebFetch工具验证最新政策动态：")
    for country, sources in COUNTRY_SOURCES.items():
        print(f"\n  【{country}】")
        for name, url in sources:
            print(f"    {name}: {url}")

    print(f"\n  搜索查询关键词:")
    for q in SEARCH_QUERIES:
        print(f"    • {q}")


def main():
    print_header("[Skill] 全球养老金政策动态追踪 - 周度更新技能")
    print(f"  日期: {date.today().isoformat()}")
    print(f"  数据文件: {DATA_FILE}")

    # 检查数据文件
    if not os.path.exists(DATA_FILE):
        print(f"\n  ❌ 数据文件不存在: {DATA_FILE}")
        sys.exit(1)

    # 显示当前数据看板
    show_dashboard()

    # 显示周度工作流
    show_weekly_workflow()

    # 列出数据源（可选择）
    if '--sources' in sys.argv or '-s' in sys.argv:
        list_sources()

    # 显示关键词
    if '--keywords' in sys.argv or '-k' in sys.argv:
        show_keywords()

    # 生成URL清单
    if '--urls' in sys.argv or '-u' in sys.argv:
        generate_search_urls()

    # 搜索模式
    if '--search' in sys.argv:
        print_header("[Search] 搜索模式")
        print("  请在 Claude Code 中使用 WebSearch 工具搜索以下关键词：")
        for q in SEARCH_QUERIES:
            print(f"    WebSearch(query=\"{q}\")")

    line = "=" * 68
    print(f"\n{line}")
    print(f"  [Tip] 提示: 使用以下参数快速访问功能")
    print(f"    --sources   列出所有数据源")
    print(f"    --keywords  列出搜索关键词")
    print(f"    --urls      生成WebFetch URL清单")
    print(f"    --search    显示搜索查询")
    print(f"{'=' * 68}\n")


if __name__ == '__main__':
    main()
