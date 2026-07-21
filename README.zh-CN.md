# Reference Verify

[English](README.md) | **简体中文**

`reference-verify` 是一个用于严格核验学术参考文献的 Codex skill。它适合处理 BibTeX、参考文献表以及 CSV/XLSX 文献数据，重点检查正式出版信息、DOI、页码、会议地点和期刊/会议名称一致性。

## 核心功能

- 保留原始论文标题、BibTeX key 和条目顺序。
- 优先核对出版社、官方会议论文集、DOI 落地页等一手来源。
- 检查 arXiv、OpenReview 或 workshop 论文是否已有正式出版版本。
- 将纯 arXiv 论文导出为规范的 `journal = {arXiv preprint arXiv:编号}`，同时保留匹配的 `eprint` 和 `archivePrefix = {arXiv}`；正式发表条目不输出这些 arXiv 字段。
- 只在 DOI 注册标题与输入标题一致时接受 DOI。
- 区分连续页码、eLocator、ACM 文章号和 PDF 内部页码。
- 核验会议论文的 `address`，不猜测会议地点。
- 对同一期刊或会议使用统一的规范名称。
- 将个人作者统一为 `Family, Given`，同时保持官方作者顺序不变。
- 删除冗余的 BibTeX 标题整体括号，同时保留大小写敏感词和 LaTeX 语法所需括号。
- 对所有条目类型按同一个确定性字段顺序输出适用字段。
- 默认生成两份修正后的 BibTeX（一份包含经核验的 DOI/URL，一份不含 DOI/URL），以及经核验的 CSV、高亮待复核条目的 XLSX 和必要的审计报告。

## 安装

### 让 Codex 安装

向 Codex 发送：

```text
请从下面的 GitHub 仓库安装 reference-verify skill：
https://github.com/pkunliu/reference-verify
```

当仓库为私有仓库时，安装者需要拥有该仓库的访问权限。

### 手动安装

```bash
git clone https://github.com/pkunliu/reference-verify.git ~/.codex/skills/reference-verify
```

安装后重新打开 Codex 或新建任务，使 skill 被重新发现。

## 使用方法

在 Codex 中使用 `$reference-verify` 调用。

### 核验整个 BibTeX 文件

```text
使用 $reference-verify 核对 references.bib。
保留所有原始标题和 citation key，核对正式出版版本、DOI、页码、会议地址和会议/期刊名称。
```

### 检查预印本的正式版本

```text
使用 $reference-verify 检查这些 arXiv 条目是否已经发表在正式期刊或会议中。
只有在标题身份精确匹配时才采用正式版本元数据。
```

### 统一期刊和会议名称

```text
使用 $reference-verify 检查这份 BibTeX 中同一期刊或会议的名称是否统一，
并为每篇会议论文核实 address。
```

### 同时生成两份 BibTeX

默认工作流输出 `*_with_doi_url.bib` 和 `*_without_doi_url.bib`。两份文件
除后一份完全省略 `doi` 与 `url` 字段外，其余内容保持一致。

## 核验原则

1. 不改写输入论文的标题。
2. 不从作者、主题或相邻页码推测 DOI。
3. 不把 PDF 本地页码当作正式论文集页码。
4. 正式版本标题发生实质变化时，只作为关联出版物报告，不生成混合引用。
5. 无法从官方来源确认的字段必须保持未解决，不猜测。

## 仓库结构

```text
reference-verify/
├── README.md
├── README.zh-CN.md
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── bibtex-output-normalization.md
│   └── source-and-doi-rules.md
└── scripts/
    └── csv_to_bibtex.py
```

`SKILL.md` 定义完整核验流程；`references/` 保存出版源、DOI、页码、会议地址及 BibTeX 规范化规则；`scripts/` 提供可重复的确定性转换工具。
