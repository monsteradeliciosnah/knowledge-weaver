import json

import typer

from .indexer import MultiModalIndexer

app = typer.Typer(help="Knowledge Weaver CLI")


@app.command()
def build(data: str = "data", index_dir: str = "index"):
    idx = MultiModalIndexer(index_dir=index_dir)
    idx.build(data)
    typer.echo(f"Indexed {data} -> {index_dir}")


@app.command()
def search(query: str, k: int = 5, index_dir: str = "index"):
    idx = MultiModalIndexer(index_dir=index_dir)
    res = idx.search(query, k)
    typer.echo(json.dumps(res, indent=2))


if __name__ == "__main__":
    app()
