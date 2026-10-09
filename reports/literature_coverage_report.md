# 文献覆盖报告与作者核对事项

目标：ACM SAC 2027 KNLP；主稿保留匿名官方格式，按总计不超过 8 页组织。以下统计与编辑说明位于正文之外。

## 2024–2026 年同类论文抽样

采用两个有目的的参照组：SAC 八页应用 NLP/LLM 实证论文用于篇幅参照；EACL/ACL/Findings 的事件、体貌和构式评测论文用于主题参照。两个参照组不能混合成会议总体分布。总 PDF 页数包含参考文献及附录，与正文页数不同。

| 论文 | 会议 | 所查 PDF 页数 | 参考文献条数 | 版本 |
|---|---|---:|---:|---|
| [SimRE](https://lbd.udc.es/Repository/Publications/Drafts/1741695248136_227_220.pdf) | SAC 2025 | 8 | 46 | 作者托管正式排版，DOI 10.1145/3672608.3707758 |
| [Robust LLM-as-a-Judge Validators](https://rdegiovanni.github.io/publications/files/SAC2026_validators.pdf) | SAC 2026 | 8 | 35 | 作者托管正式排版，DOI 10.1145/3748522.3779926 |
| [Process Knowledge Extraction…](https://github.com/patriziobellan86/Process-Knowledge-Extraction-and-Knowledge-Graph-Construction-Through-Prompting) | SAC 2024 | 8 | 32 | 作者匿名稿，PDF DOI 为占位符，单列 |
| [Retrofitting Competency Questions](https://arxiv.org/abs/2311.05662) | SAC 2024 对应工作 | 9 | 28 | 2023 年作者预印本，PDF venue/DOI 为占位符，单列 |
| [Human Temporal Inferences Go Beyond Aspectual Class](https://aclanthology.org/2024.eacl-long.115/) | EACL 2024 | 11 | 31 | 官方发表版 |
| [World Knowledge Resolves Some Aspectual Ambiguity](https://aclanthology.org/2025.findings-acl.683/) | Findings ACL 2025 | 14 | 25 | 官方发表版 |
| [CoRE](https://aclanthology.org/2025.findings-acl.992/) | Findings ACL 2025 | 21 | 43 | 官方发表版 |
| [CxMP](https://aclanthology.org/2026.acl-long.2132/) | ACL 2026 | 15 | 42 | 官方发表版 |

SAC 正式排版组实测范围为 **35–46 篇（n=2，中位数 40.5）**；最接近主题的 NLP 组为 **25–43 篇（n=4，中位数 36.5）**。两个 SAC 作者稿仅报告所下载版本的 32、28 条，不纳入正式排版组范围。SAC 样本不是全部来自 KNLP，也不是事件语义的直接竞争工作：SimRE 属语义相似度应用，Validators 属 LLM 行为评测。因此这里只给出可复核的小样本参照，不能据此声称“会议普遍要求 35–46 篇”或推算录用概率。

计数从 References 标题到附录边界：SAC 核对连续编号 1…N；ACL 按双栏阅读顺序识别悬挂缩进条目首行。保留每条首行位置、来源链接及 PDF SHA-256，并检查参考文献页的起止边界和编号。复核脚本为 `scripts/audit_literature_coverage.py`，逐篇记录为 `reports/literature_coverage_audit.json`。第三方全文仅作本地阅读，不进入匿名复现包。

## 本稿 14 → 32 篇

新增 18 篇，每篇都有正文使用位置，未把计数参照论文强行加入正文。

| 补齐方向 | 新增来源 | 正文作用 |
|---|---|---|
| 进行体语义基础 | Landman 1992 | 将进行事件与终点的区分放回既有理论脉络；有限历史 oracle 明确为本文任务定义 |
| 可执行规则评价 | ProofWriter 2021 | 比较规则推导标签与证据约束历史标签，准确界定方法关系 |
| 时间推理评价 | TimeBench、TRAM 2024 | 区分广泛时间推理任务与本文 occurrence/culmination/unknown 评价 |
| 最小对与表面线索 | BLiMP 2020、Gururangan et al. 2018 | 对照可接受性最小对、NLI 线索和本文有监督表面诊断 |
| 概率测量 | Hu and Levy 2023 | 区分提示诱发的主观 q 与直接字符串概率，不扩大成校准结论 |
| 实际统计方法 | Holm 1979、Benjamini–Hochberg 1995、Efron 1979、Bates et al. 2015 | 为多重校正、bootstrap 原理和 lme4 实现提供来源；本实验的聚类单位仍独立写明 |
| 实际实验基线 | Salton–Buckley 1988、scikit-learn 2011 | 明确 TF-IDF unigram + logistic、C=1、固定种子、无结果调参 |
| 实际模型 | Qwen3、Llama 3、Gemma 3、DeepSeek-V3.2 报告及 Ministral 官方卡 | 对应六主系统与独立 stress 模型；注明技术报告或模型卡类型 |

已有最接近的 ImperfectiveNLI、其批评、Pruś 两篇、CoRE、CxMP，以及 Vendler、Moens–Steedman、Krifka、COGS、HANS、自然逻辑、hypothesis-only 和 CheckList 均保留。未新增未运行的模型结果、数据集得分或“首次/最优”主张。32 篇低于两个 SAC 格式样本的最低 35 篇，但处于同主题组实测区间；最终按相关性取舍，不为填补三条数量差额添加无关工作。

新增作者、标题、年份、发表来源及 DOI/官方链接逐条记录于 `reports/literature_citation_verification.json`。普通规模作者列表按官方记录保留；大型模型团队采用首作者/团队加 et al.。ACL 工作采用正式版本，技术报告与模型卡按其真实类型列出，同一工作不重复列预印本和正式版。

## 尚需留意的覆盖边界

1. **SAC 样本覆盖**：正式排版组仅两篇且跨 track；2024 两篇只有作者稿。未取得其最终 PDF 的参考文献条数，不将作者版本冒充正式版本。后续取得正式版本时可扩大参照样本；这不改变本稿实验结论。
2. **全文访问**：Landman 1992 的出版商/作者机构元数据已核实，订阅全文未取得。正文只作一般理论定位，不引用其具体证明或声称有限 oracle 与该理论等价。Salton–Buckley 的出版商索引元数据与摘要已核实，完整网页返回 403；正文仅归属 term-weighting 来源，不声称实现完全相同。若进一步展开这两项理论细节，应先取得全文。
3. **范围相关的未来扩展**：本稿集中于单 episode、英语、指定 endpoint readings。跨语言体貌理论、叙事级隐含结果和额外竞争 benchmark 的直接同协议实验尚未覆盖；当前稿不提出这些范围的经验结论，也不把未运行比较写入结果。
4. **持续更新**：目前最接近的 2026 原论文与批评已纳入。提交前如新增直接相关正式版本，需替换对应预印本并复核论断；不能机械增加版本条目。

全部新增条目已与正文引用匹配；原始标签、回应数据、统计估计、完整主检验及反例保留。此次是文献与论证修订，没有新实验。
