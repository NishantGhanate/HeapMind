Here's a quick summary the project:
## 🧠 **Building an LLM-powered flashcard/quiz app**:

#### ✅ **Ingestion Flow**

* Users upload documents (PDFs, DOCX, etc.).
* It save file metadata in a database and file on file-system.
* Use the **Outbox Pattern** with **Celery + RabbitMQ** to decouple and asynchronously process uploaded documents.

#### ✅ **Processing Flow**

* A background worker:
  * Parses the document (extracts text).
  * Converts content to embeddings (using an LLM + embedding model).
  * Stores embeddings into **Qdrant** (for vector search).

#### ✅ **Query Flow**

* A user asks a question or “generate 10 quiz questions from this doc”.
* server:
  * Perform semantic search in Qdrant to retrieve relevant chunks.
  * Feed them into an LLM (like phi3) with a prompt to **generate quiz questions**.
  * Returns list of json data.
  * Validate the data & store in Postgres.
  * Query postgres to the data based on sm2.
  * Using api generate flashcards/quiz content.

---

### 🧩 Stack Summary

| Component      | Tech Used                             |
| -------------- | ------------------------------------- |
| Backend API    | FastAPI                               |
| Async Worker   | Celery + RabbitMQ (or Outbox Pattern) |
| Storage        | PostgreSQL + SQLModel                 |
| Vector DB      | Qdrant                                |
| Message Broker | RabbitMQ                              |
| Result Backend | Redis (for Celery)                    |
| Embeddings     | (all-MiniLM-L6-v2,)                   |
| Quiz Generator | LLM (phi3)                            |

---

### [Click here Setup Guide ](https://github.com/NishantGhanate/HeapMind/tree/main/documentation/setup.md)

