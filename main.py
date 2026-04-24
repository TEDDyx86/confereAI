from execution.fastapi_server import app
import uvicorn
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    # No Railway, o host deve ser 0.0.0.0
    uvicorn.run(app, host="0.0.0.0", port=port)
