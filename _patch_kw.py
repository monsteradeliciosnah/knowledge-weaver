import re
from pathlib import Path

# Fix E741 in indexer.py (rename D/I -> distances/indices)
p = Path("knowledge_weaver/indexer.py")
s = p.read_text()
s = re.sub(r"\bD,\s*I\b", "distances, indices", s)
s = re.sub(r"\bD\[", "distances[", s)
s = re.sub(r"\bI\[", "indices[", s)
s = re.sub(
    r"zip\(\s*D\[\s*0\s*\]\s*,\s*I\[\s*0\s*\]\s*\)", "zip(distances[0], indices[0])", s
)
p.write_text(s)

# Fix F841 in ingest.py (remove unused MarkdownIt() assignment, if present)
p2 = Path("knowledge_weaver/ingest.py")
s2 = p2.read_text()
s2_new = re.sub(r"(?m)^\s*md\s*=\s*MarkdownIt\(\)\s*\n", "", s2)
if s2_new != s2:
    p2.write_text(s2_new)
