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

## Remediation Exercises

### Exercise 1 — Scan the working tree
Use any of these tools to find secrets in current files:
```bash
gitleaks detect --source . --verbose
trufflehog filesystem .
detect-secrets scan > .secrets.baseline
```

### Exercise 2 — Scan git history
```bash
gitleaks detect --source . --log-opts="--all" --verbose
trufflehog git file://. --since-commit HEAD~10 --branch main
```

### Exercise 3 — Purge secrets from history
```bash
# Install git-filter-repo first
pip install git-filter-repo

# Remove a file entirely from history
git filter-repo --path .env --invert-paths

# Replace a secret string in all history
git filter-repo --replace-text <(echo 'AKIAIOSFODNN7EXAMPLE==>***REMOVED***')
```

### Exercise 4 — Verify remediation
After rewriting history, confirm the secret no longer appears anywhere:
```bash
git log --all -p | grep "AKIAIOSFODNN7EXAMPLE"
# Should return nothing
```

### Exercise 5 — What can't be fixed by history rewrite?
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
