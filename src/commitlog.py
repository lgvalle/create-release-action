import subprocess
import sys
import re
import argparse

def main():
    parser = argparse.ArgumentParser(description="Calculate commit log between previous tag or main branch and current branch")
    parser.add_argument("--branch", help="The current branch name")
    parser.add_argument("--default-branch", help="The default branch name")

    args = parser.parse_args()

    current_branch = args.branch
    default_branch = args.default_branch if args.default_branch else get_default_remote_branch()

    semver_version = extract_semver_version(current_branch)
    all_tags = list_all_tags()

    sorted_tags = sorted(all_tags, key=semver_key, reverse=True)
    previous_tag = find_previous_tag(semver_version, sorted_tags)

    if previous_tag is None:
        print(f"No previous tag found for branch {current_branch}. Comparing with the default branch ({default_branch}).")

    commit_log = calculate_commit_log(previous_tag or default_branch, current_branch)
    print(commit_log)

def extract_semver_version(branch_name):
    semver_pattern = r'^release/v(\d+\.\d+\.\d+)$'
    match = re.match(semver_pattern, branch_name.strip())  # Use strip() to remove any whitespace
    if not match:
        print(f"Branch name {branch_name} doesn't follow the expected format (e.g., release/vX.Y.Z). Exiting.", file=sys.stderr)
        sys.exit(2)  # Exit code 2: Branch name format is invalid
    return match.group(1)

def list_all_tags():
    result = subprocess.run(["git", "tag", "-l"], capture_output=True, text=True)
    if result.returncode != 0:
        print("Failed to list tags.", file=sys.stderr)
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
    git_command = ["git", "log", f"{previous_tag}..{current_branch}", "--pretty=format:\"%h - %an - %ad - %s\"", "--date=default"]
    resolved_command = ' '.join(git_command)
    print(f"Executing git command: {' '.join(git_command)}")

    result = subprocess.run(git_command, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Failed to calculate the commit log between {previous_tag}..{current_branch} with the command {resolved_command}", file=sys.stderr)
        sys.exit(4)  # Exit code 4: Failed to calculate the commit log

    return result.stdout.strip()

def get_default_remote_branch():
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "refs/remotes/origin/HEAD"],
            capture_output=True, text=True, check=True
        )
        remote_branch = result.stdout.strip().split('/')[-1]
        return remote_branch
    except subprocess.CalledProcessError as e:
        print("Failed to determine the default remote branch.", file=sys.stderr)
        sys.exit(6)  # Exit code 6: Failed to determine the default remote branch

if __name__ == "__main__":
    main()
