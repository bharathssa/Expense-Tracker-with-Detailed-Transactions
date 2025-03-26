import streamlit as st
import pandas as pd
import uuid

# Initialize session state for expenses
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []  # Store expenses entered by the user
if "edit_index" not in st.session_state:
    st.session_state["edit_index"] = None  # For editing an expense
if "participants" not in st.session_state:
    st.session_state["participants"] = []  # Store the list of participants


# Function to compute detailed transactions
def calculate_transactions(expenses):
    transactions = []  # List to hold individual transaction details

    for exp in expenses:
        payer = exp["paid_by"]  # The person who paid the expense
        total_cost = exp["amount"]  # Total cost of the expense
        participants = exp["participants"]  # List of participants
        split_type = exp["split_type"]  # The split type (Equally, Specific Person, Shared Purchase, Manual Split)
        date = exp["date"]
        category = exp["category"]

        if split_type == "Equally":
            # Calculate equal share among all participants
            share = total_cost / len(participants)
            for p in participants:
                if p != payer:  # Skip the payer, as they don't owe anyone
                    transactions.append({
                        "Date": date,
                        "Expense Name": category,
                        "Paid By": payer,
                        "From": p,
                        "To": payer,
                        "Share Amount": round(share, 2),
                        "Owe Amount": f"{p} owes {payer} ${round(share, 2)}"
                    })
        elif split_type == "Specific Person":
            # The specific person(s) are responsible for the total cost
            specific_persons = exp["specific_persons"]  # Get the list of specific persons
            share = total_cost / len(specific_persons)  # Split the amount equally among specific persons
            for specific_person in specific_persons:
                transactions.append({
                    "Date": date,
                    "Expense Name": category,
                    "Paid By": payer,
                    "From": specific_person,
                    "To": payer,
                    "Share Amount": round(share, 2),
                    "Owe Amount": f"{specific_person} owes {payer} ${round(share, 2)}"
                })
        elif split_type == "Manual Split":
            # Handle manual split where the user defines how much each person owes
            amounts_owed = exp["amounts_owed"]
            for p, amount in amounts_owed.items():
                if p != payer:
                    transactions.append({
                        "Date": date,
                        "Expense Name": category,
                        "Paid By": payer,
                        "From": p,
                        "To": payer,
                        "Share Amount": amount,
                        "Owe Amount": f"{p} owes {payer} ${round(amount, 2)}"
                    })
        else:  # Shared Purchase
            # In case of Shared Purchase, calculate the difference based on what each person paid
            amounts_paid = exp["amounts_paid"]
            total_paid = sum(amounts_paid.values())
            if total_paid > 0:
                for p in participants:
                    share = total_cost / len(participants)  # The equal share for each participant
                    diff = share - amounts_paid.get(p, 0)  # The difference between share and what was paid
                    if diff > 0:  # If the participant owes money
                        transactions.append({
                            "Date": date,
                            "Expense Name": category,
                            "Paid By": payer,
                            "From": p,
                            "To": payer,
                            "Share Amount": round(share, 2),
                            "Owe Amount": f"{p} owes {payer} ${round(diff, 2)}"
                        })
                    elif diff < 0:  # If the participant is owed money
                        transactions.append({
                            "Date": date,
                            "Expense Name": category,
                            "Paid By": payer,
                            "From": p,
                            "To": payer,
                            "Share Amount": round(share, 2),
                            "Owe Amount": f"{p} is owed ${round(-diff, 2)} by {payer}"
                        })

    return transactions


# UI - Expense Entry
st.title("💰 Expense Tracker with Detailed Transactions")
st.subheader("Enter Participants")
# Dynamically input the list of participants (comma-separated names)
participants_input = st.text_input("Enter participants (comma separated)", "")
if participants_input:
    st.session_state["participants"] = [name.strip() for name in participants_input.split(",")]

# UI - Expense Entry
st.subheader("Enter an Expense")

if st.session_state["edit_index"] is not None:
    # Editing an existing expense
    exp = st.session_state["expenses"][st.session_state["edit_index"]]
    date = st.date_input("Date of Expense", exp["date"])
    category = st.text_input("Category", exp["category"])
    amount = st.number_input("Total Cost ($)", min_value=0.0, step=0.01, value=exp["amount"])
    paid_by = st.selectbox("Who paid?", st.session_state["participants"], index=st.session_state["participants"].index(exp["paid_by"]))
    split_type = st.radio("Split Type", ["Equally", "Specific Person", "Shared Purchase", "Manual Split"], index=["Equally", "Specific Person", "Shared Purchase", "Manual Split"].index(exp["split_type"]))

    # Logic for different split types
    if split_type == "Equally":
        participants = st.session_state["participants"]  # Auto-select all participants
        specific_persons = None
        st.write(f"Since the split is equally, the total amount of ${amount} will be divided equally among all participants.")
    elif split_type == "Shared Purchase":
        participants = st.session_state["participants"]
        amounts_paid = {}
        # Ask for the amount paid by each participant in the shared purchase scenario
        for participant in participants:
            amounts_paid[participant] = st.number_input(f"Amount paid by {participant}", min_value=0.0, value=0.0)
        st.write(f"Since this is a shared purchase, please enter how much each person paid. Total cost: ${amount}.")
        specific_persons = None
    elif split_type == "Manual Split":
        # Allow users to manually input how much each person owes
        amounts_owed = {}
        for participant in st.session_state["participants"]:
            amounts_owed[participant] = st.number_input(f"Amount owed by {participant}", min_value=0.0, value=0.0)
        st.write(f"Please manually enter how much each person owes for the total amount of ${amount}.")
        participants = st.session_state["participants"]
        specific_persons = None
    else:
        # Handle specific persons (comma-separated names)
        specific_persons_input = st.text_input("Enter specific persons (comma separated)", "")
        if specific_persons_input:
            specific_persons = [name.strip() for name in specific_persons_input.split(",")]
            participants = []
        else:
            specific_persons = []
            participants = []
        st.write(f"The expense of ${amount} will be paid by {paid_by} and divided among {', '.join(specific_persons)}.")

    # Update the expense in session state
    if st.button("Update Expense"):
        st.session_state["expenses"][st.session_state["edit_index"]] = {
            "id": exp["id"],
            "date": date,
            "category": category,
            "amount": amount,
            "paid_by": paid_by,
            "split_type": split_type,
            "participants": participants,
            "specific_persons": specific_persons,
            "amounts_paid": amounts_paid if split_type == "Shared Purchase" else None,
            "amounts_owed": amounts_owed if split_type == "Manual Split" else None
        }
        st.session_state["edit_index"] = None
        st.rerun()

    st.button("Cancel Edit", on_click=lambda: st.session_state.update({"edit_index": None}))
else:
    # Adding a new expense
    expense_id = str(uuid.uuid4())
    date = st.date_input("Date of Expense")
    category = st.text_input("Category (e.g., Groceries, Dining, Utilities)")
    amount = st.number_input("Total Cost ($)", min_value=0.0, step=0.01)
    paid_by = st.selectbox("Who paid?", st.session_state["participants"])
    split_type = st.radio("Split Type", ["Equally", "Specific Person", "Shared Purchase", "Manual Split"])

    # Logic for different split types
    if split_type == "Equally":
        participants = st.session_state["participants"]  # Auto-select all participants
        specific_persons = None
        st.write(f"Since the split is equally, the total amount of ${amount} will be divided equally among all participants.")
    elif split_type == "Shared Purchase":
        participants = st.session_state["participants"]
        amounts_paid = {}
        # Ask for the amount paid by each participant in the shared purchase scenario
        for participant in participants:
            amounts_paid[participant] = st.number_input(f"Amount paid by {participant}", min_value=0.0, value=0.0)
        st.write(f"Since this is a shared purchase, please enter how much each person paid. Total cost: ${amount}.")
        specific_persons = None
    elif split_type == "Manual Split":
        # Allow users to manually input how much each person owes
        amounts_owed = {}
        for participant in st.session_state["participants"]:
            amounts_owed[participant] = st.number_input(f"Amount owed by {participant}", min_value=0.0, value=0.0)
        st.write(f"Please manually enter how much each person owes for the total amount of ${amount}.")
        participants = st.session_state["participants"]
        specific_persons = None
    else:
        # Handle specific persons (comma-separated names)
        specific_persons_input = st.text_input("Enter specific persons (comma separated)", "")
        if specific_persons_input:
            specific_persons = [name.strip() for name in specific_persons_input.split(",")]
            participants = []
        else:
            specific_persons = []
            participants = []
        st.write(f"The expense of ${amount} will be paid by {paid_by} and divided among {', '.join(specific_persons)}.")

    # Add the expense to session state
    if st.button("Add Expense"):
        st.session_state["expenses"].append({
            "id": expense_id,
            "date": date,
            "category": category,
            "amount": amount,
            "paid_by": paid_by,
            "split_type": split_type,
            "participants": participants,
            "specific_persons": specific_persons,
            "amounts_paid": amounts_paid if split_type == "Shared Purchase" else None,
            "amounts_owed": amounts_owed if split_type == "Manual Split" else None
        })
        st.rerun()

# UI - Display Recorded Expenses
st.subheader("📜 Recorded Expenses")
if st.session_state["expenses"]:
    for idx, exp in enumerate(st.session_state["expenses"]):
        # Handle participants and specific persons more safely
        participants_display = ', '.join(exp['participants']) if exp['participants'] else 'No participants'
        specific_persons_display = ', '.join(exp['specific_persons']) if exp['specific_persons'] else 'No specific persons'

        details = f"{exp['paid_by']} paid ${exp['amount']:.2f} for {participants_display if exp['split_type'] == 'Equally' else specific_persons_display} (Category: {exp['category']}, Date: {exp['date']})"

        col1, col2, col3 = st.columns([4, 1, 1])
        col1.write(details)
        if col2.button("🗑️ Delete", key=f"del_{exp['id']}"):
            del st.session_state["expenses"][idx]
            st.rerun()
        if col3.button("✏️ Edit", key=f"edit_{exp['id']}"):
            st.session_state["edit_index"] = idx
            st.rerun()

# UI - Display Transaction Details
st.subheader("📋 Transaction Details")
transactions = calculate_transactions(st.session_state["expenses"])
if transactions:
    df = pd.DataFrame(transactions)
    st.table(df)

# Display summary/conclusion
st.subheader("📝 Summary")

# Dictionary to track net balances (how much each person owes or is owed)
balances = {}

for exp in st.session_state["expenses"]:
    total_cost = exp["amount"]
    split_type = exp["split_type"]
    payer = exp["paid_by"]

    if split_type == "Equally":
        share = total_cost / len(exp["participants"])
        for p in exp["participants"]:
            if p != payer:
                balances[p] = balances.get(p, 0) - round(share, 2)
                balances[payer] = balances.get(payer, 0) + round(share, 2)

    elif split_type == "Specific Person":
        specific_persons = exp["specific_persons"]
        share = total_cost / len(specific_persons)
        for specific_person in specific_persons:
            balances[specific_person] = balances.get(specific_person, 0) - round(share, 2)
            balances[payer] = balances.get(payer, 0) + round(share, 2)

    elif split_type == "Manual Split":
        amounts_owed = exp["amounts_owed"]
        for p, amount in amounts_owed.items():
            if p != payer:
                balances[p] = balances.get(p, 0) - round(amount, 2)
                balances[payer] = balances.get(payer, 0) + round(amount, 2)

    elif split_type == "Shared Purchase":
        amounts_paid = exp["amounts_paid"]
        total_paid = sum(amounts_paid.values())
        if total_paid > 0:
            for p in exp["participants"]:
                share = total_cost / len(exp["participants"])
                diff = round(share - amounts_paid.get(p, 0), 2)
                if diff > 0:
                    balances[p] = balances.get(p, 0) - diff
                    balances[payer] = balances.get(payer, 0) + diff

# Generate final transactions based on balances
final_transactions = []
for person, amount in balances.items():
    if amount < 0:  # This person owes money
        for creditor, credit_amount in balances.items():
            if credit_amount > 0:
                settled_amount = min(abs(amount), credit_amount)
                final_transactions.append(f"{person} owes {creditor} ${round(settled_amount, 2)}")
                balances[person] += settled_amount
                balances[creditor] -= settled_amount
                if balances[person] == 0:
                    break

# Display final transactions
for transaction in final_transactions:
    st.write(transaction)

# Button to clear all entries
if st.button("Clear All Entries"):
    st.session_state["expenses"] = []
    st.session_state["participants"] = []
    st.experimental_rerun()
