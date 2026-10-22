---
name: personal-work-report
description: Draft zixiCat daily and task completion reports from verified notes and evidence, with optional private Sites publication. Bare invocation checks local setup and readiness without drafting or publishing.
---

# Personal work report

Create a reviewable report in one pass from the user's notes, current task results, and authorized local evidence. Use English unless the user explicitly requests Chinese or has established a report-language preference. The default audience is product users and leaders: emphasize what changed and why it matters to them. A product or branch update describes the product's changes, not the report author's personal work. Put implementation, experiments, and full history in supporting details.

## Writing and visual style

Use a plain, direct style: short headings, concrete changes and observed results. Lead with **At a glance / 一页看懂**: a compact two-column summary that answers what changed, what the user sees, what was checked and what remains. Put technical details and the full history below it. Prefer headings such as **What changed / 做了什么**, **Changes & commits / 提交与改动**, **Checks / 怎么验证** and **Still open / 还差什么** over abstract process language. Do not add cost, speed, savings or deployment claims without evidence.

Use the template's optional `summary` rows (`label`, `text`, `evidence_ids`) for the first-page summary. Give each distinct feature or meaningful fix a short label and one concise sentence describing the user-visible change. "Show more features" means broader coverage of verified changes, not longer paragraphs, repeated explanations, or an arbitrary feature count. Keep commit hashes, merge counts, build internals, and detailed test logs in supporting details unless they affect a reader's decision; summarize operational changes briefly when relevant. Include only material verification limits or actions in the overview. Keep **At a glance / 一页看懂** and **What changed / 做了什么** at 22 CSS px across desktop, narrow layouts, print, and image export unless the user requests otherwise.

For repository reviews, optional `commits` records contain `id`, `at`, `author`, `title` and `status`; keep original attribution, distinguish merges from implementation changes, and identify work that is only on another branch. Preserve a complete manifest separately when useful, rather than turning the main update into a commit dump. Use a restrained paper-like layout, a small section index and thin row separators; avoid oversized cards or repeated overview prose. Language follows the user's request; a Chinese reference may establish a Chinese preference for that report without changing unrelated reports.

Bare `$personal-work-report` or an explicit setup/readiness request means a setup/readiness check, not a request to invent a report: resolve runtime dependencies through `load_workspace_dependencies`, verify the bundled template/helpers exist, and create the missing local `Codex\WorkReports` folder under the current user's Windows Documents known folder. Preserve existing files. Check the installed Browser capability for visual QA and Sites capability/account only when available; report optional publication access separately. Use [hosting discovery](references/hosting.md) to identify the existing WorkReport hub without publishing. Do not create a schedule, Site, draft, or deployment during bare setup. Explicit report requests retain the workflow below and use the requested project/output location.

English is the default report and UI language on first use. For bilingual output, read [references/languages.md](references/languages.md), keep canonical prose in `language: en`, and add reviewed Chinese prose under `translations.zh` (or reverse for an explicitly Chinese source). Translate prose only; preserve proper names, metrics, evidence IDs, images, source paths, capture timestamps, action owners and due dates. The UI selector remembers an explicit choice on that browser. Missing translations display the original body with a notice. Browser edits invalidate the other language so an outdated translation cannot silently remain beside changed facts; regenerate the translation before publishing a bilingual revision. Check both languages at mobile width and in print, including long text.

## Gather and draft

Read the relevant task files before making claims. Separate completed work from proposed actions. Preserve uncertainties. Never infer that a test passed, a change shipped, or a metric improved from implementation alone. Ask only for missing information essential to a claim or requested action; use explicit unknowns for other gaps.

For a branch-wide daily update, inspect the requested branch across all authors; do not limit it to this chat's work or one author's commits. Use the reporting timezone and distinguish when a change was developed from when it was merged into the branch or deployed. Do not advertise yesterday's features as today's additions merely because today's merge brought them in. Keep earlier work as labeled history only when useful, deduplicate equivalent patches, and report new behavior separately from merge/sync records. State the scope briefly in supporting details when these dates differ.

Use [references/intake.json](references/intake.json) as the input shape. Keep the intake lightweight: subject, reporting date or period, goal, conclusion, impact, decision needed, completed items, validation, blockers, and next actions with owner and date. A few rough notes are sufficient; Codex should convert them into the structured input. Do not require the user to edit JSON.

Give each evidence item an ID, caption, actual observation, source, capture date, and limitation. Reference IDs from completed items and validation. Local PNG/JPEG screenshots can be embedded with an `image` path relative to the input file. Redact sensitive content before publication. Generated illustrations must be labeled as illustrations and must never substantiate an outcome. Use ImageGen only when it adds explanatory value, and its skill when used. The workflow diagram included in the template describes drafting; it is not validation evidence for the user's work.

### Images for an existing website or app

Treat "generate images of the website or report" as a capture and render request. Distinguish these outputs:

- UI evidence screenshots are genuine captures chosen to demonstrate completed behavior or a meaningful change. Avoid repeated empty or decorative captures that add no new finding. Caption the source URL or file, app state, capture date, observed claim and limitation; preserve the privacy checks above. Use before and after screenshots only when both real captures exist.
- Sharing images are PNG pages rendered from the actual report website, with relevant supporting details expanded. They may contain the verified UI captures, but are report-page renders rather than new screenshots of the product.
- Original illustrations are optional when explicitly requested. Label them as non-evidence and keep them separate from actual UI captures. Do not substitute imagined architecture artwork for an existing-site capture, and keep unused or withdrawn artwork out of final hosted and downloadable reports.

For example, "report on the website we just built and generate images to share" calls for actual UI captures and rendered report PNGs. An explicit request to add an original illustration can use ImageGen under the existing illustration rules.

## Generate and review

Resolve the bundled Python runtime through `load_workspace_dependencies`, then execute:

```text
<bundled-python> <this-skill>/scripts/generate_report.py --input <absolute-intake.json> --output-dir <absolute-reports-directory>
```

This produces `<slug>/index.html`, `report.md`, and `intake.json`. Existing output requires `--replace`; do not use it for an unrelated report. The HTML is self contained and editable in the browser. Markdown and JSON remain editable sources. A new revision should have a new slug when the old URL should remain stable.

Inspect the HTML at desktop and narrow widths, exercise expand, edit, download, and print behavior, and verify claims against the input. Daily mode targets one A4 page for about 300 words and one small screenshot; long content should switch to extended mode rather than be clipped. Browser edits and downloads are local and do not update a hosted report.

Provide high-resolution PNG report images as the offline sharing format, alongside the web URL and editable HTML/JSON. PDF is not the user's preferred offline deliverable. For small daily reports, render one readable page; for larger reports, use separate page images. Use the supported browser on the actual report with `?export=images`, select the language, and open supporting details. This export profile uses 112 mm wide pages with 12 pt body text, so text remains readable when fitted to a phone; it does not reuse a scaled-down desktop canvas. The documented CDP `Page.printToPDF` may be used solely as an intermediate pagination step with `preferCSSPageSize: true` and `printBackground: true`; render those pages at 300 DPI using bundled Poppler. Inspect every final PNG for clipping, readable text, missing glyphs, image quality, and caption placement. Collapsible sections become expanded content in the images; editing and link-copy controls are omitted. Never use ImageGen to render report text or fabricate evidence.

When the user requests **one long image**, set `imageLayout: long`, use the actual report's `?export=images` view at about 112 mm CSS width, and capture the whole report into one continuous PNG. Use the supported browser screenshot/CDP capability with sufficient output scale for readable text; do not shrink a wide desktop capture to phone width or substitute a ZIP of pages. Inspect the full image, including its bottom edge. A long image is still recorded as one entry such as `report.zh-1.png` in `images`; its height is not a paper page limit. Reset temporary browser viewport changes after capture.

Keep images beside the HTML as `report.en-1.png`, `report.zh-1.png`, and further numbered pages. Package a multi-page language into `report.en.images.zip` or `report.zh.images.zip` using Python's standard-library zipfile. Only after verified export, set `images` in the intake to `{ "en": ["report.en-1.png"], "zh": ["report.zh-1.png"] }` with all actual page filenames, then regenerate HTML. Stage those assets alongside the hosted report. The download button selects the current language, returning a PNG for one page or a ZIP for multiple pages. Browser edits invalidate export links; re-render images before publishing revisions. Optional `workflow: true` adds the drafting workflow illustration to the supporting appendix; use it only for reports about this workflow.

## Optional hosting and scheduling

For a requested URL, use the installed Sites skill and native tools. In the WorkReport project, reuse `site/.openai/hosting.json`; stage only the intended report HTML under `site/dist/reports/<slug>/index.html`, update the hub, and publish privately. Never upload raw input, source repositories, confidential references, or unrelated drafts. Across projects, use the user's designated Site or create a private Site with the Sites workflow. Report the per-report URL and its actual audience. Changing viewer access may invite people; obtain the intended audience and authorization before doing that. Do not message recipients.

For WorkReport updates or the observed Windows Bash packaging failure, read [references/hosting.md](references/hosting.md). Stage verified image pages and ZIPs with the report HTML. Reuse the published report routes; these are stable Site URLs, not temporary asset links.

For requested recurring drafting, use the supported automation tool only after the schedule, timezone, and authorized evidence source are clear. Automations should create drafts for review, stay quiet when nothing actionable changed, and never distribute reports automatically. An on-demand generation command is not a scheduled automation.

## Example invocation

`Use $personal-work-report to draft today's report from this task. Keep it to one page, include the verified screenshot, and give me a private Sites URL.`
