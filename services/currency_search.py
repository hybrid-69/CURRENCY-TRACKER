"""Search over the local currency mapping by code, name, or region."""

import pandas as pd
from config.settings import CURRENCY_MAPPING_PATH


class CurrencySearch:
    def __init__(self, mapping_path: str = CURRENCY_MAPPING_PATH):
        self.df = pd.read_csv(mapping_path)
        self._search_df = self.df.copy()
        for col in ["code", "name", "region"]:
            self._search_df[col + "_lower"] = self._search_df[col].str.lower()

    def search(self, query: str) -> pd.DataFrame:
        if not query or not query.strip():
            return self.df.iloc[0:0]

        q = query.strip().lower()

        exact_code = self._search_df[self._search_df["code_lower"] == q]
        if not exact_code.empty:
            return self._drop_helper_cols(exact_code)

        exact_name = self._search_df[self._search_df["name_lower"] == q]
        if not exact_name.empty:
            return self._drop_helper_cols(exact_name)

        name_match = self._search_df[self._search_df["name_lower"].str.contains(q, na=False)]
        region_match = self._search_df[self._search_df["region_lower"].str.contains(q, na=False)]

        combined = pd.concat([name_match, region_match]).drop_duplicates(subset="code")
        return self._drop_helper_cols(combined)

    @staticmethod
    def _drop_helper_cols(df: pd.DataFrame) -> pd.DataFrame:
        keep = ["code", "name", "region"]
        return df[keep].reset_index(drop=True)

    def is_valid_code(self, code: str) -> bool:
        return code.upper() in self.df["code"].values
