from data.db import engine, Base
import data.models  # noqa: F401
from presentation.api import app

@app.on_event("startup")
def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

if __name__ == "__main__":
    init_db()

from presentation.api import app
