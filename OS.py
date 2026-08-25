from flask import Flask, request, jsonify
import subprocess
import ipaddress

app = Flask(__name__)

@app.route('/ping')
def ping_host():
    # Get the IP from query parameters
    user_input = request.args.get('ip', '')

    # Validate IP address format
    try:
        ip_obj = ipaddress.ip_address(user_input)
    except ValueError:
        return jsonify({"error": "Invalid IP address"}), 400

    try:
        # Run ping safely without invoking the shell
        result = subprocess.run(
            ["ping", "-c", "1", str(ip_obj)],  # Command as list, no shell
            capture_output=True,
            text=True,
            timeout=5
        )
        return jsonify({
            "status": "success" if result.returncode == 0 else "failed",
            "output": result.stdout.strip()
        })
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Ping timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run Flask app (debug=False for security in production)
    app.run(host="0.0.0.0", port=5000, debug=False)
