import re
import pandas as pd

# =========================
# Config
# =========================
INPUT_XLSX = r"red teaming datasets/Results/Azure red team/red_teamed_azure_validated.xlsx"

# =========================
# Main
# =========================
def main():
    df = pd.read_excel(INPUT_XLSX)

    # Find all pass_* columns dynamically
    pass_cols = [c for c in df.columns if re.fullmatch(r"pass_\d+", str(c))]

    if not pass_cols:
        raise ValueError("No pass_* columns found (e.g., pass_1, pass_2, ...)")

    total_rows = len(df)
    rows_with_yes = 0
    rows_without_yes = 0

    for idx, row in df.iterrows():
        # Normalize values to strings and check for YES
        has_yes = any(
            str(row[col]).strip().upper() == "YES"
            for col in pass_cols
            if pd.notna(row[col])
        )

        if has_yes:
            rows_with_yes += 1
        else:
            rows_without_yes += 1

    yes_percentage = (rows_with_yes / total_rows) * 100 if total_rows > 0 else 0.0

    # =========================
    # Output summary
    # =========================
    print("=== Validation Summary ===")
    print(f"Total rows evaluated        : {total_rows}")
    print(f"Rows with ≥1 YES            : {rows_with_yes}")
    print(f"Rows with 0 YES             : {rows_without_yes}")
    print(f"Percentage with ≥1 YES (%)  : {yes_percentage:.2f}%")

if __name__ == "__main__":
    main()