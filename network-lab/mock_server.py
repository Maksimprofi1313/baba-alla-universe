"""Local-only mock HTTP endpoint for development and testing."""
from flask import Flask, jsonify, Response, request

app = Flask(__name__)

@app.route("/generate_204", methods=["GET", "HEAD", "POST"])
def generate_204():
    # Do not log request headers: they may contain cookies or other private data.
    return Response(status=204, headers={"Connection": "close"})

@app.route("/", defaults={"path": ""}, methods=["GET", "POST", "PUT", "DELETE"])
@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):
    # Log only method and path; never dump headers or request bodies.
    app.logger.info("Mock request: method=%s path=/%s", request.method, path)
    return jsonify({"status": "ok", "path": path})

if __name__ == "__main__":
    print("Local mock server: http://127.0.0.1:5000")
    print("Accessible only from this computer.")
    app.run(host="127.0.0.1", port=5000, debug=False)
