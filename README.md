# Git Practice Crypto Pipeline Project

A modular, lightweight Python application built with Streamlit designed specifically for practicing **Git branching, merging, merge conflict generation, conflict resolution, and team integration workflows**.

---

## 🚀 Quick Start & Application Verification

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501` to verify transaction processing and inventory tracking.

---

## 📁 Directory Structure

```text
git-practice-project/
│
├── app.py                    # Streamlit UI (Shared entry point)
├── requirements.txt          # Python dependencies
├── README.md                 # Project & Git practice documentation
│
├── backend/
│   ├── ingestion.py          # Dev 1: Ingestion feature module
│   ├── processing.py         # Pipeline coordinator (Shared file)
│   ├── validation.py         # Dev 3: Validation feature module
│   └── pricing.py            # Dev 2: Pricing feature module
│
├── security/
│   └── inventory.py          # Dev 4: Inventory feature module
│
└── config/
    └── config.py             # Global settings
```

---

## 👩‍💻 Git Practice & Developer Simulation Guide

This section guides you through acting as **Project Lead** and simulating 4 developers working on parallel feature branches, performing clean merges, creating intentional merge conflicts, and resolving them.

---

### Step 1: Initialize Git Repository & Base Branch

Ensure you are on the `main` branch with clean initial code:

```bash
git init
git add .
git commit -m "Initial commit: Base crypto pipeline"
git branch -M main
```

---

### Step 2: Simulate 4 Parallel Developer Feature Branches

Each developer works on a designated feature branch:

| Developer | Feature Branch | Target Module |
|---|---|---|
| **Dev 1** | `feature/ingestion` | `backend/ingestion.py` |
| **Dev 2** | `feature/pricing` | `backend/pricing.py` |
| **Dev 3** | `feature/validation` | `backend/validation.py` |
| **Dev 4** | `feature/inventory` | `security/inventory.py` |

---

#### 🛠️ Developer 1 (`feature/ingestion`)
Create branch, make an independent change, and commit:

```bash
git checkout -b feature/ingestion
```

*Edit `backend/ingestion.py`* (e.g., add a transaction ID generator):
```python
import uuid
# Add inside parse_transaction_data:
# "tx_id": str(uuid.uuid4())[:8]
```

Commit & merge:
```bash
git add backend/ingestion.py
git commit -m "feat(ingestion): add unique transaction ID parsing"

# Switch back to main and merge
git checkout main
git merge feature/ingestion
```

Verify application:
```bash
streamlit run app.py
```

---

#### 🛠️ Developer 2 (`feature/pricing`)
Create branch, make an independent change, and commit:

```bash
git checkout -b feature/pricing
```

*Edit `backend/pricing.py`* (e.g., add fee calculation):
```python
def calculate_fee(total_value: float, fee_rate: float = 0.001) -> float:
    return total_value * fee_rate
```

Commit & merge:
```bash
git add backend/pricing.py
git commit -m "feat(pricing): add transaction fee calculation function"

git checkout main
git merge feature/pricing
```

---

#### 🛠️ Developer 3 (`feature/validation`)
Create branch, update validation logic, commit & merge:

```bash
git checkout -b feature/validation
git add backend/validation.py
git commit -m "feat(validation): enhance security check rules"

git checkout main
git merge feature/validation
```

---

#### 🛠️ Developer 4 (`feature/inventory`)
Create branch, update inventory module, commit & merge:

```bash
git checkout -b feature/inventory
git add security/inventory.py
git commit -m "feat(inventory): add balance check before deduction"

git checkout main
git merge feature/inventory
```

---

### 💥 Step 3: Simulate and Resolve Merge Conflicts

Shared files like `app.py` or `backend/processing.py` are perfect for generating merge conflicts when multiple developers modify the exact same lines concurrently.

#### Scenario: Dev 1 and Dev 2 modify `app.py` at the same time!

1. **Dev 1 makes changes in `app.py`:**
```bash
git checkout -b dev1/ui-update
# Edit app.py header title to:
# st.markdown("<div class='main-header'>🚀 Dev 1 Crypto Engine</div>", unsafe_allow_html=True)
git add app.py
git commit -m "style: update app title by Dev 1"
```

2. **Dev 2 makes different changes to the SAME line in `app.py` on another branch:**
```bash
git checkout main
git checkout -b dev2/ui-update
# Edit app.py header title to:
# st.markdown("<div class='main-header'>💎 Dev 2 Financial Terminal</div>", unsafe_allow_html=True)
git add app.py
git commit -m "style: update app title by Dev 2"
```

3. **Merge Dev 1's branch into `main` (Succeeds):**
```bash
git checkout main
git merge dev1/ui-update
```

4. **Merge Dev 2's branch into `main` (Causes Conflict!):**
```bash
git merge dev2/ui-update
```
Git will output:
```text
CONFLICT (content): Merge conflict in app.py
Automatic merge failed; fix conflicts and then commit the result.
```

5. **Inspect & Resolve Conflict:**
Open `app.py`. You will see conflict markers:
```python
<<<<<<< HEAD
st.markdown("<div class='main-header'>🚀 Dev 1 Crypto Engine</div>", unsafe_allow_html=True)
=======
st.markdown("<div class='main-header'>💎 Dev 2 Financial Terminal</div>", unsafe_allow_html=True)
>>>>>>> dev2/ui-update
```

Decide on the resolved version (e.g., combine them):
```python
st.markdown("<div class='main-header'>🚀 Crypto Engine & Financial Terminal</div>", unsafe_allow_html=True)
```

6. **Complete Conflict Resolution Commit:**
```bash
git add app.py
git commit -m "fix(merge): resolve title conflict between Dev 1 and Dev 2"
```

---

### 🧪 Step 4: Verification After Merging

After resolving conflicts or completing any merge, always verify the app:

```bash
streamlit run app.py
```
Check that:
1. Application starts without syntax or import errors.
2. Ingestion → Pricing → Validation → Inventory flow executes properly.
3. The UI renders the updated changes cleanly.
