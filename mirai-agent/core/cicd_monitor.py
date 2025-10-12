"""
🤖 KAIZEN CI/CD Monitoring System
Monitors GitHub Actions workflows and provides real-time metrics
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import asyncio
from pathlib import Path


class CICDMonitor:
    """Monitor GitHub Actions CI/CD pipelines"""

    def __init__(self, github_token: str, repo_owner: str, repo_name: str):
        self.token = github_token
        self.owner = repo_owner
        self.repo = repo_name
        self.base_url = "https://api.github.com"
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def get_workflow_runs(self, limit: int = 10) -> List[Dict]:
        """Get recent workflow runs"""
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/actions/runs"
        params = {"per_page": limit}

        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()

        return response.json()["workflow_runs"]

    def get_workflow_metrics(self) -> Dict:
        """Calculate CI/CD metrics"""
        runs = self.get_workflow_runs(limit=50)

        total_runs = len(runs)
        successful = sum(1 for r in runs if r["conclusion"] == "success")
        failed = sum(1 for r in runs if r["conclusion"] == "failure")
        in_progress = sum(1 for r in runs if r["status"] == "in_progress")

        success_rate = (successful / total_runs * 100) if total_runs > 0 else 0

        # Average duration for successful runs
        durations = []
        for run in runs:
            if run["conclusion"] == "success" and run.get("run_started_at"):
                start = datetime.fromisoformat(
                    run["run_started_at"].replace("Z", "+00:00")
                )
                end = datetime.fromisoformat(run["updated_at"].replace("Z", "+00:00"))
                durations.append((end - start).total_seconds())

        avg_duration = sum(durations) / len(durations) if durations else 0

        return {
            "total_runs": total_runs,
            "successful": successful,
            "failed": failed,
            "in_progress": in_progress,
            "success_rate": round(success_rate, 2),
            "avg_duration_seconds": round(avg_duration, 2),
            "avg_duration_minutes": round(avg_duration / 60, 2),
            "last_run": runs[0] if runs else None,
        }

    def check_health(self) -> Dict:
        """Check CI/CD health status"""
        metrics = self.get_workflow_metrics()

        # Health criteria
        is_healthy = (
            metrics["success_rate"] >= 80
            and metrics["failed"] < 5
            and metrics["in_progress"] < 3
        )

        status = "🟢 HEALTHY" if is_healthy else "🔴 UNHEALTHY"

        if metrics["success_rate"] >= 90:
            grade = "A+"
        elif metrics["success_rate"] >= 80:
            grade = "A"
        elif metrics["success_rate"] >= 70:
            grade = "B"
        elif metrics["success_rate"] >= 60:
            grade = "C"
        else:
            grade = "F"

        return {
            "status": status,
            "grade": grade,
            "is_healthy": is_healthy,
            "metrics": metrics,
            "timestamp": datetime.now().isoformat(),
        }

    def get_failing_workflows(self) -> List[Dict]:
        """Get currently failing workflows"""
        runs = self.get_workflow_runs(limit=20)

        failing = [
            {
                "name": r["name"],
                "run_number": r["run_number"],
                "conclusion": r["conclusion"],
                "html_url": r["html_url"],
                "created_at": r["created_at"],
                "head_commit": r["head_commit"]["message"],
            }
            for r in runs
            if r["conclusion"] == "failure"
        ]

        return failing

    def generate_report(self) -> str:
        """Generate human-readable monitoring report"""
        health = self.check_health()
        metrics = health["metrics"]

        report = f"""
╔══════════════════════════════════════════════════════════════════════╗
║  🤖 KAIZEN CI/CD Monitoring Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ║
╚══════════════════════════════════════════════════════════════════════╝

📊 HEALTH STATUS: {health['status']} (Grade: {health['grade']})

📈 METRICS (Last 50 runs):
   • Total Runs:      {metrics['total_runs']}
   • Successful:      {metrics['successful']} ✅
   • Failed:          {metrics['failed']} ❌
   • In Progress:     {metrics['in_progress']} ⏳
   • Success Rate:    {metrics['success_rate']}%
   • Avg Duration:    {metrics['avg_duration_minutes']} min

"""

        if metrics["last_run"]:
            last = metrics["last_run"]
            emoji = (
                "✅"
                if last["conclusion"] == "success"
                else "❌" if last["conclusion"] == "failure" else "⏳"
            )
            report += f"""
🔄 LAST RUN:
   {emoji} Workflow: {last['name']}
   • Run #: {last['run_number']}
   • Status: {last['status']} → {last['conclusion'] or 'running'}
   • Commit: {last['head_commit']['message'].split(chr(10))[0][:60]}
   • URL: {last['html_url']}
"""

        failing = self.get_failing_workflows()
        if failing:
            report += f"\n⚠️  FAILING WORKFLOWS ({len(failing)}):\n"
            for f in failing[:5]:
                report += f"   ❌ {f['name']} (#{f['run_number']})\n"
                report += f"      {f['head_commit'][:60]}\n"
        else:
            report += "\n✨ NO FAILING WORKFLOWS - ALL GREEN! ✨\n"

        report += "\n" + "=" * 70 + "\n"

        return report

    async def monitor_continuous(self, interval_seconds: int = 300):
        """Continuous monitoring loop"""
        print(
            f"🤖 KAIZEN: Starting continuous CI/CD monitoring (every {interval_seconds}s)"
        )

        while True:
            try:
                report = self.generate_report()
                print(report)

                # Check for failures
                health = self.check_health()
                if not health["is_healthy"]:
                    print("🚨 ALERT: CI/CD pipeline is UNHEALTHY!")
                    # Here we would send Telegram notification

                await asyncio.sleep(interval_seconds)

            except Exception as e:
                print(f"❌ Monitoring error: {e}")
                await asyncio.sleep(60)


def main():
    """Main monitoring function"""
    # Load config
    config_path = Path(__file__).parent.parent / "configs" / "api_keys.json"
    with open(config_path) as f:
        config = json.load(f)

    token = config.get("GITHUB_TOKEN")
    if not token or token.startswith("ghp_") is False:
        print("❌ GitHub token not configured in api_keys.json")
        return

    # Monitor mirai-showcase repository
    monitor = CICDMonitor(
        github_token=token, repo_owner="AgeeKey", repo_name="mirai-showcase"
    )

    # Generate and print report
    report = monitor.generate_report()
    print(report)

    # Show health check
    health = monitor.check_health()
    print(f"\n🏥 Health Check: {health['status']}")
    print(f"📊 Grade: {health['grade']}")
    print(f"✅ Success Rate: {health['metrics']['success_rate']}%")

    # Offer continuous monitoring
    print("\n💡 To start continuous monitoring, run:")
    print(
        "   python3 -c 'import asyncio; from core.cicd_monitor import CICDMonitor; asyncio.run(CICDMonitor(...).monitor_continuous())'"
    )


if __name__ == "__main__":
    main()
