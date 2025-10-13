"""
🤖 KAIZEN CI/CD Monitoring Dashboard API
Flask backend for real-time CI/CD metrics visualization
"""

from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import json
from pathlib import Path
from core.cicd_monitor import CICDMonitor
from core.nasa_level.orchestrator import NASALearningOrchestrator

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

# Initialize NASA-Level Learning System
nasa_learning = NASALearningOrchestrator()


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


# ============================================================================
# 🚀 NASA-LEVEL LEARNING SYSTEM ENDPOINTS
# ============================================================================


@app.route("/api/nasa/status")
def nasa_status():
    """Get NASA learning system status"""
    try:
        status = nasa_learning.get_status()
        return jsonify({"success": True, "data": status})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/metrics")
def nasa_metrics():
    """Get NASA learning metrics"""
    try:
        status = nasa_learning.get_status()
        metrics = status.get("metrics", {})
        return jsonify({"success": True, "data": metrics})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/knowledge")
def nasa_knowledge():
    """Get all learned technologies from knowledge base"""
    try:
        technologies = nasa_learning.get_learned_technologies()
        return jsonify({"success": True, "data": technologies})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/knowledge/<technology>")
def nasa_knowledge_detail(technology):
    """Get detailed knowledge about specific technology"""
    try:
        knowledge = nasa_learning.knowledge_manager.get_knowledge(technology)
        if knowledge:
            return jsonify({"success": True, "data": knowledge})
        else:
            return jsonify({"success": False, "error": "Technology not found"}), 404
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/search/<query>")
def nasa_search(query):
    """Search in NASA knowledge base"""
    try:
        results = nasa_learning.search_knowledge(query)
        return jsonify({"success": True, "data": results})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/report")
def nasa_report():
    """Get comprehensive NASA learning report"""
    try:
        report = nasa_learning.generate_report()
        return jsonify({"success": True, "data": {"report": report}})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/prometheus")
def nasa_prometheus():
    """Get Prometheus metrics in text format"""
    try:
        metrics_text = nasa_learning.metrics.export_prometheus()
        from flask import Response

        return Response(metrics_text, mimetype="text/plain")
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    print(
        """
╔══════════════════════════════════════════════════════════════════════╗
║  🤖 KAIZEN × 🚀 NASA-LEVEL - Unified Dashboard                      ║
╚══════════════════════════════════════════════════════════════════════╝

🚀 Starting enhanced dashboard server with NASA-Level integration...

📊 CI/CD Monitoring Endpoints:
   • http://localhost:5000/           - Main dashboard
   • http://localhost:5000/api/health - Health check
   • http://localhost:5000/api/metrics - Metrics data
   • http://localhost:5000/api/runs   - Recent runs
   • http://localhost:5000/api/failures - Failing workflows
   • http://localhost:5000/api/report - Full report

🚀 NASA-Level Learning Endpoints:
   • http://localhost:5000/api/nasa/status - System status
   • http://localhost:5000/api/nasa/metrics - Learning metrics
   • http://localhost:5000/api/nasa/knowledge - All learned technologies
   • http://localhost:5000/api/nasa/knowledge/<tech> - Technology details
   • http://localhost:5000/api/nasa/search/<query> - Search knowledge base
   • http://localhost:5000/api/nasa/report - Comprehensive report
   • http://localhost:5000/api/nasa/prometheus - Prometheus metrics

🌸 МИРАЙ's choice: Unified dashboard for comprehensive monitoring
🤖 КАЙДЗЕН: Dashboard starting on port 5000...

"""
    )
    app.run(host="0.0.0.0", port=5000, debug=True)
