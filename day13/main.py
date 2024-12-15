from __future__ import annotations

import re
from pathlib import Path

fname: Path = Path(__file__).parent / "example.txt"
with open(fname) as fid:
    lines: list[str] = fid.readlines()
lines: list[tuple[str, str, str]] = list(zip(lines[::4], lines[1::4], lines[2::4]))
data: list[dict[str, tuple[int, int]]] = []
pattern = re.compile(r"(\d+)")
for line in lines:
    data_ = dict()
    for elt, line_ in zip(("A", "B", "Prize"), line, strict=True):
        x, y = re.findall(pattern, line_)
        data_[elt] = (int(x), int(y))
    data.append(data_)
