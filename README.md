# ShopFlow — Secret Scanning & Remediation Lab

> **This is a deliberately insecure repository used for practicing secret detection and remediation.**
> All credentials are fake and for educational purposes only. Do not use any values from this repo in real systems.

## Purpose

This repo simulates a real-world codebase that has accumulated secrets over time — the way most teams actually end up with leaked credentials: rushed hotfixes, copied config snippets, test credentials left in CI, `.env` files committed before `.gitignore` was set up.

The goals of this repo are to:

1. **Practice secret scanning** — find all secrets across the working tree and git history using tools like `git-secrets`, `truffleHog`, `gitleaks`, `detect-secrets`, or GitHub secret scanning.
2. **Understand the blast radius** — map which secrets appear in how many places (code, config, CI/CD, IaC, Docker images, history).
3. **Practice remediation** — remove secrets from the live files, then purge them from git history using `git filter-repo` or BFG Repo Cleaner.
4. **Practice rotation** — understand which secrets must be rotated even after history is rewritten (anyone who cloned before the rewrite still has them).

---

## Repo Structure

```
.
├── .github/workflows/          # CI/CD pipelines (secrets in env blocks)
├── services/
│   ├── java-order-service/     # Spring Boot — secrets in .properties, .yml, Java source
│   ├── python-auth-service/    # FastAPI — secrets in .env, config.py, main.py, tests
│   └── node-api-gateway/       # Express.js — secrets in config JSON, middleware, routes
├── infra/
│   ├── k8s/secrets.yaml        # Base64-encoded secrets (not encrypted)
│   ├── terraform/              # AWS provider with hardcoded credentials
│   └── helm/shopflow/          # Helm values with plaintext secrets
└── scripts/                    # Deploy scripts with hardcoded credentials
```

## Services

| Service | Stack | Port | Description |
|---------|-------|------|-------------|
| `java-order-service` | Spring Boot 3 | 8080 | Order management & inventory |
| `python-auth-service` | FastAPI | 8000 | Authentication & user management |
| `node-api-gateway` | Express.js | 3000 | API Gateway & request routing |

## Architecture

```
Client → Node API Gateway → [Java Order Service | Python Auth Service]
                          ↓
                    [PostgreSQL | Redis | MongoDB]
```

---

## Secret Inventory

All secrets below are **intentionally fake** and seeded for scanning practice.

| Secret | Type | Locations in working tree |
|--------|------|--------------------------|
| `AKIAIOSFODNN7EXAMPLE` / `AKIAI44QH8DHBEXAMPLE` | AWS Access Key | `application.properties`, `application-prod.yml`, `terraform/main.tf`, `docker-compose.yml`, `scripts/deploy.sh`, `Dockerfile` ENV, `.github/workflows/deploy.yml`, `config/default.json`, `routers/products.py` |
| `wJalrXUtnFEMI/K7MDENG/...` | AWS Secret Key | Same locations as access key |
| `sk_live_51Hx8mKL...` | Stripe Secret Key | `StripeConfig.java`, `PaymentService.java`, `payments.js`, `application.properties`, `helm/values.yaml`, CI workflow |
| `Sup3rS3cr3t_PgPass!2024` | PostgreSQL Password | `application.properties`, `alembic.ini`, `docker-compose.yml`, `k8s/secrets.yaml` (base64), `terraform/main.tf`, `test_auth.py` |
| `my-super-secret-jwt-key-...` | JWT Secret | `core/config.py`, `auth.js`, `config/default.json`, CI env, `test_auth.py` |
| `SG.xK9pLmNq...` | SendGrid API Key | `main.py` (hardcoded), `core/config.py`, CI workflow, `notifications.js` |
| `1234567890abcdef...` | Twilio Auth Token | `main.py` (hardcoded), `core/config.py` |
| `hooks.slack.com/services/T04AB12CD/...` | Slack Webhook URL | `PaymentService.java`, `scripts/deploy.sh`, CI workflow `curl`, `production.json` |
| `dd4bfe3a7c9e1b2f8d5a6c4e7b9d0f2a` | DataDog API Key | `logger.js`, `config/default.json`, `application.properties` |
| `GOCSPX-xK9pLmNq...` | Google OAuth Secret | `main.py` (hardcoded fallback), `core/config.py` |
| `VuaCfGcBCdbkQm-e5aOx:ui2lp2axTNmsyakw9tvNnw` | Elasticsearch API Key | `routers/products.py` |
| `R01234567890abcdef...` | PagerDuty Integration Key | `notifications.js`, `production.json` |
| `AcGHFK3a...` / `EL5mNpQ...` | PayPal Client ID/Secret | `payments.js` (hotfix branch + main) |
| `r3d1s_P@ssw0rd_shopflow` | Redis Password | `application.properties`, `docker-compose.yml`, `config/default.json` |
| `M0ng0_Adm1n_P@ss` | MongoDB Password | `docker-compose.yml`, `.env` |

### Secrets buried in git history (not present in current files)

| Secret | Commit | File |
|--------|--------|------|
| `AKIAIOSFODNN7EXAMPLE` + secret key | `fc55281` | `AwsConfig.java` (removed in `eeed281` but still in history) |
| All `.env` values | `fc55281` | `.env` was committed before `.gitignore` was added |
| `Sup3rS3cr3t_PgPass!2024` in CI | `test.yml` | All historical commits of `test.yml` |

---

## Git History (Intentional Mess)

The commit history was built to simulate realistic patterns of secret accumulation:

```
main ──── initial app (secrets everywhere) ──── add .gitignore (too late)
     \                                       ──── partial cleanup of AwsConfig.java
      hotfix/payment ──── hardcoded Stripe + PayPal (merged to main)
      feature/catalog ─── Elastic Cloud key, hardcoded boto3 (merged to main)
```

Key learning moments in history:

- `.gitignore` added **after** `.env` was already committed — `.env` is in history forever
- `AwsConfig.java` had keys removed in a later commit but the old commit still contains them
- Hotfix branch merged hardcoded payment keys under time pressure
- CI workflow files expose secrets as plaintext `env:` values
- Kubernetes `secrets.yaml` stores base64 values (which are **not** encrypted)
- Terraform provider block has `access_key` / `secret_key` hardcoded

---

## Tool Installation

Install the tools below before working through the remediation exercises.

### gitleaks
Fast secret scanner written in Go.

```bash
# macOS
brew install gitleaks

# Linux (binary)
curl -sSL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks_linux_amd64.tar.gz | tar -xz
sudo mv gitleaks /usr/local/bin/

# Go (any platform)
go install github.com/gitleaks/gitleaks/v8@latest
```

**Verify:**
```bash
gitleaks version
```

### trufflehog
Scans for secrets in git history, filesystems, and more.

```bash
# macOS
brew install trufflesecurity/trufflehog/trufflehog

# Linux / macOS (binary installer)
curl -sSfL https://raw.githubusercontent.com/trufflesecurity/trufflehog/main/scripts/install.sh | sh -s -- -b /usr/local/bin

# Python (pip)
pip install trufflehog
```

**Verify:**
```bash
trufflehog --version
```

### detect-secrets
Yelp's plugin-based secret detection tool; useful for baselining and CI integration.

```bash
# macOS
brew install detect-secrets

# Linux / pipx (any platform)
pipx install detect-secrets
```

**Verify:**
```bash
detect-secrets --version
```

### git-filter-repo
The recommended tool for rewriting git history to purge secrets.

```bash
# macOS
brew install git-filter-repo

# Linux / pipx (any platform)
pipx install git-filter-repo
```

**Verify:**
```bash
git filter-repo --version
```

### BFG Repo Cleaner
Java-based alternative to `git filter-repo` — faster for simple cases like removing large files or replacing strings.

**Prerequisite:** Java 8+ must be installed (`java -version`).

```bash
# macOS
brew install bfg

# Manual (any platform) — download the JAR
curl -L -o bfg.jar https://repo1.maven.org/maven2/com/madgag/bfg/1.14.0/bfg-1.14.0.jar
```

**Verify:**
```bash
# Homebrew install
bfg --version

# Manual JAR install
java -jar bfg.jar --version
```

### git-secrets
Prevents committing secrets and credentials into git repositories.

```bash
# macOS
brew install git-secrets

# Linux (from source)
git clone https://github.com/awslabs/git-secrets.git
cd git-secrets && sudo make install

# Register AWS patterns in the current repo
git secrets --register-aws
git secrets --install
```

**Verify:**
```bash
git secrets --list
```

---

## Remediation Exercises

Each step below produces an output file consumed by the next step. Run them in order.

```
Step 1 ──► leaks.json ──┐
                         ├──► replacements.txt ──► Step 4 (purge) ──► Step 5 (verify)
Step 2 ──► history-leaks.json ──┘
```

---

### Step 1 — Scan the working tree → `leaks.json`

```bash
gitleaks detect --source . --report-format json --report-path leaks.json --verbose
```

**Output:** `leaks.json` — all secrets found in current files, one JSON object per finding.

```bash
# Preview: count of findings and which files are affected
jq 'length, ([.[].File] | unique)' leaks.json
```

---

### Step 2 — Scan git history → `history-leaks.json`

```bash
gitleaks detect --source . --log-opts="--all" --report-format json --report-path history-leaks.json --verbose
```

**Output:** `history-leaks.json` — all secrets found across every commit, including deleted files and old branches.

```bash
# Preview: how many unique commits contain secrets
jq '[.[].Commit] | unique | length' history-leaks.json
```

---

### Step 3 — Consolidate findings → `replacements.txt`

Merge both scan outputs, deduplicate, and build a replacement map for `git filter-repo`.

```bash
jq -r '.[].Secret' leaks.json history-leaks.json \
  | sort \
  | uniq -c \
  | sort -rn \
  | tee /dev/stderr \
  | awk '
      { print $2"==>***REMOVED***"; unique++; total += $1 }
      END { print "\nUnique secrets: " unique "\nTotal occurrences: " total > "/dev/stderr" }
    ' \
  > replacements.txt
```

**Output:** `replacements.txt` — one `secret==>***REMOVED***` line per unique secret value.

```bash
# Review before purging
cat replacements.txt
```

---

### Step 4 — Purge secrets from history

Rewrites all commits, replacing every value in `replacements.txt` with `***REMOVED***`.

```bash
git filter-repo --replace-text replacements.txt
```

For secrets in specific files (e.g. `.env` committed before `.gitignore`):

```bash
git filter-repo --path .env --invert-paths
```

---

### Step 5 — Verify remediation

Use the same secret values from the scan outputs to confirm nothing remains in history.

```bash
jq -r '.[].Secret' leaks.json history-leaks.json | sort -u | while IFS= read -r secret; do
  count=$(git log --all -p | grep -Fc "$secret" || true)
  printf "%-60s %s occurrences remaining\n" "$secret" "$count"
done
```

Every line should show `0 occurrences remaining`. Any non-zero value means the purge missed that secret.

---

### Step 6 — What can't be fixed by history rewrite?
- Any clone or fork made before the rewrite still has the secrets
- CI logs that printed the values
- Docker image layers pushed to a registry
- The answer: always **rotate the credentials**, rewriting history alone is not enough

---

## Infrastructure

- PostgreSQL (orders, users)
- Redis (session store, caching)
- MongoDB (product catalog)
- AWS S3 (static assets)
- RabbitMQ (async messaging)

## Quick Start (for exploring the app structure)

```bash
docker-compose up -d
```
