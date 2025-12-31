import unittest
import pandas as pd
from io import StringIO
from data_quality_check_main import DataQualityChecker

class TestDataQualityChecker(unittest.TestCase):
    def setUp(self):
        """Create sample data for testing."""
        self.rich_data = pd.DataFrame({                           # Rich dataset with no issues            
            'id': [1, 2, 3, 4],
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'age': [25, 30, 18, 35]
        })

        self.missing_data = pd.DataFrame({                        # Dataset with missing values
            'id': [1, 2, None, 4],
            'name': ['Alice', 'Bob', 'Charlie', 'David'],
            'age': [25, 30, 18, 35]
        })

        self.duplicate_data = pd.DataFrame({                      # Dataset with duplicate rows
            'id': [1, 2, 2, 4],
            'name': ['Alice', 'Bob', 'Bob', 'David'],
            'age': [25, 30, 30, 35]
        })

        self.empty_data = pd.DataFrame(columns=['id', 'name', 'age'])     # Empty dataset
        

    def test_check_missing_data_pass(self):
        """Test for missing data with rich data"""
        check = DataQualityChecker(self.rich_data)
        output = check.check_missing_values()
        self.assertTrue(output["passed"])

    def test_check_missing_data_fail(self):
        """Test for missing data with missing values"""
        check = DataQualityChecker(self.missing_data)
        output = check.check_missing_values(threshold=0.2)
        self.assertFalse(output["passed"])
        self.assertGreater(len(output['columns_with_issues']), 0)

    def test_check_duplicates_pass(self):
        """Test for duplicates with rich data"""
        check = DataQualityChecker(self.rich_data)
        output = check.check_duplicates()
        self.assertTrue(output["passed"])
        self.assertEqual(output['duplicate_rows'], 0)

    def test_check_duplicates_fail(self):
        """Test for duplicates with duplicate data"""
        check = DataQualityChecker(self.duplicate_data)
        output = check.check_duplicates()
        self.assertFalse(output["passed"])
        self.assertGreater(output['duplicate_rows'], 0)

    def test_check_empty_dataset_pass(self):
        """Test for empty dataset with rich data"""
        check = DataQualityChecker(self.rich_data)
        output = check.check_empty_dataset()
        self.assertTrue(output["passed"])
        self.assertEqual(output['row_count'], 4)

    def test_check_empty_dataset_fail(self):
        """Test for empty dataset with empty data"""
        check = DataQualityChecker(self.empty_data)
        output = check.check_empty_dataset()
        self.assertFalse(output["passed"])
        self.assertEqual(output['row_count'], 0)

    def test_check_data_types_pass(self):
        """Test for data types with rich data"""
        check = DataQualityChecker(self.rich_data)
        expected_types = {
            'id': 'int64', 
            'name': 'object', 
            'age': 'int64'
        }
        output = check.check_data_types(expected_types)
        self.assertTrue(output["passed"])

    def test_check_data_types_fail(self):
        """Test for data types with mismatched types"""
        check = DataQualityChecker(self.rich_data)
        expected_types = {
            'id': 'int64', 
            'name': 'int64',                   # Intentional mismatch
            'age': 'int64'
        }
        output = check.check_data_types(expected_types)
        self.assertFalse(output["passed"])
        self.assertIn('name', output['type_mismatches'])

    def test_run_all_checks(self):
        """Test running all checks together"""
        check = DataQualityChecker(self.rich_data)
        expected_types = {
            'id': 'int64', 
            'name': 'object', 
            'age': 'int64'
        }
        output = check.run_all_checks(expected_types, missing_value_threshold=0.1)
        self.assertTrue(output['validation_passed'])
        self.assertEqual(len(output['issues_found']), 0)

if __name__ == '__main__':
    unittest.main()