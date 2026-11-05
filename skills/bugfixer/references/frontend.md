# Frontend and Product Bugs

Use this reference for screenshots, layout, interaction, theming, role/view, or client-state defects.

## Visual and Intent Checks

- Compare the implementation to the user's screenshot or latest description.
- Identify what must remain unchanged and which visual layer may change.
- Separate owner/admin/current-user views from visitor/public views.
- Check safe areas, status bars, notches, bottom bars, popups, drawers, fixed panels, overlays, and z-index.
- Prefer existing tokens and theme variables over hardcoded colors.
- Hide unconfigured optional content instead of displaying misleading demo business data.
- Do not mix public presentation with internal navigation or management controls unless intended.

## Interaction and State

- Search displayed text, event names, route names, and request helpers with `rg`.
- Inspect markup, styles, state initialization, handlers, disabled state, and overlays together.
- A visible button may be covered; verify hit area before assuming the handler is absent.
- For role-specific controls, prove the condition from actual identity, owner flags, route state, or auth state.
- For custom settings, verify application and persistence: save, reload, re-enter edit, and view every affected surface.
- For uploads, check type/size validation, upload result, persisted URL, reload display, and cleanup behavior.
- Distinguish retry noise from multiple root causes when one action creates several console errors.

## Mini Program Checks

- Check page-versus-component event scope, WXML/WXSS support, capsule/status-bar spacing, bottom tab overlap, and safe-area padding.
- Verify fixed panels do not cover content and hide when role-specific behavior requires it.
- Confirm runtime config, ext config, global data, local storage, cached builds, and backend flags when demo state persists.

## Verification

- Run syntax or config parsing checks for touched files.
- Inspect the exact component/page and affected state path.
- Compare the changed layer against the acceptance screenshot or description.
- For persistence, save, reload, reopen edit, and view the consumer/public page.
- Search for rejected copy, controls, routes, and stale fallback content.

Do not use a green build as proof of visual fidelity or correct role behavior.

