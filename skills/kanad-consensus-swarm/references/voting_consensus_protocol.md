# 🗳️ Voting Consensus Protocol & State Machine Specification

## 1. Executive Overview
The **Kanad Voting Consensus Protocol** provides a verifiable, non-sycophantic decision-making state machine for autonomous multi-agent teams. It prevents premature execution, catches architectural blind spots, and guarantees that every agent explicitly defends its vote using domain-specific criteria.

---

## 2. The 5-Phase Consensus Lifecycle

```
[Phase 1: Plan Authoring]
       │
       ▼
[Phase 2: Formal Voting & Balloting]
       │
  ┌────┴────┐
  │         │
  ▼         ▼
[Passed]  [Rejected / Amend] ──► (Return to Phase 1)
  │
  ▼
[Phase 3: Authorized Implementation]
  │
  ▼
[Phase 4: Independent Forensic Verification]
  │
  ┌────┴────┐
  │         │
  ▼         ▼
[Passed]  [Defects Flagged] ──► (Worker Patches & Resubmits)
  │
  ▼
[Phase 5: Managerial Sign-Off & Delivery]
```

---

## 3. Formal Ballot Schema

Every voting agent must post its vote publicly on the shared board using the exact schema:

```markdown
@manager @worker @analyser @coordinator
🗳️ [ROLE] VOTE: [YES / APPROVE | NO / REJECT | AMEND] on [PLAN-ID]

Domain Evaluation:
1. Criterion A (Scope / Feasibility / Reality): [Detailed assessment]
2. Criterion B (Safety / Data Integrity): [Detailed assessment]
3. Criterion C (User Value & Pedagogical Clarity): [Detailed assessment]

Verdict: [Final statement of clearance or required modifications]
```

---

## 4. Majority Rules & Deadlock Arbitration

| Decision Type | Threshold | Voting Quorum | Deadlock Resolution Rule |
| :--- | :---: | :--- | :--- |
| **Operational Evolutions** (MOC updates, styling, new notes) | **2/3 Majority** | All 3 members present | If 1 NO, 2 YES: Approved. Dissenting agent's technical concerns must be addressed in execution. |
| **Structural / Deletive Actions** (Vault re-structuring, schema changes) | **3/3 Unanimous** | All 3 members present | If 1 NO: Plan is blocked immediately. Manager must revise scope until unanimous. |
| **Emergency Patches** (Fixing broken links, correcting bad data) | **2/3 Fast-Track** | Worker + Analyser or Manager + Worker | Rapid execution followed by retro-active verification. |

---

## 5. Dispute Resolution & Anti-Sycophancy Gate

To prevent sycophancy ("I agree with everything Manager said"):
1. **Mandatory Domain Substantiation:** A vote with just "YES, looks good" is disqualified by the Analyser as invalid. Every vote must state at least two concrete technical or architectural reasons.
2. **The Analyser Veto Power:** The Analyser holds absolute veto power on questions of **data loss**, **broken links**, and **hardware safety**. If the Analyser votes NO due to a verifiable regression or fill-rate hazard, the plan cannot pass regardless of Manager and Worker approval.