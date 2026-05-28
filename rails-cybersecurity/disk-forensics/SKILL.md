---
name: disk-forensics
description: "Analyze disk images, server snapshots, container filesystems, backups, and application artifacts for Ruby on Rails security investigations. Use when the user mentions disk forensics, Rails incident evidence, server image, backup review, deleted files, log recovery, ActiveStorage artifacts, database dumps, file carving, or forensic analysis of a Rails host."
allowed-tools: Bash, Read, Grep, Glob
---

# Disk Forensics — Rails Application Evidence Analysis

Analyze disk images, server snapshots, container layers, backups, and filesystem artifacts from Ruby on Rails environments. Preserve evidence, recover relevant files, reconstruct timelines, and identify Rails-specific incident artifacts.

## Validation Runner Mode

Run this skill as evidence validation, not education. Verify hashes, preserve read-only handling, and report only recovered artifacts, timelines, Rails evidence, material unknowns, and next forensic checks. Include paths, hashes, timestamps, and command evidence.

## Evidence Handling Principles

- Work on copies, not originals.
- Verify hashes before analysis.
- Mount images read-only.
- Document every command, timestamp, and finding.
- Preserve timestamps and metadata.
- Keep secrets and customer data out of reports unless needed for the investigation.

## Step 1: Identify and Verify Evidence

```bash
file <image-or-archive>
shasum -a 256 <image-or-archive>
```

Record:

- Evidence source and acquisition time.
- Expected hash, if provided.
- Image/archive format: raw/dd, E01, VMDK, VHD, tar, zip, Docker layer, database backup.
- Time zone of the source system.

For E01 images, use `ewfinfo` when available.

## Step 2: Mount or Extract Read-Only

Inspect partition layout:

```bash
fdisk -l <image>
mmls <image>
```

Mount read-only:

```bash
mount -o ro,loop,offset=<bytes> <image> /mnt/evidence
```

For archives, extract into a working directory and hash recovered files. For encrypted volumes, identify the encryption type and ask for the key or passphrase.

## Step 3: Locate Rails Application Artifacts

Search for Rails project roots:

```bash
find /mnt/evidence -name Gemfile -o -name config.ru -o -name credentials.yml.enc -o -name routes.rb 2>/dev/null
```

Prioritize:

```text
app/
config/
config/routes.rb
config/database.yml
config/storage.yml
config/cable.yml
config/credentials.yml.enc
config/master.key
Gemfile
Gemfile.lock
log/
tmp/
storage/
public/uploads/
public/assets/
db/schema.rb
db/structure.sql
db/seeds.rb
```

Also look for deployment and runtime files:

```text
.env
.env.production
Procfile
Dockerfile
docker-compose.yml
config/puma.rb
config/sidekiq.yml
config/initializers/
systemd units
nginx/apache configs
cron entries
Kamal/Capistrano configs
```

## Step 4: Rails Logs and Timeline

Collect and preserve logs:

```text
log/production.log
log/sidekiq.log
log/worker.log
log/nginx/access.log
log/nginx/error.log
/var/log/nginx/*
/var/log/apache2/*
/var/log/syslog
/var/log/auth.log
journalctl exports
```

Parse for:

- Admin access and impersonation.
- Login failures and password resets.
- CSRF failures.
- `Completed 500`, `ActionController::RoutingError`, `ActiveRecord::StatementInvalid`.
- Unusual params, long payloads, SQL errors, deserialization errors.
- Webhook failures and signature failures.
- File uploads, direct uploads, variants, and blob access.
- Sidekiq retries, dead jobs, and unexpected job classes.

Build a UTC timeline from logs and filesystem metadata. Note time zone conversions.

## Step 5: Secrets and Configuration Review

Search for exposed secrets and credential material:

```bash
grep -RIn "RAILS_MASTER_KEY\|secret_key_base\|DATABASE_URL\|REDIS_URL\|AWS_ACCESS_KEY_ID\|STRIPE_SECRET\|PRIVATE_KEY\|BEGIN .*PRIVATE KEY" /mnt/evidence 2>/dev/null
```

Handle secrets as sensitive evidence. Report presence, location, and likely exposure. Do not print full secret values unless the user specifically needs them for incident response.

Check:

- `config/master.key` present on disk or in backups.
- `.env` files in app roots, home directories, shell history, process dumps, CI workspaces.
- Rails credentials backups or plaintext copies.
- Database dumps with user, token, session, or PII data.

## Step 6: ActiveStorage and Uploaded Files

Rails apps often store evidence in:

```text
storage/
public/uploads/
tmp/storage/
tmp/uploads/
```

For ActiveStorage, correlate files with database records when a DB dump is available:

- `active_storage_blobs`.
- `active_storage_attachments`.
- `active_storage_variant_records`.

Review suspicious uploads:

- SVG, HTML, PDF, Office documents, archives.
- Files with double extensions or mismatched MIME types.
- Recently uploaded files near incident time.
- Oversized files or parser-crash candidates.

Use metadata tools on copies:

```bash
file <recovered-file>
exiftool <recovered-file>
shasum -a 256 <recovered-file>
```

## Step 7: Deleted Files and File Carving

Use Sleuth Kit when working with filesystem images:

```bash
fsstat -o <offset> <image>
fls -r -o <offset> <image>
icat -o <offset> <image> <inode> > recovered-file
```

Recover deleted Rails artifacts:

- Old `.env` files.
- Rotated logs.
- Database dumps.
- Uploaded payloads.
- Shell scripts, rake tasks, one-off maintenance scripts.
- Web shells or unexpected files in `public/`, `tmp/`, or upload directories.

Use carving tools such as `foremost` or `scalpel` only on copies.

## Step 8: System and Persistence Artifacts

Inspect host-level persistence and access:

- Shell history for deploy users: `.bash_history`, `.zsh_history`, `.irb_history`, `.rails_console_history`.
- SSH keys and `authorized_keys`.
- Cron, systemd timers, launch agents.
- Modified init scripts or service units.
- Unexpected binaries in `/tmp`, `/var/tmp`, app release directories, or shared directories.
- Package manager logs and deploy timestamps.
- Docker image layers and mounted volumes.

For Rails compromise, pay attention to:

- Modified initializers.
- Monkey patches in `config/initializers` or `lib/`.
- Added rake tasks.
- Changed views that skim forms.
- Backdoored jobs or mailers.
- New admin users or changed roles in database dumps.

## Output Format

```markdown
# Rails Forensic Analysis Report
## Case
## Evidence
## Date of Analysis

### Evidence Integrity
| Item | SHA256 | Verified | Notes |
|------|--------|----------|-------|

### Rails Applications Found
| Path | Rails Version | Environment | Notes |
|------|---------------|-------------|-------|

### Key Findings
#### [SEVERITY] [Title]
**Evidence:** [path/artifact]
**Timestamp:** [UTC]
**Hash:** [SHA256 when applicable]
**Description:** [what was found]
**Significance:** [why it matters]

### Timeline
| Time (UTC) | Event | Source | Notes |
|------------|-------|--------|-------|

### Recovered Files
| File | Source | Method | SHA256 | Significance |
|------|--------|--------|--------|--------------|

### Secrets and Sensitive Data Handling
| Location | Type | Exposure Concern | Recommended Action |
|----------|------|------------------|--------------------|

### Conclusions and Next Steps
1. [Immediate preservation or containment]
2. [Further analysis]
3. [Remediation]
```

## Boundaries

- Work only on provided images, backups, archives, and files.
- Maintain read-only access to source evidence.
- Do not tamper with evidence, logs, or timestamps.
- Do not expose secrets or personal data beyond investigative need.
- For real incidents, preserve chain of custody and recommend legal/IR escalation when appropriate.
- Refuse unauthorized device access or evidence manipulation.

## References

- NIST SP 800-86
- The Sleuth Kit
- SANS DFIR resources
- Rails Security Guide
- ActiveStorage documentation
