# Report languages

English is the first-use default. Set `language` to `en` or `zh` for the canonical body. Add a `translations` object for the alternate language. Translate complete sentences from the same verified facts; never add results while translating.

A translation may contain `title`, `audience`, `period`, `status`, `goal`, `conclusion`, `impact`, `decision`, `summary`, `commits`, `completed`, `validation`, `limitations`, `next`, `evidence`, and `details`. For a complete bilingual report, include the prose fields present in the source. The original `author`, `date`, `slug`, and `mode` are retained.

Lists keep the same length and order as the canonical report. Completed and validation records retain their `evidence_ids`. Next actions retain their `owner` and `due` values. Translated evidence records contain only `id`, `caption`, `observation`, and `limitation`; the generator retains the original `source`, `captured`, and `image`. Do not copy image data into translation objects.

Summary rows translate `label` and `text` while preserving `evidence_ids`. Commit translations contain `id`, `title` and `status` only; preserve each original ID and order. The generator retains the author and timestamp. A summary should remain compact in both languages; do not shorten it by dropping a limitation or changing a result.

```json
{
  "language": "en",
  "translations": {
    "zh": {
      "title": "报告标题",
      "completed": [{"text": "已核实的完成结果", "evidence_ids": ["E1"]}],
      "next": [{"action": "下一步行动", "owner": "zixiCat", "due": "To confirm"}],
      "evidence": [{"id": "E1", "caption": "图注", "observation": "可见观察", "limitation": "证明范围的局限"}]
    }
  }
}
```

This fragment illustrates the translation shape; supply the complete canonical intake before running the generator. Recheck bilingual names, numbers, conditions, and claims. The browser selector translates labels and selects supplied prose; it does not use machine translation. Browser edits invalidate the other translation, so regenerate it before publishing revised bilingual content.
