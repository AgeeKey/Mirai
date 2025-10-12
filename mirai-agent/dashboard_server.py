"""
🤖 KAIZEN CI/CD Monitoring Dashboard API
Flask backend for real-time CI/CD metrics visualization
"""

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from core.cicd_monitor import CICDMonitor

app = Flask(__name__, template_folder="../web/templates", static_folder="../web/static")
CORS(app)

# Load GitHub config
config_path = Path(__file__).parent / "configs" / "api_keys.json"
with open(config_path) as f:
    config = json.load(f)

monitor = CICDMonitor(
    github_token=config["GITHUB_TOKEN"],
    repo_owner="AgeeKey",
    repo_name="mirai-showcase",
)


@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("dashboard.html")


@app.route("/api/health")
def health():
    """Get CI/CD health status"""
    try:
        health_data = monitor.check_health()
        return jsonify({"success": True, "data": health_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/metrics")
def metrics():
    """Get detailed CI/CD metrics"""
    try:
        metrics_data = monitor.get_workflow_metrics()
        return jsonify({"success": True, "data": metrics_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/runs")
def runs():
    """Get recent workflow runs"""
    try:
        runs_data = monitor.get_workflow_runs(limit=20)
        return jsonify({"success": True, "data": runs_data})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/failures")
def failures():
    """Get failing workflows"""
    try:
        failing = monitor.get_failing_workflows()
        return jsonify({"success": True, "data": failing})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/report")
def report():
    """Get full text report"""
    try:
        report_text = monitor.generate_report()
        return jsonify(
            {
                "success": True,
                "data": {
                    "report": report_text,
                    "timestamp": monitor.check_health()["timestamp"],
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print(
        """
╔══════════════════════════════════════════════════════════════════════╗
║  🤖 KAIZEN CI/CD Monitoring Dashboard                               ║
╚══════════════════════════════════════════════════════════════════════╝

🚀 Starting dashboard server...

📊 Available endpoints:
   • http://localhost:5000/           - Main dashboard
   • http://localhost:5000/api/health - Health check
   • http://localhost:5000/api/metrics - Metrics data
   • http://localhost:5000/api/runs   - Recent runs
   • http://localhost:5000/api/failures - Failing workflows
   • http://localhost:5000/api/report - Full report

🌸 МИРАЙ's choice: Web dashboard for real-time visualization
🤖 КАЙДЗЕН: Dashboard starting on port 5000...

"""
    )
    app.run(host="0.0.0.0", port=5000, debug=True)
