from flask import Flask, request, jsonify

from rag import ask_question


app = Flask(__name__)


# --------------------------------------------------
# Home
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "message": "College RAG API is running"
    })


# --------------------------------------------------
# Health check
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():

    return jsonify({
        "status": "healthy"
    })


# --------------------------------------------------
# Ask question
# --------------------------------------------------

@app.route("/ask", methods=["POST"])
def ask():

    try:

        data = request.get_json()

        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({
                "error": "Question is required"
            }), 400


        result = ask_question(
            question
        )


        return jsonify(result)


    except Exception as e:

        return jsonify({
            "error": str(e)
        }), 500


# --------------------------------------------------
# Run server
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )