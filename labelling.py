from pprint import pprint

import pandas as pd

raw = pd.DataFrame(
    [
        # project, job, question, assessor, timestamp, label
        ("p1", "j1", "q1", "a1", "2026-08-01 09:00", 1),
        ("p1", "j1", "q1", "a2", "2026-08-01 09:05", 1),
        ("p1", "j1", "q1", "a3", "2026-08-01 09:10", 0),
        # a1 reassessed q1 later
        ("p1", "j1", "q1", "a1", "2026-08-01 11:00", 0),
        # Tied question
        ("p1", "j1", "q2", "a1", "2026-08-02 09:00", 0),
        ("p1", "j1", "q2", "a2", "2026-08-02 09:05", 1),
        # Unanimous negative
        ("p1", "j1", "q3", "a1", "2026-08-03 09:00", 0),
        ("p1", "j1", "q3", "a2", "2026-08-03 09:05", 0),
        ("p1", "j1", "q3", "a3", "2026-08-03 09:10", 0),
        # Missing label
        ("p1", "j1", "q4", "a1", "2026-08-04 09:00", 1),
        ("p1", "j1", "q4", "a2", "2026-08-04 09:05", 1),
        ("p1", "j1", "q4", "a4", "2026-08-04 09:10", None),
        # question_id is not globally unique
        ("p2", "j2", "q1", "a1", "2026-08-05 09:00", 1),
        ("p2", "j2", "q1", "a2", "2026-08-05 09:05", 0),
        ("p2", "j2", "q1", "a3", "2026-08-05 09:10", 0),
        # String label and invalid label
        ("p2", "j2", "q5", "a2", "2026-08-06 09:00", "1"),
        ("p2", "j2", "q5", "a3", "2026-08-06 09:05", 1),
        ("p2", "j2", "q5", "a4", "2026-08-06 09:10", 2),
        # Missing assessor
        ("p2", "j2", "q6", None, "2026-08-07 09:00", 1),
        ("p2", "j2", "q6", "a2", "2026-08-07 09:05", 1),
        ("p2", "j2", "q6", "a3", "2026-08-07 09:10", 0),
    ],
    columns=[
        "project",
        "job",
        "question",
        "assessor",
        "assessed_at",
        "label",
    ],
)


def audit_votes(raw: pd.DataFrame) -> dict:
    required_columns = {
        "project",
        "job",
        "question",
        "assessor",
        "assessed_at",
        "label",
    }

    missing_columns = required_columns - set(raw.columns)
    if missing_columns:
        raise ValueError(f"Missing required column: {sorted(missing_columns)}")

    # business key
    item_key = ["project", "job", "question"]
    vote_key = item_key + ["assessor"]

    work = raw.copy()  # shallow copy

    work["parsed_timestamp"] = pd.to_datetime(
        arg=raw["assessed_at"], format="%Y-%m-%d %H:%M", errors="coerce"
    )

    work["parsed_label"] = pd.to_numeric(work["label"], errors="coerce")

    missing_identifier_mask = work[vote_key].isna().any(axis=1)

    missing_timestamp_mask = (
        work["assessed_at"].notna() & work["parsed_timestamp"].isna()
    )

    missing_label_mask = work["label"].isna()

    non_numeric_label_mask = (
        work['label'].notna()
        & work['parsed_label'].isna()
    )

    out_of_domain_label_mask = (
        work['parsed_label'].notna() &
        work['parsed_label'].isin([0,1])
    )

    duplicate_vote_mask = work.duplicated(
        subset=vote_key,
        keep=False
    )

    return {
        "row_count": len(work),
        "missing_by_column": work[
            list(required_columns)
        ].isna().sum().to_dict(),
        "raw_label_values": work["label"]
            .value_counts(dropna=False)
            .to_dict(),
        "question_count": work[item_key]
            .drop_duplicates()
            .shape[0],
        "assessor_count": work["assessor"].nunique(),
        "duplicate_vote_rows": int(duplicate_vote_mask.sum()),
        "missing_identifier_rows": int(
            missing_identifier_mask.sum()
        ),
        "malformed_timestamp_rows": int(
            missing_timestamp_mask.sum()
        ),
        "missing_label_rows": int(missing_label_mask.sum()),
        "non_numeric_label_rows": int(
            non_numeric_label_mask.sum()
        ),
        "out_of_domain_label_rows": int(
            out_of_domain_label_mask.sum()
        ),
    }


get_audit_votes: dict = audit_votes(raw)
pprint(get_audit_votes)
