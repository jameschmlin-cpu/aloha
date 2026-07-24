---
name: security-gate
description: Enforces Genesis project coding standards, AST integrity, S1-S4 specifications, and SHA-256 hash checks before finalizing code writes.
triggers:
  - pre_write
  - file_modify
  - code_review
  - pre_commit
---

# Skill: Genesis Security Gate & AST Validator

This skill ensures that all code modifications, new script creations, and configurations conform to the strict, closed-loop safety guidelines of the Genesis project before any write operations are committed.

## Operations Flow

Whenever the agent is requested to create or edit python code files under `C:\Genesis`:

1.  **Code Preparation**:
    Ensure the code contains the `# -*- coding: utf-8 -*-` encoding comment at line 1 or 2.
    Do not use empty `pass` statements in function or class bodies. Empty functions must return a placeholder value (e.g., `return True` or `return None`) or throw an explicit error.

2.  **Run Validation Check**:
    Execute the helper script:
    `python C:\Genesis\.agents\skills\security-gate\scripts\validate_hash.py <target_file_path>`

3.  **Audit Exit Code**:
    - If the script outputs `[STATUS] PASSED` (Exit Code 0), the modification is safe. Proceed with writing the file.
    - If the script outputs errors or warnings (Exit Code 1), stop immediately. The code contains logical defects (e.g., pass statement violations or encoding issues). Fix the defects before attempting to write.

4.  **Register Code Hash**:
    Log the computed SHA-256 hash of the modified script to the DB or event streams as requested.
