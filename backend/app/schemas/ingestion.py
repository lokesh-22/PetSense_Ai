from pydantic import BaseModel


class IngestResponse(BaseModel):
    status: str
    documents_indexed: int | None = None
    index_dir: str | None = None
    source: str | None = None
