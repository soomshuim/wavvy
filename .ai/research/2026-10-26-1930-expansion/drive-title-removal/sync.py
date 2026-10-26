from pathlib import Path
import shutil
s=Path('/Users/zenkim_office/.aside/u/0/sessions/2026-10-26_7uXQ12UCOTUChKQm/artifacts/1930-drive-title-removal');d=Path('.ai/research/2026-10-26-1930-expansion/drive-title-removal/raw');d.mkdir(exist_ok=True)
for p in s.glob('*'):shutil.copy2(p,d/p.name)
Path('SERIES/19-30/production/suno-drive-title-removal-20261026.json').write_text((d/'journal.json').read_text());print('host rename journal synchronized')
