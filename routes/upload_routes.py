import os
from flask import Blueprint, request, jsonify

from services.pdf_loader import extract_text
from services.text_chunker import chunk_text
from services.embeddings import generate_embeddings
from services.vector_store import store_chunks

# Blueprint
upload_bp = Blueprint("upload", __name__)

UPLOAD_FOLDER = "temp_uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload_bp.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files allowed"}), 400

    # Save PDF temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    try:
        # 1. Extract text
        text = extract_text(file_path)

        # 2. Chunk text
        chunks = chunk_text(text)

        # 3. Generate embeddings
        embeddings = generate_embeddings(chunks)

        # 4. Store in vector DB
        store_chunks(chunks, embeddings)

        return jsonify({
            "message": "PDF uploaded and processed successfully",
            "chunks": len(chunks)
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        # Cleanup uploaded file
        if os.path.exists(file_path):
            os.remove(file_path)
