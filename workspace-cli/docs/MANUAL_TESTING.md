# Manual Testing Guide

This document outlines essential manual tests to perform before creating a release tag. These tests verify functionality that automated tests cannot easily cover.

## Prerequisites

- Clean environment (preferably a fresh VM or container)
- Git installed
- Python managed by ASDF (as specified in `.tool-versions`)
- VS Code (latest version)
- Dev Containers extension for VS Code (latest version)

## Test Cases

### 1. Installation Test

**Purpose**: Verify the CLI can be installed from source

```bash
# Clone the repository
git clone https://github.com/matthew-dresden/agentic-workspace.git
cd devcontainer

# Install the CLI
pip install ./workspace-cli

# Verify installation
workspace --version
# Should display: "Agentic Workspace CLI X.Y.Z"
```

### 2. Interactive Setup Test

**Purpose**: Verify the interactive setup process works with user input

```bash
# Create a test directory
mkdir -p /tmp/test-project
cd /tmp/test-project

# Run the setup command in interactive mode
workspace setup-devcontainer .

# .tool-versions is auto-created as an empty file before prompts begin
# Follow the prompts with these values:
# - No saved template
# - AWS Config: false
# - Claude Code CLI: true
# - Git branch: main
# - Developer name: Test User
# - Git provider: github.com
# - Git username: testuser
# - Git email: test@example.com
# - Git token: test-token
# - Extra packages: (leave empty)
# - Pager: cat
# - Don't save as template

# Verify files were created
ls -la .devcontainer/
cat devcontainer-environment-variables.json
# Should see the values you entered
cat .tool-versions
# Should exist and be empty
```

### 3. Template Save and Load Workflow

**Purpose**: Verify the complete template workflow across projects

```bash
# Save the template from the previous test
cd /tmp/test-project
workspace template save test-template

# Create a new project
mkdir -p /tmp/test-project2
cd /tmp/test-project2

# List templates
workspace template list
# Should see "test-template" in the list

# Load the template
workspace template load test-template

# Verify the environment file was created
cat devcontainer-environment-variables.json
# Should contain the same values as the first project
```

### 4. VS Code Launch and Container Build

**Purpose**: Verify VS Code launches and builds the container correctly

```bash
# Navigate to a project with devcontainer setup
cd /tmp/test-project

# Launch VS Code
workspace code .

# Verify:
# 1. VS Code opens
# 2. You get a prompt to reopen in container
# 3. After reopening, the container builds successfully
# 4. The terminal in VS Code shows the correct environment
```

### 5. AWS Profile Configuration

**Purpose**: Verify AWS profile configuration works correctly (if applicable)

```bash
# Create a new project with AWS enabled
mkdir -p /tmp/test-project-aws
cd /tmp/test-project-aws

# Run setup with AWS enabled
workspace setup-devcontainer .

# .tool-versions is auto-created as an empty file
# Follow prompts, this time set:
# - AWS_CONFIG_ENABLED: true
# - Complete all environment prompts (branch, name, git, proxy, pager, etc.)
# - AWS output format: json
# - Add a simple AWS profile configuration when prompted

# Verify AWS profile map was created
cat .devcontainer/aws-profile-map.json
# Verify .tool-versions was created (empty)
cat .tool-versions
```

### 6. .tool-versions File Management Test

**Purpose**: Verify .tool-versions file detection and auto-creation

```bash
# Test 1: Project without .tool-versions
mkdir -p /tmp/test-no-tool-versions
cd /tmp/test-no-tool-versions

# Run setup — .tool-versions is auto-created as an empty file before prompts begin
workspace setup-devcontainer .
# Complete the interactive setup prompts

# Verify file was created (empty — Python is managed via devcontainer features)
cat .tool-versions
# Should exist and be empty

# Test 2: Project with existing .tool-versions
mkdir -p /tmp/test-existing-tool-versions
cd /tmp/test-existing-tool-versions
echo "python 3.11.5" > .tool-versions

# Run setup
workspace setup-devcontainer .
# Should detect existing file; if it contains a Python entry, a notice is shown
# recommending Python be managed through devcontainer features instead

# Verify original content preserved
cat .tool-versions
# Should still contain: python 3.11.5
```

### 7. Catalog URL Override Test

**Purpose**: Verify the --catalog-url flag works with different git references

```bash
# Test 1: Use main branch instead of the auto-resolved semver tag
mkdir -p /tmp/test-catalog-url-main
cd /tmp/test-catalog-url-main

# Run setup pinned to main branch via --catalog-url
workspace setup-devcontainer --catalog-url "https://github.com/matthew-dresden/agentic-workspace.git@main" .
# Should clone from main branch instead of the auto-resolved semver tag

# Verify files were created
ls -la .devcontainer/
# Should see devcontainer files

# Test 2: Use a specific semver tag via --catalog-url
mkdir -p /tmp/test-catalog-url-tag
cd /tmp/test-catalog-url-tag

# Run setup pinned to a specific tag
workspace setup-devcontainer --catalog-url "https://github.com/matthew-dresden/agentic-workspace.git@0.1.0" .
# Should clone from the specified tag

# Verify files were created
ls -la .devcontainer/
# Should see devcontainer files

# Test 3: Invalid catalog URL should fail gracefully
mkdir -p /tmp/test-catalog-url-invalid
cd /tmp/test-catalog-url-invalid

# Run setup with an invalid repository URL
workspace setup-devcontainer --catalog-url "https://github.com/nonexistent/repo.git" .
# Should fail with a clear error message about the catalog not being accessible
# Exit code should be non-zero
```

### 8. Template Create Test

**Purpose**: Verify template create command works correctly

```bash
# Test 1: Create template with current CLI version
workspace template create test-template

# Follow the interactive prompts with test values:
# - AWS Config: false
# - Claude Code CLI: true
# - Git branch: main
# - Developer name: Test User
# - Git provider: github.com
# - Git auth method: token
# - Git username: testuser
# - Git email: test@example.com
# - Git token: test-token
# - Extra packages: (leave empty)
# - Pager: cat
# - Host proxy: false
# - No custom env vars

# Verify template was created
workspace template list
# Should see "test-template" in the list

# Test 2: Verify template content
cat ~/.workspace-templates/test-template.json
# Should contain current CLI version

# Clean up test template
workspace template delete test-template
```

### 9. Template Create Help Test

**Purpose**: Verify help text is correct

```bash
# Test help command
workspace template create --help
# Should display help text for template creation
```

### 10. Catalog List Test

**Purpose**: Verify the catalog list command displays available entries

```bash
# Test 1: List entries from the default catalog
workspace catalog list
# Should display a formatted list of available devcontainer configurations
# with "default" entry listed first

# Test 2: Filter by tags
workspace catalog list --tags general
# Should only show entries matching the "general" tag

# Test 3: Filter with no matches
workspace catalog list --tags nonexistent-tag
# Should display "No entries found matching tags: nonexistent-tag"

# Test 4: Custom catalog URL
export WORKSPACE_CATALOG_URL="https://github.com/matthew-dresden/agentic-workspace.git"
workspace catalog list
# Should display entries from the specified catalog
unset WORKSPACE_CATALOG_URL

# Test 5: Invalid catalog URL should fail gracefully
export WORKSPACE_CATALOG_URL="https://github.com/nonexistent/repo.git"
workspace catalog list
# Should fail with actionable error message about cloning
# Exit code should be non-zero
unset WORKSPACE_CATALOG_URL
```

### 11. Catalog Validate Test

**Purpose**: Verify the catalog validate command checks catalog structure

```bash
# Test 1: Validate local catalog (this repository)
cd /path/to/devcontainer
workspace catalog validate --local .
# Should display "Catalog validation passed. N entries found."

# Test 2: Validate remote default catalog
workspace catalog validate
# Should clone and validate the default catalog

# Test 3: Validate invalid directory
workspace catalog validate --local /tmp/empty-dir
# Should fail with validation errors

# Test 4: Validate nonexistent directory
workspace catalog validate --local /nonexistent/path
# Should fail with "Directory not found" error
```

### 12. Setup-DevContainer Catalog Integration Test

**Purpose**: Verify catalog integration in the setup-devcontainer command

```bash
# Test 1: --catalog-entry flag requires WORKSPACE_CATALOG_URL
unset WORKSPACE_CATALOG_URL
mkdir -p /tmp/test-catalog-entry
workspace setup-devcontainer --catalog-entry my-collection /tmp/test-catalog-entry
# Should fail with error about WORKSPACE_CATALOG_URL not being set
# Exit code should be non-zero

# Test 2: --catalog-entry flag with env var set
export WORKSPACE_CATALOG_URL="https://github.com/matthew-dresden/agentic-workspace.git"
mkdir -p /tmp/test-catalog-entry2
workspace setup-devcontainer --catalog-entry default /tmp/test-catalog-entry2
# Should clone the catalog, find the "default" entry, display metadata
# Ask "Is this correct?" and continue with setup
unset WORKSPACE_CATALOG_URL

# Test 3: Source selection when WORKSPACE_CATALOG_URL is set
export WORKSPACE_CATALOG_URL="https://github.com/matthew-dresden/agentic-workspace.git"
mkdir -p /tmp/test-source-select
workspace setup-devcontainer /tmp/test-source-select
# Should present a source selection prompt:
# > Default General DevContainer
#   Browse specialized configurations from catalog
# Select "Default" and verify setup continues normally
unset WORKSPACE_CATALOG_URL

# Test 4: Default setup (no WORKSPACE_CATALOG_URL)
unset WORKSPACE_CATALOG_URL
mkdir -p /tmp/test-default-catalog
workspace setup-devcontainer /tmp/test-default-catalog
# Should auto-clone default catalog and auto-select the default entry
# No source selection prompt should appear
```

### 13. Code Command Catalog Integration Test

**Purpose**: Verify catalog integration in the code command (Step 5 Option 1)

```bash
# Test 1: Step 5 Option 1 with catalog-entry.json present
# First, set up a project using catalog
mkdir -p /tmp/test-code-catalog
workspace setup-devcontainer /tmp/test-code-catalog
# Complete the interactive setup

# Verify catalog-entry.json was created in .devcontainer/
cat /tmp/test-code-catalog/.devcontainer/catalog-entry.json
# Should contain "name" and "catalog_url" fields

# Now simulate missing variables scenario:
# Edit the devcontainer-environment-variables.json to remove a key
# Then run code command
workspace code /tmp/test-code-catalog
# If missing variables detected, select "Update devcontainer configuration and add missing variables"
# Should show replacement notification, ask for acknowledgement
# Should clone catalog from catalog-entry.json URL, replace .devcontainer/ files

# Test 2: Step 1 metadata missing — Yes path
# Create a project with no metadata in project files
mkdir -p /tmp/test-code-metadata
mkdir -p /tmp/test-code-metadata/.devcontainer
echo '{"containerEnv": {"DEVELOPER_NAME": "test"}}' > /tmp/test-code-metadata/devcontainer-environment-variables.json
echo "export DEVELOPER_NAME='test'" > /tmp/test-code-metadata/shell.env
workspace code /tmp/test-code-metadata
# Should detect missing metadata and prompt
# Select "Yes — select or create a template to regenerate files"
# Should run interactive setup to regenerate files
```

## Reporting Issues

If any test fails:

1. Note the exact command that failed
2. Capture any error messages
3. Document the environment (OS, Python version)
4. Create an issue with these details
