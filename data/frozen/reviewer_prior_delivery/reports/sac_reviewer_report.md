# SAC KNLP 模拟审稿报告

审稿对象：当前八页《Endpoint Inference under Compatible Histories: A Theory-Driven Event Benchmark for Language Models》，32 篇参考文献。审稿依据：正文、有限历史 oracle、生成样本 F141、表面基线逐单元结果及提示定义。本报告模拟审稿判断，不是会议实际评审或录用预测；没有修改稿件或实验数据。

**总体意见：倾向弱拒，处于边缘稿范围。** 文章有可发表的诊断结果，复现工程和基本统计组织较完整；当前主要障碍是贡献的增量性与评测的区分效度。对于 SAC KNLP，题目与 LM/knowledge、语言推理方向相关，但需要更明确说明这项诊断比已有事件评测多揭示什么，以及它在简单模板线索之外仍能测量什么。SAC 官方选择标准包括原创性、技术贡献、表达质量和 track 相关性，未规定本文使用的评分标尺：[KNLP CFP](https://knlp-sac.github.io/2027/call_for_papers.html)。

**工作概述。** 本文通过证据保留的兼容事件历史定义 E/C/U，以同词根的 bounded/activity targets、Real/Nonce/Micro 三种表达及三种证据条件构造 120 个主 family。六系统与 DeepSeek 匹配 stress 结果表明，显式过程正确率可达 100%，而自然语言 unknown recall 仍明显不足；负 completion-score contrast 还能同时掩盖 unknown→contradicted 和活动发生判断错误。这是全文最有价值的发现。

**优点。**

1. 三类 truth condition 与三类错误有明确对应，图 1 表现的是证据如何筛选历史；图 2 展示未知终点与发生事实，较好地服务于核心论证。
2. 理论驱动的 gold 有明确、可执行的任务定义。在指定 episode、witness 与 endpoint readings 下，理论标签可以作为合理参考标准，不应因没有人工标注就否定。文章也没有把这些标签包装成独立现实世界观测。
3. 多系统、同 family stress、标签控制、表述变体、完整主检验和表面基线形成有用的诊断组合。尤其值得保留的是 Nonce 下的发生事实错误，而不仅是 Real 与 Micro 的总体得分差。
4. 主检验多重校正和失败的 mixed fits 得到披露；缺陷修正的原始结果也保留。未看到应仅因不符合故事而删除的结果。

**影响录用的主要问题，按优先级排列。**

**1. 表面线索可恢复性影响 benchmark 的区分效度。** §4.7 的 TF-IDF unigram + logistic 在主集达到 95.4% accuracy / 90.7% macro accuracy。进一步检查已存在的 `reports/surface_baselines.json`，该基线对 Real-neutral bounded 与 activity 两个单元均为 120/120，对对应 Micro-neutral 单元也均为 120/120。与此同时，Real-neutral 前提明确写出 “Nothing in the account says whether any required endpoint was reached…”，activity 目标又得到直接的发生 witness。activity 全部 1,080 个主 items 均为 E。

这些事实没有推翻报告中的 LLM 错误，却使评测成功可以由有限模板线索完成，而无需证明模型保留一般事件组合结构。Held-renderer 的 16.7-point 基线下降提供了重要证据，但单一新 renderer 还不能区分模板迁移与结构泛化。若作为新 benchmark 投稿，建议增加独立保留的词项/句法实现，或在固定 gold 下解除 “是否说明终点” 的固定措辞与标签的对应，并报告简单基线及 LLM 的分类别结果。无需引入人工 gold；可使用同一形式规范的新受控 realization。若不能补实验，应把贡献明确定位为这一受控构造集上的诊断，而减少广义 event-semantic competence 的解释。

**2. 三种呈现与目标对比尚不能定位单一机制。** §3.2–3.3 已正确承认 presentation packages 不同。但 §5 中 “distinguish rule application from language interpretation” 和 “localizing interpretation difficulty” 比实际识别条件更强。Real、Nonce、Micro 同时改变长度、定义负担、命名、符号与措辞；F141 bounded/activity pair 的完整 premise 也不同。Micro 全对、Real 有错，可以确定输入表达敏感性，不能单独确定语言解释环节是造成差异的机制。

建议主稿给出一组完整三种 premise/hypothesis，而不仅是 VP excerpts；明确哪些内容属于共享证据，哪些是目标、定义或表达新增信息。更有鉴别力的补充是 shared-premise dual-target 或更接近长度/定义匹配的比较。既有 Real-definition 控制应集中报告核心 unknown 与 occurrence 单元，而不只给总体 accuracy change 范围。q(B)−q(A) 在当前设置中应始终称为目标与前提包的配对分数差；它并非同一文本条件下的两个目标概率的纯组合效应。

**3. 可执行 truth table 与研究创新需要更清楚区分。** “所有历史为真/为假/混合” 是既有模型论式三值推断定义。本文的实际新意更可能是将其落实到 endpoint/occurrence 的受控任务，并与呈现条件和类别错误联动。当前第一项贡献容易被读成新的推理形式，而实际 oracle 只有两类代表历史和固定阈值。

已有 CoRE 研究 context/condition 与事件 outcome，CxMP 已结合构式最小对和 pseudoword；文章有准确引用，却还需要更具体地证明“旧评测/旧 completion score 会如何把本文的两种不同错误合并”。建议用真实结果构成一个紧凑反例：在同一组 items 上同时展示 score gap、U→C 与 occurrence failure，说明新增诊断实际改变了哪种研究判断。此项多可用已有结果完成，无须扩大理论新颖性。

相关来源：[CoRE](https://aclanthology.org/2025.findings-acl.992/)、[CxMP](https://aclanthology.org/2026.acl-long.2132/)。

**4. 主检验与当前中心发现的主次关系不够紧。** 全文最强的主张涉及 categorical unknown/occurrence errors，而表 4 的五个 prespecified contrasts 中四个为 q，另一个为 structural-rule gain。当前不是“没有分类证据”：表 3、图 2 和 secondary reports 已有相关证据；问题是正文最显眼的统计表主要验证另一组问题。

建议用一张紧凑的 error-profile 表连接核心主张与 Real/Nonce/Micro 分类结果及匹配差异，说明哪些是预先规定的 primary tests，哪些是 descriptive/secondary analyses。保留完整 30-test family，不能事后把更显著的结果改称预设主检验。现有 marginal CI 已有清楚说明，无须在所有段落重复；对于决定 presentation 比较的关键差异，若作跨构造推广解释，应集中提供相应配对不确定性。Structural-rule 未显著只支持没有检出改善，不支持规则干预一般无效。

**5. 十二词项与 family 数不能等同于广泛语言覆盖。** 120 families 对重复模板中的错误定位有价值，但分布只包含 12 lemmas、两个基础 renderer。Bootstrap 考虑 lexical blocks 是正确做法，却不会自动扩大词汇或构式覆盖。尤其 quantity/path/incremental 三个 strata 的设计动机应在结果中得到检验或明确只用于构造覆盖。建议补充已有数据的 per-lemma/per-stratum error analysis，检查中心现象是否由少数词项驱动；若主张超出该构造集，则进一步需要保留词项或构式测试。此问题不要求人工标注，也不要求将理论 gold 改成经验 gold。

**写作与可直接修复的问题。**

- §4.2 最后一句的交叉引用已损坏。源文件包含 `Section~` 后换行再 `ef{sec:robustness}`，当前 PDF 实际显示 “Section efsec:robustness”。应修复为有效的 `\ref`；“编译无 undefined references” 没有捕获这类普通文本错误。
- 多个 bibliography 条目是 `et al..`，存在双句点；手工参考文献的会议、期刊和技术报告格式也不一致。属于小修，32 条数量本身不是接收或拒稿依据。
- Abstract 中 “for four systems with over 91% aggregate accuracy” 宜明确为 Real accuracy，以免误读为跨 presentation aggregate。
- 各 prompt 直接包含 all-history label definition，而 structural guidance 增量相对短小。其无显著改善需要结合这个已较充分的 baseline instruction 解读。
- API 费用、payload 等细节有复现价值，但篇幅紧张时可压缩，优先给完整 stimulus、类别错误和现有 definition/renderer 控制的核心单元结果。

**给作者的关键问题。**

1. 消除固定 outcome-unspecified wording 与标签关联后，最重要的 unknown/occurrence 错误是否仍出现？
2. Real-definition 在核心 unknown/occurrence cells 上是否缩小 Real–Nonce 差异，还是只改善其他单元？
3. 主要失败是否跨十二词项与三个 strata 分布？哪个已有结果最直接证明新诊断纠正了旧评分会产生的研究判断？

**决定说明。** 我不会因理论 gold、没有人工复核或没有新模型算法而拒稿。当前倾向弱拒，是因为 benchmark 的结构诊断价值还未充分与模板/指令效应区分，而方法的新增研究价值仍主要由概念叙述支撑。若补齐线索解除或更强 held-out 测试、展示集中分类诊断、收紧机制解释，本稿可进入更有说服力的接收讨论范围。最优先投入应是增强评测鉴别力，而不是继续扩展文献数量或放大措辞。
