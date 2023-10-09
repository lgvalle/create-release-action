import subprocess
import sys
import re

def main():
    current_branch = get_current_branch()
    semver_version = extract_semver_version(current_branch)
    all_tags = list_all_tags()

    sorted_tags = sorted(all_tags, key=semver_key, reverse=True)
    previous_tag = find_previous_tag(semver_version, sorted_tags)

    if previous_tag is None:
        print(f"No previous tag found for branch {current_branch}. Exiting.")
        sys.exit(5)  # Exit code 5: No previous tag found

    commit_log = calculate_commit_log(previous_tag, current_branch)
    print(commit_log)

def get_current_branch():
    result = subprocess.run(["git", "symbolic-ref", "--short", "HEAD"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to get the current branch name.")
        sys.exit(1)  # Exit code 1: Failed to get the current branch name
    return result.stdout.strip()

def extract_semver_version(branch_name):
    semver_pattern = r'^release/v(\d+\.\d+\.\d+)$'
    match = re.match(semver_pattern, branch_name)
    if not match:
        print("Branch name doesn't follow the expected format (e.g., release/vX.Y.Z). Exiting.")
        sys.exit(2)  # Exit code 2: Branch name format is invalid
    return match.group(1)

def list_all_tags():
    result = subprocess.run(["git", "tag", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to list tags.")
        sys.exit(3)  # Exit code 3: Failed to list tags
    return result.stdout.strip().split("\n")

def semver_key(tag):
    match = re.match(r'^v(\d+)\.(\d+)\.(\d+)$', tag)
    if match:
        return [int(x) for x in match.groups()]
    else:
        return [0, 0, 0]

def find_previous_tag(semver_version, sorted_tags):
    for tag in sorted_tags:
        if tag != f'v{semver_version}':
            return tag
    return None

def calculate_commit_log(previous_tag, current_branch):
    result = subprocess.run(["git", "log", f"{previous_tag}..{current_branch}", "--pretty=format:%h - %an - %ad - %s", "--date=default"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to calculate the commit log.")
        sys.exit(4)  # Exit code 4: Failed to calculate the commit log
    return result.stdout.strip()

if __name__ == "__main__":
    main()
