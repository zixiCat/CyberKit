"""Validate report intake and generate self-contained HTML and editable Markdown.

Standard library only. Never interprets notes, executes input, or publishes.
"""
import argparse
import base64
import copy
import html
import json
import re
import sys
from pathlib import Path


def validate(data, base):
    if not isinstance(data, dict):
        raise ValueError('Report input must be an object')
    required = ('slug', 'title', 'author', 'audience', 'date', 'period', 'mode',
                'status', 'goal', 'conclusion', 'impact', 'decision')
    for key in required:
        if not isinstance(data.get(key), str) or not data[key].strip():
            raise ValueError(f'{key} must be a non-empty string')
    if not re.fullmatch(r'[a-z][a-z0-9]*(?:-[a-z0-9]+)*', data['slug']):
        raise ValueError('slug must use lowercase letters, numbers and single hyphens')
    if data['mode'] not in ('daily', 'extended'):
        raise ValueError('mode must be daily or extended')
    if data.get('language', 'en') not in ('en', 'zh'):
        raise ValueError('language must be en or zh')
    if data.get('imageLayout', 'pages') not in ('pages', 'long'):
        raise ValueError('imageLayout must be pages or long')
    for key in ('summary', 'commits'):
        if key in data and not isinstance(data[key], list):
            raise ValueError(f'{key} must be a list')
    commit_ids = set()
    for item in data.get('commits', []):
        if not isinstance(item, dict) or any(not isinstance(item.get(k), str) or not item[k].strip() for k in ('id', 'at', 'author', 'title', 'status')):
            raise ValueError('Each commit needs id, at, author, title and status')
        if item['id'] in commit_ids:
            raise ValueError('Commit IDs must be unique')
        commit_ids.add(item['id'])
    ids = set()
    for key in ('completed', 'validation', 'limitations', 'next', 'evidence', 'details'):
        if not isinstance(data.get(key), list):
            raise ValueError(f'{key} must be a list')
    for e in data['evidence']:
        if not isinstance(e, dict):
            raise ValueError('Each evidence item must be an object')
        for key in ('id', 'caption', 'observation', 'source', 'captured', 'limitation'):
            if not isinstance(e.get(key), str) or not e[key].strip():
                raise ValueError(f'evidence.{key} must be a non-empty string')
        if not re.fullmatch(r'E[1-9][0-9]*', e['id']) or e['id'] in ids:
            raise ValueError('Evidence IDs must be unique and follow E1, E2, ...')
        ids.add(e['id'])
        if e.get('image'):
            raw = e['image']
            if not isinstance(raw, str):
                raise ValueError('image must be a path or image data URI')
            if raw.startswith('data:'):
                if not re.fullmatch(r'data:image/(png|jpeg);base64,[A-Za-z0-9+/=\r\n]+', raw):
                    raise ValueError('Only PNG and JPEG data images are accepted')
                content = base64.b64decode(raw.split(',', 1)[1], validate=True)
                mime = raw.split(';', 1)[0][5:]
            else:
                path = (base / raw).resolve()
                if path.suffix.lower() not in ('.png', '.jpg', '.jpeg'):
                    raise ValueError('Only local PNG and JPEG screenshots are accepted')
                content = path.read_bytes()
                mime = 'image/png' if path.suffix.lower() == '.png' else 'image/jpeg'
            if len(content) > 5 * 1024 * 1024:
                raise ValueError('Each screenshot must be at most 5 MB')
            if not (content.startswith(b'\x89PNG\r\n\x1a\n') or content.startswith(b'\xff\xd8\xff')):
                raise ValueError('Image content is not PNG or JPEG')
            e['image'] = f'data:{mime};base64,' + base64.b64encode(content).decode('ascii')
    for key in ('summary', 'completed', 'validation'):
        for item in data.get(key, []):
            if not isinstance(item, dict):
                raise ValueError(f'Each {key} item must be an object')
            if not isinstance(item.get('text'), str) or not item['text'].strip():
                raise ValueError(f'{key}.text must be non-empty')
            if key == 'summary' and (not isinstance(item.get('label'), str) or not item['label'].strip()):
                raise ValueError('summary.label must be non-empty')
            refs = item.get('evidence_ids', [])
            if not isinstance(refs, list) or any(ref not in ids for ref in refs):
                raise ValueError(f'{key} contains an unknown evidence ID')
    if any(not isinstance(s, str) or not s.strip() for s in data['limitations']):
        raise ValueError('limitations must contain non-empty strings')
    for item in data['next']:
        if not isinstance(item, dict):
            raise ValueError('Each next action must be an object')
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in ('action','owner','due')):
            raise ValueError('Each next action needs action, owner and due')
    for item in data['details']:
        if not isinstance(item, dict):
            raise ValueError('Each detail must be an object')
        if any(not isinstance(item.get(k), str) or not item[k].strip() for k in ('title','text')):
            raise ValueError('Each detail needs title and text')
    translations = data.get('translations', {})
    if not isinstance(translations, dict):
        raise ValueError('translations must be an object')
    for lang, translation in translations.items():
        if lang not in ('en', 'zh') or not isinstance(translation, dict):
            raise ValueError('Translation languages must be en or zh')
        allowed = {'title','audience','period','status','goal','conclusion','impact','decision',
                   'summary','commits','completed','validation','limitations','next','evidence','details'}
        if set(translation) - allowed:
            raise ValueError('Translations may change prose only, not report identity or screenshots')
        for field in ('summary','commits','completed','validation','next','evidence','details'):
            if field in translation:
                if not isinstance(translation[field], list) or len(translation[field]) != len(data.get(field, [])) or any(not isinstance(i, dict) for i in translation[field]):
                    raise ValueError('Translation records must match the original report')
        for field in ('summary','completed','validation'):
            for original, translated in zip(data.get(field, []), translation.get(field, data.get(field, []))):
                if translated.get('evidence_ids', []) != original.get('evidence_ids', []):
                    raise ValueError('Translations must preserve evidence references')
        for original, translated in zip(data.get('commits', []), translation.get('commits', [])):
            if translated.get('id') != original['id'] or set(translated) - {'id', 'title', 'status'}:
                raise ValueError('Translated commits must preserve IDs, attribution and dates')
        for original, translated in zip(data['evidence'], translation.get('evidence', [])):
            if translated.get('id') != original['id'] or set(translated)-{'id','caption','observation','limitation'}:
                raise ValueError('Translated evidence must preserve IDs and original screenshot metadata')
        for original, translated in zip(data['next'], translation.get('next', data['next'])):
            if any(translated.get(k) != original[k] for k in ('owner','due')):
                raise ValueError('Translations must preserve owners and due dates')
        merged = localized(data, lang)
        merged.pop('translations', None)
        validate(merged, base)
    return data


def localized(data, lang):
    result = copy.deepcopy(data)
    for key, value in data.get('translations', {}).get(lang, {}).items():
        if key in ('evidence', 'commits'):
            result[key] = [{**original, **translated} for original, translated in zip(data.get(key, []), value)]
        else:
            result[key] = value
    result['language'] = lang
    return result


def markdown(data):
    def clean(s):
        return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    lines = [f"# {clean(data['title'])}", '',
             ' | '.join(clean(data[k]) for k in ('author','date','period','status')), '',
             f"Audience: {clean(data['audience'])}", '', '## At a glance', '']
    if data.get('summary'):
        lines += [clean(data['conclusion']), '', '| Topic | Summary |', '| --- | --- |']
        for item in data['summary']:
            lines += ['| ' + ' | '.join(clean(item[k]).replace('|', '\\|').replace('\n', ' ') for k in ('label', 'text')) + ' |']
        lines += ['']
    for k in (() if data.get('summary') else ('goal','conclusion','impact','decision')):
        lines += [f"**{k.capitalize()}:** {clean(data[k])}", '']
    for k, title in (('completed','What changed'),('validation','Checks')):
        lines += [f'## {title}', '']
        for item in data[k]:
            refs = ' '.join(f"[{ref}](#{ref.lower()})" for ref in item.get('evidence_ids', []))
            lines += [f"- {clean(item['text'])} {refs}".rstrip()]
        if not data[k]: lines += ['Not recorded.']
        lines += ['']
    if data.get('commits'):
        lines += ['## Changes & commits', '', '| Commit | Author | Time | Change | Status |', '| --- | --- | --- | --- | --- |']
        for item in data['commits']:
            lines += ['| ' + ' | '.join(clean(item[k]).replace('|', '\\|').replace('\n', ' ') for k in ('id', 'author', 'at', 'title', 'status')) + ' |']
        lines += ['']
    lines += ['## Still open','']
    lines += ['- ' + clean(s) for s in data['limitations']] or ['Not recorded.']
    lines += ['', '## Next steps', '', '| Action | Owner | Due |', '| --- | --- | --- |']
    for item in data['next']:
        lines += ['| ' + ' | '.join(clean(item[k]).replace('|', '\\|').replace('\n', ' ') for k in ('action','owner','due')) + ' |']
    lines += ['', '## Sources', '']
    for e in data['evidence']:
        lines += [f"<a id=\"{e['id'].lower()}\"></a>", f"### {e['id']} {clean(e['caption'])}", '',
                  clean(e['observation']), '', f"Source: {clean(e['source'])}. Captured: {clean(e['captured'])}.", '',
                  f"Limit: {clean(e['limitation'])}", '']
        if e.get('image'):
            lines += [f"![{clean(e['caption'])}](evidence/{e['id']}.{'png' if e['image'].startswith('data:image/png') else 'jpg'})", '']
    for item in data['details']:
        lines += [f"## {clean(item['title'])}", '', clean(item['text']), '']
    result = '\n'.join(lines)
    if data.get('language') == 'zh':
        for original, translated in {'At a glance':'一页看懂','What changed':'做了什么','Changes & commits':'提交与改动','Checks':'怎么验证','Still open':'还差什么','Next steps':'接下来','Sources':'依据与范围'}.items():
            result = result.replace('## '+original+'\n','## '+translated+'\n')
        for original, translated in {'Goal':'目标','Conclusion':'结论','Impact':'影响','Decision':'需要的决策'}.items():
            result = result.replace('**'+original+':**','**'+translated+':**')
        result = result.replace('Audience: ', '读者: ').replace('| Action | Owner | Due |','| 行动 | 负责人 | 截止日期 |').replace('Source: ','来源: ').replace('Captured: ','采集日期: ').replace('Limit: ','局限: ').replace('Not recorded.','尚未记录。')
        result = result.replace('| Topic | Summary |', '| 事项 | 摘要 |').replace('| Commit | Author | Time | Change | Status |', '| 提交 | 作者 | 时间 | 改动 | 状态 |')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--output-dir', required=True, type=Path)
    parser.add_argument('--replace', action='store_true')
    args = parser.parse_args()
    try:
        data = validate(json.loads(args.input.read_text(encoding='utf-8-sig')), args.input.parent)
        target = args.output_dir.resolve() / data['slug']
        if target.exists() and not args.replace:
            raise ValueError(f'Output exists: {target}; use a new slug or --replace')
        template = (Path(__file__).resolve().parent.parent / 'assets/report.html').read_text(encoding='utf-8')
        payload = json.dumps(data, ensure_ascii=False).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
        rendered = template.replace('REPORT_PAYLOAD', payload).replace('REPORT_TITLE', html.escape(data['title']))
        target.mkdir(parents=True, exist_ok=True)
        (target/'index.html').write_text(rendered, encoding='utf-8')
        (target/'report.md').write_text(markdown(data), encoding='utf-8')
        for lang in data.get('translations', {}):
            (target/f'report.{lang}.md').write_text(markdown(localized(data, lang)), encoding='utf-8')
        (target/'intake.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        for e in data['evidence']:
            if e.get('image'):
                folder = target/'evidence'
                folder.mkdir(exist_ok=True)
                ext = 'png' if e['image'].startswith('data:image/png') else 'jpg'
                (folder/f"{e['id']}.{ext}").write_bytes(base64.b64decode(e['image'].split(',',1)[1]))
        count = sum(len(str(v).split()) for v in (data['goal'], data['conclusion'], data['impact'], data['decision']))
        count += sum(len(i['text'].split()) for k in ('completed','validation') for i in data[k])
        if data['mode'] == 'daily' and (count > 300 or len(data['evidence']) > 1):
            print('Note: content may exceed one page; consider extended mode.', file=sys.stderr)
        print(json.dumps({'html': str(target/'index.html'), 'markdown': str(target/'report.md'), 'intake': str(target/'intake.json')}, ensure_ascii=False))
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f'Input error: {exc}\n')


if __name__ == '__main__':
    main()
