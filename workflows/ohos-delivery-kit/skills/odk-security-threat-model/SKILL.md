---
name: odk-security-threat-model
description: "Use when a change touches security/privacy/compliance and needs threat-model.md (STRIDE + regulatory checks). Bypass skill, triggered by proposal's security/permission dimension. Zero plugin dependencies."
license: MIT
---

# ODK Security Threat Model

## Key Rules

- Use for high-risk changes that involve security, privacy, or compliance requirements
- STRIDE analysis must be grounded in actual data flows identified from code/spec
- Each threat must have a verifiable mitigation strategy traceable to a Task
- Compliance gaps must be documented with remediation plans

## Prerequisites

- `proposal.md` exists and change meets trigger conditions (see below)
- `spec.md` exists with acceptance criteria and business rules
- Preferably `design.md` exists for architecture context

## Trigger Conditions

Run this skill when `proposal` 的 `安全/权限` 维度 = 「是」 **且** 命中任一高风险判据，**或** 用户显式调用：

| Category | Trigger Condition |
|----------|-------------------|
| **Single-source trigger + high-risk** | `proposal.md` `安全/权限` dimension = "是" **AND** any high-risk criterion below is met |
| **Sensitive Data** | Involves user data (PII), biometrics, location, contacts, payment info |
| **Network Exposure** | Adds network interfaces, remote APIs, cloud sync, external connectivity |
| **Auth/Authz Changes** | Modifies authentication, authorization, permission models |
| **Compliance Requirements** | Involves GDPR, personal information protection law, data export |
| **Critical Infrastructure** | Changes to security-critical components (kernel, security framework) |
| **Explicit Call** | User explicitly invokes `/odk-security-threat-model` (bypasses the high-risk gate) |

> `安全/权限` = "是" without a high-risk signal stays at the `安全基础检查` level in `design.md`; only the high-risk combination escalates to a standalone `threat-model.md`. Each threat's mitigation must be traceable to a `spec.md` AC / `execution-plan.md` Task.

## Input

1. Read `proposal.md` to understand change scope, impact, and security dimensions
2. Read `spec.md` to identify security-relevant ACs and business rules
3. Read `design.md` (if exists) for architecture context and data flows
4. Analyze codebase to identify:
   - External entities, processes, data stores, data flows
   - Trust boundaries (user/kernel, sandbox, SELinux domains, network)
   - Security controls (authentication, authorization, encryption)

## Steps

1. **Trigger Verification**:
   - Verify change meets trigger conditions
   - If not met, suggest using base security check in `design.md` instead and ask for confirmation

2. **Data Flow Analysis**:
   - Identify all external entities (users, external systems, services)
   - Identify all processes (components, modules, services)
   - Identify all data stores (databases, files, memory regions)
   - Identify all data flows (IPC, network, local calls)
   - Map trust boundaries with clear annotations

3. **STRIDE Analysis**:
   - Apply STRIDE to each DFD element type:
     - **External Entity**: Spoofing, Repudiation
     - **Process**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege
     - **Data Store**: Tampering, Information Disclosure, Denial of Service
     - **Data Flow**: Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service
   - For each applicable threat, document:
     - Threat scenario (concrete attack description)
     - Impact (High/Medium/Low)
     - Likelihood (High/Medium/Low)
     - Existing controls (what already mitigates this)
     - Recommended controls (what should be added)
     - Priority (P0/P1/P2 based on risk)
     - Associated AC/Task for traceability

4. **Compliance Check**:
   - Check against security regulations checklist:
     - **个人信息保护法**: 最小必要、知情同意、匿名化、用户权利
     - **数据安全法**: 数据分类分级、数据出境安全
     - **网络安全法**: 等级保护、关键信息基础设施
     - **GDPR**: Lawful Basis, Data Subject Rights, DPIA
   - Document compliance status (✅ compliant, ⚠️ partial, ❌ non-compliant)
   - For gaps, document remediation measures

5. **Generate Threat Model Document**:
   - Read template from `{{ASSET_ROOT}}/templates/ai/threat-model.md`
   - Generate comprehensive threat model document per template
   - Include Mermaid DFD diagrams, STRIDE analysis tables, compliance matrix

## Output

Write to `.codespec/changes/<id>/threat-model.md`

Report summary to user:
- Number of threats identified by priority (P0/P1/P2)
- Compliance status with any gaps
- Recommendations for next steps

Suggest integration:
- High priority threats should be added to `design.md` "风险与缓解" section
- Compliance requirements should be reflected in `spec.md` ACs
- Mitigation tasks should be tracked in `execution-plan.md`

## Template Reference

Base template: `{{ASSET_ROOT}}/templates/ai/threat-model.md`

## STRIDE Quick Reference

| Threat Type | Description | DFD Element | Key Questions |
|-------------|-------------|-------------|---------------|
| **Spoofing** | Attacker impersonates legitimate entity | External Entity, Process, Data Flow | How is caller identity verified? |
| **Tampering** | Unauthorized modification of data/code | Data Store, Data Flow, Process | How is data integrity protected? |
| **Repudiation** | User denies their actions | External Entity, Process, Data Flow | How are non-repudiable audit logs maintained? |
| **Information Disclosure** | Sensitive info exposed to unauthorized parties | Data Store, Data Flow, Process | What data needs encryption? Access controls? |
| **Denial of Service** | Service availability compromised | Process, Data Store, Data Flow | How are resource consumption and abuse limited? |
| **Elevation of Privilege** | Attacker gains higher privileges | Process, Data Flow | How are privilege escalation paths prevented? |
