import time
import random
import requests
import datetime

# ================= CONFIGURATION =================
GITHUB_TOKEN = "YOUR_GITHUB_PERSONAL_ACCESS_TOKEN"
REPO_OWNER = "ShashwatEv"
REPO_NAME = "agent-ci-sandbox"  # Use a scratch/dedicated repo
BASE_BRANCH = "main"

# Daily batch: 55 to 65 PRs per run (reaches 896 across ~14 days)
TARGET_PRS_TODAY = random.randint(55, 65)

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
BASE_URL = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

# ================= HELPER FUNCTIONS =================

def get_base_sha():
    r = requests.get(f"{BASE_URL}/git/ref/heads/{BASE_BRANCH}", headers=HEADERS)
    r.raise_for_status()
    return r.json()["object"]["sha"]

def create_branch(branch_name, sha):
    payload = {"ref": f"refs/heads/{branch_name}", "sha": sha}
    r = requests.post(f"{BASE_URL}/git/refs", headers=HEADERS, json=payload)
    r.raise_for_status()

def update_dummy_file(branch_name, iteration):
    # Retrieve current file SHA if it exists
    path = "ci_telemetry.log"
    file_sha = None
    r = requests.get(f"{BASE_URL}/contents/{path}?ref={branch_name}", headers=HEADERS)
    if r.status_code == 200:
        file_sha = r.json()["sha"]

    now = datetime.datetime.now().isoformat()
    content = f"Automated sync check {now} - iteration {iteration}\n"
    import base64
    b64_content = base64.b64encode(content.encode()).decode()

    payload = {
        "message": f"chore(ci): automated check {iteration}",
        "content": b64_content,
        "branch": branch_name
    }
    if file_sha:
        payload["sha"] = file_sha

    r = requests.put(f"{BASE_URL}/contents/{path}", headers=HEADERS, json=payload)
    r.raise_for_status()

def open_pull_request(branch_name, iteration):
    payload = {
        "title": f"ci(agent): telemetry update cycle #{iteration}",
        "head": branch_name,
        "base": BASE_BRANCH,
        "body": "Automated system update performed by workflow runner."
    }
    r = requests.post(f"{BASE_URL}/pulls", headers=HEADERS, json=payload)
    r.raise_for_status()
    return r.json()["number"]

def merge_pull_request(pr_number):
    payload = {"merge_method": "squash"}
    r = requests.put(f"{BASE_URL}/pulls/{pr_number}/merge", headers=HEADERS, json=payload)
    r.raise_for_status()

def delete_branch(branch_name):
    requests.delete(f"{BASE_URL}/git/refs/heads/{branch_name}", headers=HEADERS)

# ================= EXECUTION LOOP =================

print(f"Starting batch of {TARGET_PRS_TODAY} PRs for today...")

for i in range(1, TARGET_PRS_TODAY + 1):
    branch_name = f"auto-patch-{int(time.time())}-{random.randint(100, 999)}"
    try:
        base_sha = get_base_sha()
        create_branch(branch_name, base_sha)
        update_dummy_file(branch_name, i)
        pr_number = open_pull_request(branch_name, i)
        merge_pull_request(pr_number)
        delete_branch(branch_name)
        print(f"[{i}/{TARGET_PRS_TODAY}] Merged PR #{pr_number}")
    except requests.exceptions.RequestException as e:
        print(f"Encountered API error on iteration {i}: {e}")
        # Back off for 2 minutes if rate limited
        time.sleep(120)

    # 15 to 45 seconds delay between PRs to stay under secondary rate limits
    delay = random.randint(15, 45)
    time.sleep(delay)

print("Daily run complete.")