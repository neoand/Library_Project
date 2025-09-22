# Recommendations for Future Odoo 18 Module Development

This document provides a set of universal best practices and guidelines for Large Language Models (LLMs) when developing new Odoo 18 modules. These recommendations are based on key lessons learned from building robust, scalable, and maintainable applications on the platform.

---

## 1. Core Architectural Principle: Favor Standalone Models

**Guideline:** Avoid inheriting from complex, high-level Odoo models (e.g., `product.product`, `sale.order`) unless the new module's domain is a direct and complete extension of the base model.

**Default Approach:** Create a standalone model (`_name = 'your.new.model'`) and inherit only from essential mixins like `mail.thread` and `mail.activity.mixin` for communication and tracking features.

**Justification:**
- **Performance:** Prevents significant overhead from unnecessary database joins and loading of irrelevant fields.
- **Simplicity & Maintainability:** Leads to a cleaner, more focused codebase with fewer dependencies, reducing the risk of conflicts during Odoo upgrades or when installing other modules.
- **Domain Clarity:** Ensures the model's schema is perfectly tailored to its specific business purpose.

---

## 2. Naming Conventions and Code Structure

**Guideline:** Follow Odoo's standard naming conventions to ensure consistency and readability across the platform.

- **Model Names (`_name`):** Use singular nouns, separated by dots (e.g., `project.task`, `account.invoice`).
- **File Names:** Python files in `models/` should match the model name (e.g., `project_task.py`). XML files in `views/` should be descriptive (e.g., `project_task_views.xml`).
- **XML IDs:** Use the format `<module_name>.<record_id>` (e.g., `library_app.action_library_book`). View IDs should follow `<model_name>_view_<view_type>` (e.g., `res_partner_view_form`).
- **Variable Names:** Use clear, descriptive names in Python (e.g., `active_loans` instead of `als`).

---

## 3. UI/UX Best Practices

### 3.1. Professional Menu Structure

**Guideline:** Always structure module menus hierarchically to separate daily tasks from configuration.

**Standard Structure:**
```
Your App/
├── Operations      (For day-to-day transactional records)
├── Catalogs        (For master data like contacts, products, etc.)
└── Configuration   (For settings that are rarely changed)
```
- Use the `sequence` attribute to control the order logically. This creates an intuitive user experience consistent with Odoo's native modules.

### 3.2. Robust UI Cleanup with CSS

**Guideline:** When a dependency module adds unwanted UI elements to a view, the preferred method for removal is **CSS**, not XML `xpath`.

**Process:**
1.  Create a dedicated CSS file (e.g., `static/src/css/custom.css`).
2.  Register it in the `web.assets_backend` section of `__manifest__.py`.
3.  Use a specific CSS selector to hide the element with `display: none !important;`.

**Justification:**
- **Stability:** CSS selectors are more resilient to changes in view architecture and are not affected by user security groups, which can make `xpath` expressions fail.
- **Centralization:** Keeps all style modifications in one place.

---

## 4. Modern Odoo 18 View and Code Patterns

**Guideline:** Adhere to the latest Odoo 18 conventions for cleaner and more efficient code.

- **Chatter:** Use the simplified `<chatter/>` tag.
- **View Modes:** Specify `view_mode="list,form,kanban"` (use `list` instead of the deprecated `tree`).
- **Dynamic Attributes:** Use direct attributes like `invisible="state == 'draft'"` instead of the older `attrs` dictionary.
- **File Structure:** Strictly separate concerns: `models/`, `views/`, `security/`, `data/`. Create separate files for actions (`*_action.xml`) and menus (`*_menu.xml`).

---

## 5. Performance and Security

### 5.1. Performance First

**Guideline:** Always consider performance when creating computed fields.

- **`store=True` is Essential:** If a computed field is used for filtering, grouping, searching, or is displayed in a list/kanban view, it **must** have `store=True`.
- **Precise `@api.depends()`:** Ensure the `depends` decorator is as specific as possible to avoid unnecessary recomputations.

### 5.2. Security by Default

**Guideline:** Do not grant universal access. Define clear security groups and access rights.

- **`ir.model.access.csv`:** Define baseline permissions (read, write, create, unlink) for different groups. Start with the least privilege necessary.
- **Record Rules:** Use record rules (`ir.rule`) to implement row-level security (e.g., users can only see their own documents).
- **Security Groups:** Create custom groups in `security/security.xml` for different roles within the module.

---

## 6. Workflow and Documentation

**Guideline:** Development is not complete until the documentation is updated.

- **Use Automation Scripts:** Leverage scripts like `./start_odoo.sh` and `./dev_tools.sh` to streamline the development workflow.
- **Document Decisions:** For any significant architectural change, create a new entry in `ARCHITECTURE_DECISIONS.md`.
- **Update the Changelog:** Add clear, user-friendly entries to `CHANGELOG.md` for every new feature or fix.
- **Update these Instructions:** If a new, critical best practice is discovered, update this `RECOMMENDATIONS.md` file.
