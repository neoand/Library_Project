# Recommendations for Future Odoo 18 Module Development

This document provides a set of best practices and guidelines for Large Language Models (LLMs) when developing new modules for this Odoo 18 project. These recommendations are based on the key lessons learned during the development and refactoring of the `library_app` module.

---

## 1. Core Architectural Principle: Favor Standalone Models

**Guideline:** Avoid inheriting from complex, high-level Odoo models like `product.product` or `sale.order` unless the new module's domain is a direct and complete extension of the base model.

**Default Approach:** Create a standalone model (`_name = 'my.new.model'`) and inherit only from essential mixins like `mail.thread` and `mail.activity.mixin`.

**Justification (See `ADR-001`):**
- **Performance:** Prevents significant performance overhead from unnecessary database joins and field loading. The `library_app` module saw a 77% performance improvement after removing `product.product` inheritance.
- **Simplicity & Maintainability:** Results in a cleaner, more focused codebase with fewer dependencies. This reduces the risk of conflicts during Odoo upgrades or when installing other modules.
- **Domain Clarity:** Ensures the model's schema is perfectly tailored to its specific business purpose, without irrelevant fields.

---

## 2. UI/UX Best Practices

### 2.1. Professional Menu Structure

**Guideline:** Always structure module menus hierarchically to separate daily tasks from configuration.

**Standard Structure (See `ADR-002`):**
```
Your App/
├── Operations      (For day-to-day records like books, loans)
├── Catalogs        (For master data like authors, categories)
└── Configuration   (For settings that are rarely changed like stages, types)
```
- Use `sequence` attributes to control the order logically.
- This creates an intuitive user experience consistent with Odoo's native modules.

### 2.2. Robust UI Cleanup with CSS

**Guideline:** When a dependency module adds unwanted UI elements (e.g., buttons, fields) to a view, the preferred method for removal is CSS, not XML `xpath`.

**Process (See `ADR-003`):**
1.  Create a dedicated CSS file (e.g., `static/src/css/custom.css`).
2.  Register it in the `web.assets_backend` section of `__manifest__.py`.
3.  Use a specific CSS selector to hide the element with `display: none !important;`.

**Justification:**
- **Stability:** CSS selectors are more resilient to changes in view architecture and are not affected by user security groups, which can make `xpath` expressions fail.
- **Centralization:** Keeps all style modifications in one place.

---

## 3. Modern Odoo 18 View and Code Patterns

**Guideline:** Adhere to the latest Odoo 18 conventions for cleaner and more efficient code.

- **Chatter:** Use the simplified `<chatter/>` tag instead of the old `<div class="oe_chatter">...</div>` structure.
- **View Modes:** Specify `view_mode="list,form,kanban"` instead of the deprecated `tree`.
- **Dynamic Attributes:** Use direct attributes like `invisible="state == 'draft'"` instead of the older `attrs="{'invisible': [('state', '=', 'draft')]}"`.
- **File Structure:** Strictly separate concerns:
    - `models/`: Python logic.
    - `views/`: All XML UI definitions. Create separate files for actions (`*_action.xml`) and menus (`*_menu.xml`).
    - `security/`: Access rights (`ir.model.access.csv`) and rules.
    - `data/`: Initial or demo data.

---

## 4. Performance First

**Guideline:** Always consider performance when creating computed fields.

- **`store=True` is Essential:** If a computed field is used for filtering, grouping, searching, or is displayed in a list/kanban view, it **must** have `store=True` to avoid severe performance degradation.
- **Precise `@api.depends()`:** Ensure the `depends` decorator is as specific as possible to avoid unnecessary recomputations.

---

## 5. Workflow and Documentation

**Guideline:** Development is not complete until the documentation is updated.

- **Use the Scripts:** Leverage `./start_odoo.sh` and `./dev_tools.sh` to streamline the development workflow.
- **Document Decisions:** For any significant change, create a new entry in `ARCHITECTURE_DECISIONS.md`.
- **Update the Changelog:** Add clear, user-friendly entries to `CHANGELOG.md` for every new feature or fix.
- **Update these Instructions:** If a new, critical best practice is discovered, update this `RECOMMENDATIONS.md` file.
