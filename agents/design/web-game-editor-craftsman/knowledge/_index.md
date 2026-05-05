# Knowledge Index — Web Game Editor Craftsman

Lazy-loaded references. Do not read all at once; consult per-task.

## Editor patterns

- [editor-runtime-contract.md](editor-runtime-contract.md) — How an editor and its runtime consumer should agree on a store schema; migration helpers; example: gpc xRel migration.
- [single-source-property-pane.md](single-source-property-pane.md) — When to hide legacy fields, when to keep both; toggle UX patterns.
- [dirty-state-ux.md](dirty-state-ux.md) — markDirty / markClean wiring, dirty pill, tab title prefix, beforeunload.
- [live-preview-hotapply.md](live-preview-hotapply.md) — storage event, postMessage protocol, debounce, iframe sync.
- [test-page-pattern.md](test-page-pattern.md) — dedicated <editor>-test.html shape; status overlay; what to surface.
- [cache-busting.md](cache-busting.md) — `?v=N` bump rules; SW cache traps; user-visible version tag.

## Reference projects

- [reference-figma-editor-ux.md](reference-figma-editor-ux.md) — Property pane consolidation patterns from Figma's Inspector.
- [reference-storybook-controls.md](reference-storybook-controls.md) — Storybook addon-controls dirty/reset pattern.
- [reference-codesandbox.md](reference-codesandbox.md) — CodeSandbox iframe live preview architecture.

## Host project (golf-paper-craft) specifics

- [host-gpc-editors.md](host-gpc-editors.md) — UI editor, course editor, level editor, asset browser; submodule layout; editorSync=1 protocol.
- [host-gpc-store-keys.md](host-gpc-store-keys.md) — All localStorage keys the editors persist (gpc_ui_overrides, gpc_course_overrides, etc.).
