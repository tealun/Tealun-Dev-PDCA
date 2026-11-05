# Specialized Audits

Load the relevant section for AI/prompt security, maintainability, or documentation governance.

## AI and Prompt Security

When user-controlled data reaches an LLM or model output affects tools, storage, or later prompts, trace:

1. input entry, identity, tenant, length, and accepted format;
2. prompt/message assembly and instruction/data separation;
3. retrieved-context authorization and tenant scoping;
4. model output schema, enums/ranges, and failure handling;
5. storage of raw versus validated fields;
6. re-injection of stored content into later prompts;
7. execution surfaces such as SQL, templates, shell, eval, URLs, or files;
8. tool allowlist, parameter validation, confirmation boundaries, and least privilege;
9. logging/redaction and cross-user exposure.

Schema validation is a control, not an automatic proof of safety. Closed enums constrain values; free strings, URLs, identifiers, nested objects, and tool arguments still require contextual validation. Confirm the reachable chain before reporting injection or exfiltration.

## Maintainability and Boundaries

Default structural findings to P1 or P2 unless they directly cause a severe runtime failure.

Check:

- cross-layer reach-in: UI to DB, route to embedded domain logic, helpers with hidden I/O;
- responsibility leakage and hidden coupling through globals/singletons/side effects;
- functions or modules owning unrelated concerns;
- duplicated hardcoded config and shotgun edits for one feature;
- upgrade traps: internal library imports, deprecated APIs, unmanaged patches, unsafe version policy;
- contract drift among implementation, callers, schema, and docs;
- speculative abstractions, one-implementation interfaces, needless wrappers/factories;
- deep nesting, long parameter lists, premature caching, or complexity without a current requirement.

A maintainability finding needs a concrete location and change-cost/risk explanation. Recommend the smallest simplification that clarifies ownership; do not fix over-engineering by adding another abstraction.

## Documentation Governance

For document-status or consistency reviews:

1. map documentation files, their claimed status, and intended authority;
2. identify the real source of truth for product behavior, schema, routes, operations, and task status;
3. verify claims against code/configuration and recent changes—headers alone are not evidence;
4. classify blocks as current, outdated, duplicated, unique, or unverifiable;
5. report conflicts with the authoritative version and recommended destination;
6. edit/reorganize documents only when requested, preserving useful unique content and links.

For migrations or production status, local files may prove intended state but not applied state. Require actual environment evidence before marking deployment or migration complete.

When decomposing a junk-drawer document, first map overlap, then move unique content to the correct authoritative destination, repair links, and delete the original only if the user asked for the reorganization and no unique content is lost.
