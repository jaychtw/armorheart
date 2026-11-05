# AI Collaboration & Continuity Protocol (AICP)

**Version:** 1.2.1  
**Status:** Adopted collaboration baseline  
**Applies to:** AI-assisted game and application development adopting this protocol  
**Owner:** Human product owner / creative director  
**Date:** 2026-10-31

## 1. Purpose and boundaries

Preserve durable design intent, decision rationale and accountable delivery across ChatGPT conversations and AI agents. This protocol governs *collaboration and knowledge continuity*, not gameplay acceptance. UGDS governs applicable game quality standards; the product GDD governs project identity and approved functionality. For non-game apps, apply only expressly adopted UGDS provisions.

**Core rule:** Memory enables familiarity; project documentation establishes authority; implementation and evidence establish what exists.

No AI may claim complete historical recall, successful document retrieval, or owner approval without evidence. Never substitute inferred recollections for verified records.

## 2. Roles and decision ownership

- **Human owner:** vision, design direction, constraints, scope, budgets, acceptance, release and exceptions.
- **ChatGPT / advisory AI:** challenge assumptions, surface tradeoffs and blind spots, maintain decision clarity, create actionable briefs and review evidence.
- **Codex / implementation AI:** assess feasibility and counterpropose during Offer; implement within approved boundaries after commitment, test, document and report deviations and limitations.
- **GitHub:** versioned source of truth for project specifications, decisions, implementation and evidence.

AI agents must not reinterpret delivery as approval. Material scope or gameplay changes, visual direction, costs, external services, deployment, security/privacy impacts or standards exceptions require owner approval. Routine implementation details need not interrupt work.

## 3. Authority, conflicts and evidence

Apply law, safety and platform policy first. For product intent, prefer the owner's latest *explicitly approved* decision, as recorded in project GDD/decision records; then pinned applicable standards and approved briefs. For actual behavior and status, inspect code, builds, tests and deployment evidence. A chat recollection is supporting context, not proof.

Where documentation, conversation, implementation or results disagree:
1. State the conflict and cite the affected records.
2. Distinguish **approved intent**, **implemented behavior**, **verified outcome**, and **unresolved questions**.
3. Never silently choose or rewrite a decision; request owner resolution when material.

Pin the UGDS version by tag or commit SHA as UGDS requires. Pin this protocol by version and preferably commit SHA when reproducibility matters. New standard revisions are not retroactively imposed.

## 4. Context reconstruction on conversation startup

For an existing project:
1. Discover the relevant repository under the owner's GitHub namespace, **https://github.com/jaychtw**, when the precise repository is not supplied. Prefer the connected GitHub integration to enumerate accessible repositories, including authorized private repositories. Do not assume all repositories are accessible to every agent. Check identity using project name, README and repository metadata; do not pick an ambiguous match without verification.
2. Once identified, prioritize its **current approved GDD** and associated design decisions as the record of intended experience, then inspect its README, `PROJECT_STATE.md` if present, current GDD, decision records, standards pins, key verification reports and relevant changes.
3. Review this protocol, the applicable UGDS and available project templates.
4. Recover relevant ChatGPT Project conversations when accessible; explicitly distinguish confirmed history from partial memories and inference.
5. Summarize verified phase/status, frozen decisions, known risks and next open question briefly; then follow the owner's instruction.
6. If GitHub or past conversations are inaccessible, declare that limitation. Do not invent missing content or needlessly demand a full recap.

For a new project, establish the scope and governing standards without prematurely restricting exploration. A new conversation per development effort is recommended, not mandatory. If a conversation reaches context limits, use a documented handoff.

## 5. Decision preservation

Record *material* decisions in the project's GDD or decision log, noting:
- identifier/date, decision and status (**proposed**, **approved**, **superseded**, **rejected**, **deferred**);
- rationale and significant alternatives considered;
- consequences, constraints and references to supporting evidence;
- owner approval and superseding decision, when applicable.

Do not mistake brainstorming, agent recommendations or generated files for approved choices. Do not reopen settled decisions absent changed evidence, changed circumstances or an explicit request.

Update `PROJECT_STATE.md` at meaningful milestones or after decisions that change project direction. It is an **index and snapshot**, not a second GDD. Avoid copying entire specifications into it. Keep it compact and link to authoritative files. Treat stale or contradictory state as a review issue, not truth.

## 6. Work and quality gates

Distinguish **Explore → Offer → explicit commitment gate → Execute → Confirm & Close → separate deployment approval**, as detailed in §6.1. Never collapse these gates. Passing automated tests is not proof of visual quality, user experience or public readiness.

Implementation briefs must contain objective, constraints, authoritative sources, in/out of scope, acceptance tests, evidence requirements, escalation thresholds and stopping conditions. Codex may choose low-impact technical approaches; report design-affecting deviations before implementing them.

On completion, review changes and evidence independently where practical. Label tests as reported, independently reproduced, not verified or failed. Release requires separate authorization.

### 6.1 Commitment Cycle: Explore → Offer → Execute → Confirm & Close

Use the Commitment Cycle as a **proportionate collaboration framework**, not four mandatory ceremonies for every trivial change. The human owner retains creative, budget, acceptance and release authority throughout.

1. **Explore — discover intent.** The owner and advisory AI brainstorm, challenge assumptions, compare alternatives and converge toward a candidate GDD or change proposal. Mark uncertainties, risks and unresolved decisions. A draft GDD is not yet an implementation authorization.
2. **Offer — establish a feasible commitment.** Invite Codex to inspect the actual repository, pinned standards, tools and constraints *before committing to uncertain implementation*. Codex assesses feasibility, exposes gaps, estimates tradeoffs, proposes alternatives or a bounded technical spike, and states what evidence can be delivered. The advisory AI and owner evaluate the offer and any counteroffers. For routine, well-understood work, this can be a short preflight rather than a separate experiment.
3. **Commitment gate — authorize execution.** Before substantive execution, establish an agreed outcome, scope and exclusions, constraints (including cost and release), decision ownership, acceptance criteria, evidence, and stop/escalation conditions. Owner approval of material changes is required; Codex may decide routine engineering details. A feasibility report or POC does not authorize expanded scope.
4. **Execute — deliver the agreement.** Codex implements the agreed work, verifies it in the actual target environment, preserves reproducible artifacts and reports deviations. Material discoveries trigger a counteroffer or explicit return to Offer rather than a silent quality downgrade.
5. **Confirm & Close — owner judges evidence.** Separate technical verification from human aesthetic/experience acceptance. The owner may accept, conditionally accept, reject, or redirect. Close the *specific commitment* when its agreed criteria are met, even if nonblocking improvements remain; document remaining defects as separate follow-up commitments. Do not conceal failed mandatory criteria through a general acceptance score.

**Diagnostic feedback routing:** Return to Explore if the product intent is wrong; Offer if the approach or feasibility premise is wrong; Execute for a localized implementation defect. Reopen only the necessary stage and preserve accepted baselines. A closure decision is not automatically a release/deployment authorization.

**Evidence-gated feasibility (risk-based):** Use a bounded technical spike/POC when there is material uncertainty about visual quality, technical capability, cost, performance, integrations or production scalability. Specify the question, time/scope boundary, demonstrable artifact, objective checks, human review criteria and stopping point. Record limitations and whether evidence was actually inspected. Avoid speculative process overhead on familiar low-risk changes.

**Continuity:** Record consequential offers, counteroffers, owner commitment/acceptance decisions, accepted baselines and outstanding follow-ups in the project's GDD/decision log and `PROJECT_STATE.md`. Distinguish a *milestone accepted for continued development* from *final production acceptance* and from *permission to merge, publish or deploy*. Preserve project-specific evidence in its own repository, not in the shared standards.

### 6.2 Durable development checkpoints

**Development synchronization is not release authorization.** Codex should use a dedicated working branch as the durable Git-backed record for authorized implementation. A working cloud environment or accessible preview link is not a durable backup.

1. **Start:** Read applicable repository instructions and the adopted AICP; inspect branch state, local modifications, CI/deployment triggers, cost implications and branch protections. Use a designated working branch rather than `main` unless explicitly authorized otherwise.
2. **During work:** Commit and safely push meaningful intermediate checkpoints, especially before long-running or asset-heavy operations. Preserve reproducible editable sources and useful review evidence without indiscriminately committing large generated files.
3. **Before reporting completion:** Run relevant checks, inspect staged changes for secrets and unintended files, check remote divergence, commit and push the final checkpoint, verify the remote commit SHA, and return stable GitHub links and honest test results. Incomplete work may be preserved as clearly labeled WIP, never misrepresented as accepted.
4. **Exceptions:** Do not push when it could trigger unapproved deployment, publication, costs, secret exposure, destructive conflicts or a project-specific prohibition. Do not force-push or silently change workflow/settings. Report the specific blocker and provide an independently durable backup where feasible; a backup only in the same transient workspace is not independent preservation.
5. **Authority:** Safe development-branch checkpoint pushes are routine and preauthorized for implementation work unless the owner specifies local-only work or repository policy prohibits them. Push does not mean owner acceptance, merge, release or deployment; those remain separate gates.

**First-instruction reinforcement:** At each new project, the initial Codex implementation brief must both direct Codex to read the adopted AICP and explicitly state the working-branch, intermediate-checkpoint and final-push requirement. This short reminder complements the governing protocol.

## 7. Handoff, drift and confidentiality

When transitioning conversations, prepare a concise handoff covering project link, source revision, current phase, accepted decisions, rejected/deferred alternatives, reasoning, pending approvals, risks and next action. Link documents rather than replicate them. If not possible, say what was not recovered.

Do not put credentials, personal data, access tokens or sensitive private discussions into repository records. Verify repository visibility and intended audience before adding content. Private repositories are not a substitute for secret management.

Agents must not claim they persist independent memory across sessions. The recoverable record is the documented Git history, not the model's internal recollection.

## 8. Maintenance and amendment

Reusable process lessons belong here, with a version change and changelog entry. Product-specific decisions belong in their individual repositories. Changes to this protocol require owner review; agents should propose improvements without silently modifying the governing baseline.

## 9. Continuous improvement at cycle closure

At a meaningful milestone, finished prototype, abandoned experiment, project pause, or conversation handoff, the advisory AI should **proactively offer or conduct a proportionate retrospective**, using available GDDs, change history, implementation reports and conversation context. The owner should not have to restate established practices or request the review by a special phrase. Do not interrupt active exploration with procedural ceremony.

Examine, as relevant, design fidelity, implementation friction, AI collaboration, quality/evidence gaps and transferability. Separate observed evidence from speculation. Record only consequential lessons and avoid repeating the entire project history.

**Route each lesson by scope:**
- Project-specific design and decisions → project GDD, decision record or `PROJECT_STATE.md`.
- Reusable product-quality or QA requirement → propose a UGDS improvement.
- Reusable AI collaboration, prompting, handoff or decision procedure → propose an AICP improvement.
- Technical repeatable solution → suitable technical template or reference, not automatically AICP.
- Unvalidated hypothesis → a candidate for future evaluation, not a mandatory standard.

**Promotion threshold:** Adopt a universal practice when it addresses a recurring problem, mitigates material risk or has compelling cross-project benefits. Clearly identify the evidence, impact, tradeoffs and applicable scope. Avoid bloating standards with one-off anecdotes, duplicative instructions or speculative requirements. Prefer clarification, simplification or retirement of obsolete rules when warranted.

For low-risk refinements within the owner's standing authorization, an agent may prepare and commit a narrowly scoped, versioned improvement; preserve a reviewable change history and report what changed. Seek explicit approval for substantial new obligations, quality gates, costs, privacy/security changes, or changes affecting adopted project acceptance criteria. Never silently change the pinned standards of existing projects.

Keep the **closing routine lightweight**: (1) summarize consequential lessons, (2) classify their destination, (3) update only justified records, (4) note any unresolved question for the next project. If no transferable lesson emerges, say so and make no standards change. This is an event-triggered practice, not autonomous background monitoring or a promise of persistent internal AI memory.

## 10. Possibility portfolio publication at project lifecycle closure

**Conversation ownership:** The conversation dedicated to a game/app owns its end-of-cycle release evidence and the request to add/update that work in **Possibility** (`jaychtw/jaychtw.github.io`). The Possibility-focused conversation owns shared portal design, navigation, localization, governance and architecture. Routine catalog entries should not require moving conversations. AICP owns reusable cross-project procedure; UGDS does not acquire a portfolio-publication requirement.

**Distinct release gates:** A project being deployed and a Possibility entry being published are separate events and separate repositories. Verify public project deployment before preparing a live card. Neither the project release nor a successful portal CI run automatically authorizes a portal deployment. Follow the **current verified** approval and deployment policy in each repository. Never infer authorization from an old chat, outdated documentation, a test pass or the presence of a publishing workflow. If the owner's explicit authorization covers both releases and the current workflow permits it, execute within that authorization; otherwise request approval at the applicable gate.

**Routine closing sequence (proportionate, no automatic background work):**
1. Verify the independent release's canonical playable/open URL, representative functioning, source repository, release evidence and known limitations. Label unresolved checks honestly.
2. Consult the current Possibility repository's `docs/CATALOG.md`, `docs/MAINTENANCE.md`, release instructions and real metadata schema before editing. Existing portal conventions govern the entry; AICP does not freeze a particular JSON schema or prescribe a new UI.
3. Create/update one stable project entry in the correct collection without duplicating a card; use accurate English/Traditional Chinese copy according to the **current** portal localization contract, approved names, descriptions and tags. Never invent translations, release dates, approval records or maturity claims.
4. Verify the destination link and record actual link evidence as required by the portal contract. Use only owner-approved cover artwork, preserve its title lettering and provenance, and use documented screenshot/neutral fallback if no cover is approved. Never generate artwork or change unrelated cards as a side effect.
5. Make a narrow, reviewable portal change, run relevant build, link, browser, accessibility and language checks, and publish only under the portal's verified release authority. Verify the actual public Possibility entry after deployment. A project repository deployment cannot substitute for this verification.
6. Update the project `PROJECT_STATE.md` or release record with **two independent statuses**: project deployment and Possibility publication (not started / pending approval / deployed-and-verified / blocked), including live URLs and exact commit/deployment references when known. Record a concise handoff and perform the §9 retrospective.

**Scope boundaries:** A routine portal entry must not alter shared design, global translations, filters, governance, legal policies, unrelated assets, other games, or repository licensing. Route any new platform-wide decision to the Possibility workstream. The frozen Possibility v1.2 change request remains a separate, not-yet-executed platform initiative until independently implemented and verified; do not treat it as a currently deployed requirement. Preserve no-expenditure constraints unless the owner expressly changes them.

**Exceptions:** If a game/app is released but not meant for public showcase, mark Possibility publication as deferred rather than manufacturing a card. If the portal is inaccessible, publication is blocked or not verified; produce a concise handoff for later execution instead of claiming completion.

**Governing maxim:** Standardize continuity without standardizing creativity.
