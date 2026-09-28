# Akki — where we are, in plain language (2026-09-28)

> **Historical report — corrected by the later descriptor review.** The ~35%
> figure is an unreconciled planning estimate, not verified programme completion.
> Revised remaining shares below do not sum to 100%. NAS is now owner-reported
> mounted at `/mnt/nfs-share`; worker/read-only verification is E1 work before
> requesting SMB changes. New requirements and actual owner dependencies:
> `../descriptor_requirements_20260928/OWNER_PENDING.md`. Historical census counts
> are not a fresh live check or proof of complete admitted-runtime compliance.

## What are we building?
**Akki** is an autonomous system that:
1. Safely connects to a client's **entire data estate** (databases, cloud storage, archives),
2. Takes a **read-only census** of what's there (how many databases, tables, rows, files — never the raw content),
3. Then **extracts and serves governed answers** on top of it,
4. With **proof at every step**, strict **per-client separation**, and a rule that the
   "brain" pod **never touches raw data directly** — it only directs admitted workers.

## How much is built? **≈ 35% built *and proven*.**
There are two layers, and it helps to separate them:

1. **The safety + control system** (permissions, billing limits, tamper-proof logs,
   governance) — **roughly half of all requirements are coded**. This is the hard,
   invisible plumbing that keeps Akki safe and auditable.
2. **Proof that it works on *real* data** — until last week this was **~0%**: everything
   had only been tested with fake/synthetic data. **This week we crossed the biggest
   hurdle** — Akki now genuinely reads your real estates.

Blending "built" with "proven where it counts", we're about **one-third of the way** to a
finished, proven Akki.

## What we proved this week (real, not a demo)
| Estate | How | What Akki read (read-only, counts only) |
|---|---|---|
| **RMS databases** | via your **Jump Server** | **20 databases, ~1,015 tables, ~256 million rows** across 6 servers |
| **DigiCow** (Aurora cloud DB) | AWS RDS Data API (your key) | **digicow_live + ndume: 239 tables, ~5.9 million rows** |
| **RMS cloud storage** (Huawei OBS) | S3-compatible API (your key) | **all 106 storage buckets listed** |

All read-only, counts only, kept separate per client, each with a proof receipt.

## What's remaining (≈ 65%), and what each part is
We've built the safe "reading machine" **and proven it reads**. What's left is:
(a) plug in the **last data source** (NAS recordings), and
(b) turn the **built-but-unproven AI features** into **proven-on-real-data** features.

The remaining work splits into 8 buckets. The % is **that bucket's share of the work
still left**:

| Remaining work bucket | Share of what's left | Plain meaning |
|---|---|---|
| **Rules & decision engines** | **25%** | The largest area. Part of it is *blocked because we're missing some of your specification documents* (24 requirements) + a few threshold decisions only you can set (5). |
| The core promise: reliable, certainty-scored answers | 17% | Making Akki's answers dependable and self-rated for confidence, proven on real data. |
| Governance, security & safety guardrails | 15% | Coded; needs to be *exercised and proven* under real runtime, not just static. |
| Running the AI models well (quality + context) | 12% | Feeding the right context and proving output quality on real jobs. |
| Billing, entitlements & commercials | 8% | Charging + rights per client/model, proven off real usage (not ledger fixtures). |
| Users, tenants & business continuity | 7% | Multi-client accounts + safe restart/handover. |
| **Connecting & reading data estates** | **~5% (was 13%)** | *Mostly done this week.* Left: NAS recordings + deeper object/row counts. |
| Memory & continuous learning | 4% | Akki remembering and improving over time. |

## What's blocking the last connection bits (needs you, not code)
- **NAS recordings**: turn on **SMB/CIFS** on the Synology NAS (or send the SMB password).
  SMB ports are reachable from the jump; the account just fails SMB logon right now.
- **artists_app database**: one MySQL **GRANT** for the census account at the jump's IP,
  and that 7th server joins the census automatically.
- ✅ **DigiCow AWS key** and ✅ **Huawei OBS key**: received and working.

## One-line summary
> The safe reading machine is built and — as of this week — **proven** on your real RMS
> databases, DigiCow, and cloud storage. About a third of the whole product is done. The
> remaining two-thirds is mostly turning already-coded AI/governance features into
> features **proven on your real data**, plus recovering a few of your spec documents and
> flipping on the NAS share.
