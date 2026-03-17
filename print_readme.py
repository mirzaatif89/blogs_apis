from pathlib import Path
path = Path('README.md')
data = path.read_text().splitlines()
start = 35
for i,line in enumerate(data[start-1:], start=start):
    print(f'{i:04d}: {line}')
