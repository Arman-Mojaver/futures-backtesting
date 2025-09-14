from typing import Any

import pandas as pd


def from_databento_df_to_items(df: pd.DataFrame) -> dict[str, Any]:
    return list(
        df.reset_index()
        .rename(columns={df.reset_index().columns[0]: "timestamp"})
        .astype({"timestamp": str})
        .T.to_dict()
        .values()
    )
