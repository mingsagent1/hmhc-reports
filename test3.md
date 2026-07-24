# Test 3: Claude session write access

One-off test after the repo transfer to the **hmhc-ai** org.

Verifies that this Claude Code session (as mingsagent1) can:

1. Create a branch via the GitHub API.
2. Push a commit to it.
3. Open a pull request against `main`.
4. Merge it — exercising the `protect-main` ruleset bypass for the `ai-editors` team.

This file is disposable; it can be deleted together with `testmerge.md` in the cleanup PR.
