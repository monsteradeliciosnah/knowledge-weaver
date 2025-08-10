from __future__ import annotations
import os, io, hashlib
from pathlib import Path
from typing import List, Dict, Any, Tuple
import pandas as pd
from PIL import Image
from markdown_it import MarkdownIt
from pdfminer.high_level import extract_text

def read_text(path: Path) -> str:
    if path.suffix.lower() in [".md",".markdown"]:
        md=MarkdownIt()
        return path.read_text(encoding="utf-8")
    elif path.suffix.lower() in [".txt"]:
        return path.read_text(encoding="utf-8")
    elif path.suffix.lower() in [".pdf"]:
        return extract_text(str(path))
    else:
        return path.read_text(encoding="utf-8", errors="ignore")

def read_image(path: Path) -> Image.Image:
    return Image.open(path).convert("RGB")

def read_csv(path: Path) -> str:
    df=pd.read_csv(path)
    return df.to_csv(index=False)

def chunk_text(text: str, chunk_size:int=800, overlap:int=120)->List[str]:
    chunks=[]
    i=0
    n=len(text)
    while i<n:
        chunks.append(text[i:i+chunk_size])
        i+= max(1, chunk_size-overlap)
    return chunks

def collect_files(root: str)->List[Path]:
    p=Path(root)
    files=[]
    for ext in ["*.txt","*.md","*.pdf","*.png","*.jpg","*.jpeg","*.csv"]:
        files.extend(p.rglob(ext))
    return files

def sha1(s: str)->str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()
