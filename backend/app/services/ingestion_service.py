from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pypdf import PdfReader

from app.core.config import settings
from app.data.breed_catalog import BREED_CATALOG, UNIVERSAL_ARTICLES
from app.utils.text import slugify


class IngestionService:
    def __init__(self) -> None:
        self.knowledge_base_dir = Path(settings.knowledge_base_dir)
        self.knowledge_base_dir.mkdir(parents=True, exist_ok=True)
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def ensure_seed_documents(self) -> None:
        seed_dir = self.knowledge_base_dir / "seed"
        seed_dir.mkdir(parents=True, exist_ok=True)

        for breed, data in BREED_CATALOG.items():
            breed_slug = slugify(breed)
            breed_dir = seed_dir / breed_slug
            breed_dir.mkdir(parents=True, exist_ok=True)
            for index, article in enumerate(data["articles"], start=1):
                path = breed_dir / f"{index:02d}-{slugify(article['title'])}.md"
                content = (
                    f"---\n"
                    f"breed: {breed}\n"
                    f"species: {data['species']}\n"
                    f"source: {article['source']}\n"
                    f"title: {article['title']}\n"
                    f"topic: {article['topic']}\n"
                    f"---\n\n"
                    f"{article['content']}\n"
                )
                if not path.exists():
                    path.write_text(content, encoding="utf-8")

        universal_dir = seed_dir / "universal"
        universal_dir.mkdir(parents=True, exist_ok=True)
        for index, article in enumerate(UNIVERSAL_ARTICLES, start=1):
            path = universal_dir / f"{index:02d}-{slugify(article['title'])}.md"
            content = (
                f"---\n"
                f"breed: universal\n"
                f"species: all\n"
                f"source: {article['source']}\n"
                f"title: {article['title']}\n"
                f"topic: {article['topic']}\n"
                f"---\n\n"
                f"{article['content']}\n"
            )
            if not path.exists():
                path.write_text(content, encoding="utf-8")

    def load_documents(self) -> list[Document]:
        documents: list[Document] = []
        for path in sorted(self.knowledge_base_dir.rglob("*")):
            if path.suffix.lower() not in {".txt", ".md", ".pdf"} or not path.is_file():
                continue
            raw_text = self._read_text(path)
            metadata = self._extract_metadata(path, raw_text)
            content = metadata.pop("_body")
            documents.append(Document(page_content=content, metadata=metadata))
        return documents

    def split_documents(self, documents: list[Document]) -> list[Document]:
        split_docs = self.splitter.split_documents(documents)
        for index, document in enumerate(split_docs, start=1):
            document.metadata["chunk_id"] = f"{document.metadata['source_path']}::chunk-{index}"
        return split_docs

    def ingestable_documents(self) -> list[Document]:
        self.ensure_seed_documents()
        documents = self.load_documents()
        return self.split_documents(documents)

    @staticmethod
    def _read_text(path: Path) -> str:
        if path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        return path.read_text(encoding="utf-8")

    def _extract_metadata(self, path: Path, raw_text: str) -> dict:
        metadata = {
            "breed": "universal",
            "species": "all",
            "source": path.name,
            "title": path.stem,
            "topic": "general",
            "source_path": path.relative_to(self.knowledge_base_dir).as_posix(),
        }

        body = raw_text
        if raw_text.startswith("---\n"):
            _, frontmatter, remainder = raw_text.split("---\n", 2)
            for line in frontmatter.splitlines():
                if ":" not in line:
                    continue
                key, value = line.split(":", 1)
                metadata[key.strip()] = value.strip()
            body = remainder.strip()

        metadata["breed"] = slugify(metadata.get("breed", "universal"))
        metadata["_body"] = body
        return metadata


ingestion_service = IngestionService()
