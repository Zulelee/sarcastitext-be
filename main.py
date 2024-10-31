import uvicorn
from os import getenv

if __name__ == "main":
    port = int(getenv("PORT", 8000))
    uvicorn.run("app.api:app", host="0.0.0.0", port=port, reload=True)