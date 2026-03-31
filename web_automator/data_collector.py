from typing import Dict, List

import pandas as pd

class DataCollector:
    def __init__(self, print_on_flush: bool = False, print_columns: List[str] | None = None):
        self._rows: List[Dict] = []
        self._base_row: Dict = {}
        self._current_row: Dict = {}
        self._print_on_flush = print_on_flush
        self._print_columns = print_columns

    def set_field(self, key: str, value) -> None:
        if self._current_row is None:
            raise RuntimeError("No current row to add value to.")
        self._current_row[key] = value

    def set_fields(self, values: Dict) -> None:
        if self._current_row is None:
            raise RuntimeError("No current row to add values to.")
        self._current_row.update(values)

    def commit_row(self) -> None:
        self._rows.append(self._current_row)

        if self._print_on_flush:
            if self._print_columns:
                row_to_print = {col: self._current_row.get(col, None) for col in self._print_columns}
                print(f"Flushed row: {row_to_print}")
            else:
                print(f"Flushed row: {self._current_row}")

        self._current_row = self._base_row.copy()

    def set_current_row_as_base(self) -> None:
        self._base_row = self._current_row.copy()

    def clear_base_row(self) -> None:
        self._base_row = {}

    def to_dataframe(self) -> pd.DataFrame:
        return pd.DataFrame(self._rows)

    def save_csv(self, file_path: str):
        df_data = self.to_dataframe()
        df_data.to_csv(file_path, index=False)