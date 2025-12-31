import pandas as pd
from typing import Dict, Tuple

class DataQualityChecker:
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.issues = []

    def check_missing_values(self, threshold: float = 0.5) -> Dict:
        """Check for missing values in each column and return the percentage of missing values."""
        missing_values = self.data.isnull().sum() / len(self.data)
        problematic_columns = missing_values[missing_values > threshold]

        output = {
            "passed": len(problematic_columns) == 0,
            "columns_with_issues": problematic_columns.to_dict(),
            "message": f"Columns with more than {threshold*100}% missing values: {list(problematic_columns.index)}"
        }

        if not output["passed"]:
            self.issues.append(output["message"])

        return output

    def check_duplicates(self) -> Dict:
        """Check for duplicate rows in the DataFrame and return the count of duplicates."""
        duplicate_count = self.data.duplicated().sum()

        output = {
            "passed": duplicate_count == 0,
            "duplicate_rows": duplicate_count,
            "message": f"Number of duplicate rows found: {duplicate_count}"
        }
        if not output["passed"]:
            self.issues.append(output["message"])

        return output

    def check_data_types(self, expected_types: Dict[str, str]) -> Dict:
        """Check the data types of each column and return a dictionary of mismatches."""
        mismatches = {}
        for col, expected_type in expected_types.items():
            if col not in self.data.columns:
                mismatches[col] = f"Column {col} not found"
            elif str(self.data[col].dtype) != expected_type:
                mismatches[col] = f"Expected {expected_type}, found {self.data[col].dtype}"

        output = {
            "passed": len(mismatches) == 0,
            "type_mismatches": mismatches,
            "message": f"Data type mismatches found: {len(mismatches)}"
        }

        if not output["passed"]:
            self.issues.append(output["message"])

        return output

    def check_empty_dataset(self) -> Dict:
        """Check if the dataset is empty."""
        is_empty = len(self.data) == 0

        output = {
            "passed": not is_empty,
            "row_count": len(self.data),
            "message": "Dataset is empty" if is_empty else "Dataset is not empty"
        }

        if not output["passed"]:
            self.issues.append(output["message"])

        return output
    
    def run_all_checks(self, expected_types: Dict[str, str] = None, missing_value_threshold: float = 0.5) -> Dict:
        """Run all data quality checks and return a summary."""
        output = {   
            "empty_dataset": self.check_empty_dataset(),
            "missing_values": self.check_missing_values(threshold=missing_value_threshold),
            "duplicates": self.check_duplicates(),
        }
        
        if expected_types:
            output["data_types"] = self.check_data_types(expected_types)

        all_passed = all(check["passed"] for check in output.values())
            
        return {
            "validation_passed": all_passed,
            "issues_found": self.issues,
            "detailed_results": output
        }

    def load_and_check(self, file_path: str, expected_types: Dict[str, str] = None) -> Tuple[pd.DataFrame, Dict]:
        """Load data from a CSV file and run all data quality checks."""
        data = pd.read_csv(file_path)
        check = DataQualityChecker(data)
        output = check.run_all_checks(expected_types)

        return data, output