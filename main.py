from execution.fastapi_server import app
import uvicorn
import os

if __name__ == "__main__":
    # Hugging Face Spaces usa a porta 7860 por padrão
    port = int(os.environ.get("PORT", 7860))
    uvicorn.run(app, host="0.0.0.0", port=port)
