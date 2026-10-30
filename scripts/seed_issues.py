"""Preview (default) or create challenge issues using an authenticated GitHub CLI."""
import argparse
import json
from pathlib import Path
import re
import subprocess
ROOT = Path(__file__).resolve().parents[1]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--repo', required=True)
    parser.add_argument('--apply', action='store_true')
    args=parser.parse_args()
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', args.repo):
        parser.error('expected OWNER/REPO')
    cards=sorted((ROOT/'challenges').glob('[0-9][0-9].md'))
    existing=set()
    if args.apply:
        result=subprocess.run(['gh','api',f'repos/{args.repo}/issues?state=all&per_page=100','--paginate','--slurp'],check=True,capture_output=True,text=True)
        existing={issue['title'] for page in json.loads(result.stdout) for issue in page if 'pull_request' not in issue}
    for path in cards:
        title='[Challenge] '+path.read_text().splitlines()[0].removeprefix('# ')
        if title in existing:
            print('Exists:',title)
        elif args.apply:
            subprocess.run(['gh','issue','create','--repo',args.repo,'--title',title,'--body-file',str(path)],check=True)
        else:
            print('Would create:',title)
if __name__=='__main__':
    main()
