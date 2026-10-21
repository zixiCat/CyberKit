"""Rasterize verified browser page exports into phone-readable PNGs and ZIPs.

Input PDFs are pagination intermediates, not the sharing deliverable.
"""
import argparse
import json
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--intake',required=True,type=Path)
    p.add_argument('--output-dir',required=True,type=Path)
    p.add_argument('--poppler-dir',required=True,type=Path)
    p.add_argument('--input-en',type=Path)
    p.add_argument('--input-zh',type=Path)
    args=p.parse_args()
    d=json.loads(args.intake.read_text(encoding='utf-8-sig'))
    target=args.output_dir.resolve()/d['slug']
    target.mkdir(parents=True,exist_ok=True)
    tool=args.poppler_dir/('pdftoppm.exe' if (args.poppler_dir/'pdftoppm.exe').exists() else 'pdftoppm')
    images={}
    for lang,path in [('en',args.input_en),('zh',args.input_zh)]:
        if path is None: continue
        with tempfile.TemporaryDirectory() as temp:
            prefix=Path(temp)/'page'
            subprocess.run([str(tool),'-r','300','-png',str(path.resolve()),str(prefix)],check=True)
            pages=sorted(Path(temp).glob('page-*.png'),key=lambda x:int(x.stem.rsplit('-',1)[1]))
            if not pages: raise RuntimeError(f'No rendered pages for {lang}')
            names=[]
            for i,page in enumerate(pages,1):
                name=f'report.{lang}-{i}.png'
                shutil.copyfile(page,target/name)
                names.append(name)
            with zipfile.ZipFile(target/f'report.{lang}.images.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
                for name in names:z.write(target/name,name)
            images[lang]=names
    if not images: p.error('Supply at least one language page export')
    d['images']=images
    args.intake.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'slug':d['slug'],'images':images,'output':str(target)},ensure_ascii=False))


if __name__=='__main__':main()
