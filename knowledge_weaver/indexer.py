from __future__ import annotations
from typing import List, Dict, Any, Tuple
from pathlib import Path
import json, os
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer, util
from PIL import Image
from .ingest import read_text, read_image, read_csv, chunk_text, collect_files, sha1

class MultiModalIndexer:
    def __init__(self, index_dir="index", text_model="all-MiniLM-L6-v2", image_model="clip-ViT-B-32"):
        self.index_dir=index_dir
        Path(index_dir).mkdir(parents=True, exist_ok=True)
        self.text_model=SentenceTransformer(text_model)
        self.image_model=SentenceTransformer(image_model)

    def _faiss(self, dim: int):
        idx = faiss.IndexFlatIP(dim)
        faiss.normalize_L2 = faiss.normalize_L2
        return idx

    def build(self, data_dir: str):
        files=collect_files(data_dir)
        text_vecs=[]; text_meta=[]; img_vecs=[]; img_meta=[]
        for f in files:
            if f.suffix.lower() in [".txt",".md",".pdf",".csv"]:
                if f.suffix.lower()==".csv":
                    txt = read_csv(f)
                else:
                    txt = read_text(f)
                for chunk in chunk_text(txt):
                    emb = self.text_model.encode(chunk, convert_to_numpy=True, normalize_embeddings=True)
                    text_vecs.append(emb)
                    text_meta.append({"type":"text","path":str(f),"chunk":chunk[:2000]})
            elif f.suffix.lower() in [".png",".jpg",".jpeg"]:
                img = read_image(f)
                emb = self.image_model.encode(img, convert_to_numpy=True, normalize_embeddings=True)
                img_vecs.append(emb)
                img_meta.append({"type":"image","path":str(f)})
        if text_vecs:
            tv=np.vstack(text_vecs).astype("float32")
            idx_t=self._faiss(tv.shape[1]); idx_t.add(tv)
            faiss.write_index(idx_t, os.path.join(self.index_dir,"text.faiss"))
            with open(os.path.join(self.index_dir,"text_meta.json"),"w") as f: json.dump(text_meta,f)
        if img_vecs:
            iv=np.vstack(img_vecs).astype("float32")
            idx_i=self._faiss(iv.shape[1]); idx_i.add(iv)
            faiss.write_index(idx_i, os.path.join(self.index_dir,"image.faiss"))
            with open(os.path.join(self.index_dir,"image_meta.json"),"w") as f: json.dump(img_meta,f)

    def search(self, query: str, k:int=5)->List[Dict[str,Any]]:
        out=[]
        tpath=os.path.join(self.index_dir,"text.faiss")
        if os.path.exists(tpath):
            idx=faiss.read_index(tpath)
            meta=json.load(open(os.path.join(self.index_dir,"text_meta.json")))
            q=self.text_model.encode(query, convert_to_numpy=True, normalize_embeddings=True).astype("float32")
            D,I = idx.search(q.reshape(1,-1), k)
            for d,i in zip(D[0], I[0]):
                if i==-1: continue
                out.append({"score": float(d), **meta[i]})
        ipath=os.path.join(self.index_dir,"image.faiss")
        if os.path.exists(ipath):
            idx=faiss.read_index(ipath)
            meta=json.load(open(os.path.join(self.index_dir,"image_meta.json")))
            q=self.image_model.encode(query, convert_to_numpy=True, normalize_embeddings=True).astype("float32")
            D,I = idx.search(q.reshape(1,-1), k)
            for d,i in zip(D[0], I[0]):
                if i==-1: continue
                out.append({"score": float(d), **meta[i]})
        out.sort(key=lambda x: x["score"], reverse=True)
        return out[:k]
