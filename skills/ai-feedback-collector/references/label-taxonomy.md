# Label Taxonomy

Use these values as the canonical starting point. Add a new lowercase kebab-case value only when none of the existing labels fit.

## `tool`

- `opencode`
- `cursor`
- `claude-code`
- `chatgpt`
- `copilot`
- `internal-agent`
- `office-assistant`
- `search-assistant`
- `unknown`

## `category`

Use this family for root problem classification and improvement statistics. Prefer one primary category in the report, with optional secondary categories.

- `model-capability`
- `environment-tooling`
- `business-context-clarity`
- `workflow-process`
- `user-skill-training`
- `data-permission`
- `safety-compliance`
- `unknown`

### Category Definitions

- `model-capability`: The AI failed at reasoning, planning, context management, instruction following, code understanding, tool-use decisions, or recovery after errors.
- `environment-tooling`: The problem is likely caused by local environment, dependencies, IDE/CLI behavior, build/test setup, network, command availability, or tool integration reliability.
- `business-context-clarity`: The task lacks clear business goals, product rules, domain concepts, acceptance criteria, edge cases, or expected behavior.
- `workflow-process`: The team's AI-assisted R&D process needs improvement, such as task decomposition, review gates, verification strategy, rollback/checkpointing, or handoff.
- `user-skill-training`: The user likely needs better prompting habits, context packaging, AI collaboration patterns, or output verification practices.
- `data-permission`: The AI cannot access required repositories, files, documents, logs, credentials, private knowledge, or runtime data.
- `safety-compliance`: The issue involves privacy, security, compliance, unsafe code changes, production risk, or irreversible actions.
- `unknown`: The report does not contain enough evidence for responsible classification.

## `scenario`

- `coding`
- `writing`
- `search`
- `data-analysis`
- `design`
- `office-work`
- `customer-support`
- `meeting`
- `learning`
- `automation`
- `unknown`

## `task`

- `bug-fix`
- `feature-dev`
- `api-change`
- `refactor`
- `test`
- `documentation`
- `code-review`
- `planning`
- `summarization`
- `translation`
- `data-cleaning`
- `report-generation`
- `question-answering`
- `unknown`

## `workflow-stage`

- `requirements`
- `planning`
- `implementation`
- `verification`
- `implementation-and-verification`
- `review`
- `deployment`
- `handoff`
- `unknown`

## `issue`

- `wrong-understanding`
- `hallucination`
- `wrong-file-edit`
- `wrong-tool-use`
- `tool-call-error`
- `repeated-failure`
- `poor-context-use`
- `unclear-business-requirement`
- `missing-acceptance-criteria`
- `missing-domain-context`
- `environment-setup-failure`
- `missing-clarification`
- `ignored-instruction`
- `bad-output-quality`
- `formatting-error`
- `slow-response`
- `excessive-cost`
- `unsafe-action`
- `privacy-risk`
- `permission-error`
- `environment-error`
- `integration-error`
- `unknown`

## `capability`

- `planning`
- `reasoning`
- `coding`
- `context-management`
- `tool-use`
- `instruction-following`
- `memory`
- `communication`
- `retrieval`
- `safety`
- `unknown`

## `severity`

- `low`
- `medium`
- `high`
- `critical`
- `unknown`

## `frequency`

- `once`
- `occasional`
- `frequent`
- `systemic`
- `unknown`

## Suggested Routing Values

- `product experience`
- `model capability`
- `tool integration`
- `environment setup`
- `business analysis`
- `prompt/workflow design`
- `permissions/data access`
- `documentation/training`
- `safety/compliance`
- `unknown`

## Category Examples for AI-Assisted R&D

Use `category:model-capability` for feedback like "the agent edited unrelated files", "it kept repeating the same failed fix", "it hallucinated an API", or "it ignored a clear instruction."

Use `category:environment-tooling` for feedback like "tests cannot run because dependencies are missing", "the tool cannot call the terminal", "the IDE plugin loses connection", or "commands work locally but not inside the agent environment."

Use `category:business-context-clarity` for feedback like "we do not know how to describe the business rule", "the acceptance criteria are unclear", "the AI implemented technically correct code but not the desired product behavior", or "domain terms were not explained."

Use `category:workflow-process` for feedback like "the task was too large for one AI session", "nobody reviewed the AI's change before merge", "there was no test plan", or "handoff between human and AI was unclear."

Use `category:user-skill-training` for feedback like "the user did not know what context to provide", "the prompt was too vague", or "the user expected a finished answer without checking assumptions."

Use `category:data-permission` for feedback like "the AI needed logs but could not access them", "the repository was incomplete", "private documentation was unavailable", or "credentials/permissions blocked verification."

Use `category:safety-compliance` for feedback like "the AI exposed sensitive data", "it attempted an unsafe production action", or "the output violated security or compliance requirements."

## Severity Calibration

Use `critical` when the report mentions or strongly implies data loss, security exposure, privacy exposure, production outage, compliance risk, irreversible unsafe action, or broad business impact.

Use `high` when the issue blocks task completion, causes major rework, affects several people, or repeatedly prevents a team workflow from completing.

Use `medium` when the issue creates noticeable friction, repeated manual correction, or quality concerns, but the user can still recover.

Use `low` when the issue is cosmetic, mildly inconvenient, or has an obvious workaround.

Use `unknown` when the impact cannot be estimated from the description.
