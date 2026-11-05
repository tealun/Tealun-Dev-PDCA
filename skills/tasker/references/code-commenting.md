# Code Commenting Gate

Loaded from Tasker's Conditional References for comment-focused development-code work.

Use this gate only for development-code work that asks to add comments, add documentation-style explanations, or improve maintainability/readability through comments. Before execution, sample the target files and record in the execution contract: the project's primary developer-facing language, existing comment style, comment density, and the user's maintainability expectation. Unless the user requests otherwise, new comments must use the project's primary developer-facing language.

For comment-focused work, do not satisfy the task with scattered inline notes. Prefer concise, human-maintainer entry points at the module, class, method, and function level, covering responsibility, inputs and outputs, key business constraints, boundary conditions, side effects, permissions/security/tenant semantics, and intentional tradeoffs when relevant. Use inline comments only for non-obvious logic inside an implementation. Do not use English or mechanically fragmented comments as a substitute for maintainable method-level explanations when the project faces developers in another language.

If the evidence shows the user expects a systematic readability improvement, plan and verify the work by file or coherent batch before editing. Do not casually pick a few code points to annotate and call the request complete.
