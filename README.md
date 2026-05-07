#  Personal Finance Tracker API

**FastAPI** application designed to manage personal financial records with **MongoDB**. This API provides high-performance transaction tracking, categorization, and deep financial insights through MongoDB’s aggregation framework.

---

## Project Architecture

The project follows a modular structure to ensure scalability, clean code, and separation of concerns:

- **`Tracker/database/`**: Handles MongoDB connections and programmatic index initialization via Motor.
- **`Tracker/Routes/`**: Contains modularized endpoints for transactions and categories.
- **`Pydantic_Models.py`**: Centralized data validation using Pydantic v2 (separate schemas for Input/Output).
- **`main.py`**: The application entry point and lifecycle management.

---

##  Key Features

*   **Advanced Filtering**: Multi-parameter search (date ranges, tags, categories) with reusable pagination logic.
*   **Monthly Analytics**: Custom aggregation pipelines providing net balance and category-wise spending percentages.
*   **Full-Text Search**: Optimized searching across transaction titles and descriptions.
*   **Transactional Integrity**: Uses MongoDB sessions to ensure category deletions safely update linked transactions.
*   **Strict Validation**: Pydantic v2 field validators for data hygiene (e.g., preventing future dates, stripping whitespace).

---
##  Project Structure

The project follows a clean, modular architecture to ensure scalability and separation of concerns:

```text
FinanceTrackerAPI/
├── Tracker/
│   ├── database/
│   │   ├── __init__.py
│   │   └── db.py               # DB connection & programmatic index setup
│   ├── Routes/
│   │   ├── __init__.py
│   │   ├── category_app.py     # Category CRUD & Transactional logic
│   │   ├── Pydantic_Models.py  # Strict Pydantic v2 Input/Output schemas
│   │   └── transaction_app.py  # Transaction CRUD & Aggregation pipelines
│   └── __init__.py
├── .env                        # Environment variables (DB URI, Secrets)
├── .gitignore                  # Python & Environment exclusions
├── main.py                     # App entry point & Router registration
├── poetry.lock                 # Locked dependency versions
└── pyproject.toml              # Project metadata & dependencies
```

##  Database Design

### Collections & Schema Justification

1.  transactions: Centralizes financial data. We use an embedded array for tags to allow flexible metadata without complex joins.
2.  categories: Stores unique category definitions. We enforce uniqueness at the database level to ensure data consistency.
3.  audit_logs: Captured during critical operations (like category deletion) to provide a history of systemic changes.


---

## Specialized Logic

### Aggregation Pipeline
The `/transactions/summary` endpoint utilizes a `$facet` pipeline to simultaneously calculate:
- Total monthly income/expenses.
- Spending breakdown by category with percentage calculations.
- The single highest expense for the period.

### MongoDB Transactions
The category deletion process is **atomic**. If a category is deleted, the system automatically:
1. Removes the category.
2. Re-assigns all orphaned transactions to `"uncategorized"`.
3. Logs the action to `audit_logs`.
*If any step fails, the entire operation rolls back.*

---

## ️ Setup & Installation

1. **Environment Config**: Create a `.env` file with your `MONGODB_URL`.
2. **Install Dependencies**:
   ```bash
   poetry install
