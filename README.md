# Expense-Tracker-with-Detailed-Transactions
This Expense Tracker is a Streamlit app for managing shared expenses. Users can add participants, record expenses, and split costs equally, by specific persons, shared purchase, or manual split. It calculates who owes whom, allows editing, deleting, resetting, and supports PDF export. Ideal for trips and shared costs! 🚀
# Expense Tracker with Detailed Transactions

This Streamlit application is a powerful tool for managing shared expenses among groups, providing detailed breakdowns and flexible splitting options. It's designed to simplify the often complex task of figuring out who owes what after shared activities, trips, or purchases.

## Key Features

- **Participant Management:**
  - Dynamically add and manage participants.
  - Store participant names for use across multiple expense entries.
- **Flexible Expense Tracking:**
  - Record expense details, including date, category, and amount.
  - Edit and delete expense entries as needed.
- **Versatile Splitting Options:**
  - **Equally:** Split expenses evenly among all participants.
  - **Specific Person:** Assign expenses to specific individuals.
  - **Shared Purchase:** Handle scenarios where participants contribute different amounts.
  - **Manual Split:** Define custom amounts owed by each participant.
- **Detailed Transaction Breakdown:**
  - Generate a clear, tabular view of all transactions.
  - Show who owes whom and the exact amount for each expense.
- **Expense Summaries:**
  - Provides a summary of who owes whom for each expense.
- **User-Friendly Interface:**
  - Built with Streamlit for an intuitive and interactive experience.
- **Data Persistence:**
  - Uses Streamlit's session state to maintain data across interactions.
- **PDF Export:**
  - Option to download the transaction details as a PDF file.
- **Clear All Entries:**
  - Reset the application and remove all data.

## How It Works

### 1. Participants Input:
- Users enter a comma-separated list of participant names.
- These names are stored and used throughout the expense tracking process.

### 2. Expense Entry:
- Users input expense details, including:
  - Date
  - Category (e.g., "Groceries," "Dining")
  - Total Amount
  - Payer (the person who paid initially)
  - Split Type

### 3. Splitting Logic:
- The application handles different splitting scenarios:
  - **Equally:** Divides the total amount by the number of participants.
  - **Specific Person:** Assigns the expense to a selected group of people.
  - **Shared Purchase:** Allows users to enter individual contributions and calculates who owes or is owed.
  - **Manual Split:** Provides fields for users to define the exact amount each person owes.

### 4. Transaction Calculation:
- The `calculate_transactions` function processes the expense data.
- It generates a list of individual transactions, showing the "From" (debtor), "To" (creditor), and "Amount."

### 5. Output and Display:
- Recorded expenses are displayed with options to edit or delete.
- A table shows all calculated transactions.
- A summary is provided.
- Option to download the transactions as a PDF.

## Who Is This For?

This application is ideal for:
- Groups of friends sharing expenses on trips or outings.
- Housemates splitting rent, utilities, and groceries.
- Anyone who wants a clear and organized way to track shared costs.
- Event planners managing budgets and payments.

## Getting Started

### Prerequisites:
- Python 3.6+
- `pip` (Python package installer)

### Installation:
```bash
pip install streamlit pandas streamlit-pdf
```

### Running the App:
```bash
streamlit run your_app_name.py
```
(Replace `your_app_name.py` with the name of your Python file.)

## Code Structure
- `main.py` (or your chosen filename): Contains the Streamlit application code, including:
  - Import statements for `streamlit`, `pandas`, and `uuid`.
  - Functions for calculating transactions and managing data.
  - Streamlit UI elements for input, display, and interaction.
  - State management using `st.session_state`.

## Contributing

Contributions are welcome! Feel free to submit pull requests for bug fixes, new features, or improvements to the documentation.

## PDF Export Instructions

### Install `streamlit-pdf`:
```bash
pip install streamlit-pdf
```

### Add PDF Download Button:
```python
from streamlit_pdf import st_pdf

# ... (Your existing Streamlit code)

if transactions:
    pdf_bytes = st_pdf(df.to_html(), height="1000px")
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name="transactions.pdf",
        mime="application/pdf",
    )
```

