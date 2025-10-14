"""
🤖 KAIZEN CI/CD Monitoring Dashboard API
Flask backend for real-time CI/CD metrics visualization
"""

import asyncio
import json
import threading
from pathlib import Path

from core.cicd_monitor import CICDMonitor
from core.nasa_level.learning_pipeline import Priority
from core.nasa_level.orchestrator import NASALearningOrchestrator
from flask import Flask, jsonify, render_template, request, send_from_directory
from flask_cors import CORS
from modules.analytics_engine import get_analytics_engine
from modules.learning_api import TaskStatus, get_task_manager

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
CORS(app)

# Task manager для real-time learning
task_manager = get_task_manager()


# Запускаем task manager в отдельном потоке
def start_task_manager():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(task_manager.start())
    loop.run_forever()


task_manager_thread = threading.Thread(target=start_task_manager, daemon=True)
task_manager_thread.start()

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

# Initialize Analytics Engine
analytics = get_analytics_engine()


@app.route("/")
def index():
    """Main dashboard page"""
    return render_template("index.html")


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

# ============================================================================
# 📡 REAL-TIME LEARNING API
# ============================================================================


@app.route("/api/nasa/learn", methods=["POST"])
def nasa_learn():
    """
    Start a new learning task

    Body: {
        "technology": str,
        "depth": str (optional, default="basic"),
        "priority": str (optional, default="normal")
    }

    Returns: {
        "success": bool,
        "task_id": str,
        "message": str
    }
    """
    try:
        data = request.json
        if not data or "technology" not in data:
            return (
                jsonify(
                    {"success": False, "error": "Missing 'technology' in request body"}
                ),
                400,
            )

        technology = data["technology"]
        depth = data.get("depth", "basic")
        priority_str = data.get("priority", "normal").upper()

        # Parse priority
        try:
            priority = Priority[priority_str]
        except KeyError:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Invalid priority '{priority_str}'. Use: CRITICAL, HIGH, NORMAL, LOW",
                    }
                ),
                400,
            )

        # Add task
        task_id = task_manager.add_task(technology, depth, priority)

        return jsonify(
            {
                "success": True,
                "task_id": task_id,
                "message": f"Learning task for '{technology}' created successfully",
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/learn/<task_id>", methods=["GET"])
def nasa_learn_status(task_id):
    """
    Get status of a learning task

    Returns: {
        "success": bool,
        "task": {
            "task_id": str,
            "technology": str,
            "status": str,
            "progress": int,
            "result": dict,
            ...
        }
    }
    """
    try:
        task = task_manager.get_task(task_id)
        if not task:
            return (
                jsonify({"success": False, "error": f"Task '{task_id}' not found"}),
                404,
            )

        return jsonify({"success": True, "task": task.to_dict()})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/tasks", methods=["GET"])
def nasa_tasks():
    """
    Get all learning tasks

    Query params:
        - status: filter by status (pending, running, completed, failed)
        - limit: max number of tasks to return

    Returns: {
        "success": bool,
        "tasks": [...],
        "stats": {...}
    }
    """
    try:
        # Get filters
        status_filter = request.args.get("status")
        limit = request.args.get("limit", type=int)

        # Get all tasks
        all_tasks = task_manager.get_all_tasks()

        # Filter by status
        if status_filter:
            status_enum = TaskStatus(status_filter.lower())
            filtered_tasks = [t for t in all_tasks if t.status == status_enum]
        else:
            filtered_tasks = all_tasks

        # Sort by created_at (newest first)
        filtered_tasks.sort(key=lambda t: t.created_at, reverse=True)

        # Limit
        if limit:
            filtered_tasks = filtered_tasks[:limit]

        # Convert to dict
        tasks_data = [t.to_dict() for t in filtered_tasks]

        # Get stats
        stats = task_manager.get_stats()

        return jsonify({"success": True, "tasks": tasks_data, "stats": stats})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/learn/<task_id>", methods=["DELETE"])
def nasa_cancel_task(task_id):
    """
    Cancel a learning task

    Returns: {
        "success": bool,
        "message": str
    }
    """
    try:
        cancelled = task_manager.cancel_task(task_id)
        if cancelled:
            return jsonify(
                {"success": True, "message": f"Task '{task_id}' cancelled successfully"}
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": f"Task '{task_id}' cannot be cancelled (not found or already completed)",
                    }
                ),
                400,
            )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


# ============================================================================
# 📊 NASA SYSTEM STATUS & KNOWLEDGE
# ============================================================================


@app.route("/api/nasa/status")
def nasa_status():
    """Get NASA learning system status"""
    try:
        status = nasa_learning.get_status()

        # Add task manager stats
        status["task_manager"] = task_manager.get_stats()

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


# ═══════════════════════════════════════════════════════════════
# 🧠 ANALYTICS ENDPOINTS (Phase 3.3)
# ═══════════════════════════════════════════════════════════════


@app.route("/api/nasa/analytics/trends", methods=["GET"])
def get_trends():
    """Get learning trends analysis"""
    try:
        period = request.args.get("period", "week")  # day, week, month
        technology = request.args.get("technology")  # Optional filter

        trends = analytics.get_learning_trends(period=period, technology=technology)

        return jsonify(
            {
                "success": True,
                "trends": [
                    {
                        "period": t.period,
                        "technology": t.technology,
                        "metric": t.metric,
                        "values": t.values,
                        "timestamps": t.timestamps,
                        "trend_direction": t.trend_direction,
                        "confidence": t.confidence,
                    }
                    for t in trends
                ],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/analytics/recommendations", methods=["GET"])
def get_recommendations():
    """Get AI-powered technology recommendations"""
    try:
        limit = int(request.args.get("limit", 5))
        user_level = request.args.get("level", "intermediate")

        recommendations = analytics.get_technology_recommendations(
            limit=limit, user_level=user_level
        )

        return jsonify(
            {
                "success": True,
                "recommendations": [
                    {
                        "technology": r.technology,
                        "score": r.score,
                        "reason": r.reason,
                        "related_techs": r.related_techs,
                        "estimated_difficulty": r.estimated_difficulty,
                        "estimated_time_hours": r.estimated_time_hours,
                    }
                    for r in recommendations
                ],
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/analytics/predictions", methods=["GET"])
def get_predictions():
    """Get proficiency predictions for a technology"""
    try:
        technology = request.args.get("technology", "python")
        user_level = request.args.get("level", "intermediate")

        prediction = analytics.predict_proficiency(
            technology=technology, context={"user_level": user_level}
        )

        return jsonify(
            {
                "success": True,
                "prediction": {
                    "technology": prediction.technology,
                    "predicted_proficiency": prediction.predicted_proficiency,
                    "confidence": prediction.confidence,
                    "estimated_attempts": prediction.estimated_attempts,
                    "success_probability": prediction.success_probability,
                    "factors": prediction.factors,
                },
            }
        )
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/api/nasa/analytics/insights", methods=["GET"])
def get_insights():
    """Get performance insights and recommendations"""
    try:
        insights = analytics.get_performance_insights()

        return jsonify(
            {
                "success": True,
                "insights": [
                    {
                        "category": i.category,
                        "title": i.title,
                        "description": i.description,
                        "metric_value": i.metric_value,
                        "recommendation": i.recommendation,
                        "priority": i.priority,
                    }
                    for i in insights
                ],
            }
        )
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
   • http://localhost:5000/api/nasa/learn - Create learning task (POST)
   • http://localhost:5000/api/nasa/tasks - List all tasks

🧠 Analytics Endpoints (NEW):
   • http://localhost:5000/api/nasa/analytics/trends - Learning trends
   • http://localhost:5000/api/nasa/analytics/recommendations - What to learn next
   • http://localhost:5000/api/nasa/analytics/predictions - Success predictions
   • http://localhost:5000/api/nasa/analytics/insights - Performance insights

🌸 МИРАЙ's choice: Unified dashboard for comprehensive monitoring
🤖 КАЙДЗЕН: Dashboard starting on port 5000...

"""
    )
    app.run(host="0.0.0.0", port=5000, debug=True)
