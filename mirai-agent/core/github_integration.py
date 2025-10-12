"""
GitHub API Integration для МИРАЙ
Работа с репозиториями, issues, PR через GitHub API
"""

import os
import json
import requests
from typing import Dict, List, Optional, Any


class GitHubIntegration:
    """Интеграция с GitHub API"""

    def __init__(self, token: Optional[str] = None):
        # Пытаемся загрузить токен
        self.token = token
        if not self.token:
            self.token = self._load_token()

        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json",
        }

        if self.token:
            self.headers["Authorization"] = f"token {self.token}"
            self.authenticated = True
        else:
            self.authenticated = False

    def _load_token(self) -> Optional[str]:
        """Загрузить токен из конфига"""
        try:
            # Из api_keys.json
            config_path = "/root/mirai/mirai-agent/configs/api_keys.json"
            if os.path.exists(config_path):
                with open(config_path, "r") as f:
                    config = json.load(f)
                    return config.get("GITHUB_TOKEN")

            # Из переменной окружения
            return os.getenv("GITHUB_TOKEN")
        except:
            return None

    def is_authenticated(self) -> bool:
        """Проверить авторизацию"""
        if not self.authenticated:
            return False

        try:
            response = requests.get(
                f"{self.base_url}/user", headers=self.headers, timeout=10
            )
            return response.status_code == 200
        except:
            return False

    def get_user_info(self) -> Dict[str, Any]:
        """Получить информацию о текущем пользователе"""
        if not self.authenticated:
            return {
                "error": "Not authenticated. Please add GITHUB_TOKEN to configs/api_keys.json"
            }

        try:
            response = requests.get(
                f"{self.base_url}/user", headers=self.headers, timeout=10
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def list_repos(self, username: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Получить список репозиториев"""
        if not self.authenticated:
            return [{"error": "Not authenticated"}]

        try:
            if username:
                url = f"{self.base_url}/users/{username}/repos"
            else:
                url = f"{self.base_url}/user/repos"

            response = requests.get(
                url,
                headers=self.headers,
                params={"per_page": limit, "sort": "updated"},
                timeout=10,
            )

            if response.status_code == 200:
                repos = response.json()
                return [
                    {
                        "name": r["name"],
                        "full_name": r["full_name"],
                        "description": r.get("description", ""),
                        "url": r["html_url"],
                        "language": r.get("language", "Unknown"),
                        "stars": r["stargazers_count"],
                        "forks": r["forks_count"],
                        "private": r["private"],
                    }
                    for r in repos
                ]
            else:
                return [{"error": f"HTTP {response.status_code}"}]
        except Exception as e:
            return [{"error": str(e)}]

    def create_repo(
        self, name: str, description: str = "", private: bool = False
    ) -> Dict:
        """Создать новый репозиторий"""
        if not self.authenticated:
            return {"error": "Not authenticated"}

        try:
            response = requests.post(
                f"{self.base_url}/user/repos",
                headers=self.headers,
                json={"name": name, "description": description, "private": private},
                timeout=10,
            )

            if response.status_code == 201:
                repo = response.json()
                return {
                    "success": True,
                    "name": repo["name"],
                    "url": repo["html_url"],
                    "clone_url": repo["clone_url"],
                }
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def create_issue(self, owner: str, repo: str, title: str, body: str = "") -> Dict:
        """Создать issue в репозитории"""
        if not self.authenticated:
            return {"error": "Not authenticated"}

        try:
            response = requests.post(
                f"{self.base_url}/repos/{owner}/{repo}/issues",
                headers=self.headers,
                json={"title": title, "body": body},
                timeout=10,
            )

            if response.status_code == 201:
                issue = response.json()
                return {
                    "success": True,
                    "number": issue["number"],
                    "url": issue["html_url"],
                }
            else:
                return {"error": f"HTTP {response.status_code}: {response.text}"}
        except Exception as e:
            return {"error": str(e)}

    def get_repo_content(self, owner: str, repo: str, path: str = "") -> Dict:
        """Получить содержимое файла/директории из репозитория"""
        try:
            response = requests.get(
                f"{self.base_url}/repos/{owner}/{repo}/contents/{path}",
                headers=self.headers,
                timeout=10,
            )

            if response.status_code == 200:
                return response.json()
            else:
                return {"error": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"error": str(e)}

    def search_repositories(self, query: str, limit: int = 10) -> List[Dict]:
        """Поиск репозиториев"""
        try:
            response = requests.get(
                f"{self.base_url}/search/repositories",
                headers=self.headers,
                params={"q": query, "per_page": limit, "sort": "stars"},
                timeout=10,
            )

            if response.status_code == 200:
                items = response.json()["items"]
                return [
                    {
                        "name": r["name"],
                        "full_name": r["full_name"],
                        "description": r.get("description", ""),
                        "url": r["html_url"],
                        "stars": r["stargazers_count"],
                        "language": r.get("language", "Unknown"),
                    }
                    for r in items
                ]
            else:
                return [{"error": f"HTTP {response.status_code}"}]
        except Exception as e:
            return [{"error": str(e)}]


# Пример использования
if __name__ == "__main__":
    gh = GitHubIntegration()

    print("🔍 Проверка GitHub интеграции:")
    print("-" * 60)

    if gh.is_authenticated():
        print("✅ Авторизация успешна!")

        user = gh.get_user_info()
        print(f"\n👤 Пользователь: {user.get('login', 'Unknown')}")
        print(f"📧 Email: {user.get('email', 'Not public')}")
        print(f"📦 Публичных репозиториев: {user.get('public_repos', 0)}")

        print("\n📂 Последние репозитории:")
        repos = gh.list_repos(limit=5)
        for repo in repos:
            if "error" not in repo:
                print(f"   • {repo['name']} ⭐ {repo['stars']} ({repo['language']})")
    else:
        print("❌ Не авторизован")
        print("\nДобавьте GITHUB_TOKEN в configs/api_keys.json:")
        print('{"GITHUB_TOKEN": "ghp_your_token_here"}')
