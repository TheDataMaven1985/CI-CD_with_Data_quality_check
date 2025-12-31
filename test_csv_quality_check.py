import unittest
import pandas as pd
import os
from data_quality_check_main import DataQualityChecker

class TestDataQualityCheckerWithCSV(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data file path."""
        cls.test_data_file = os.path.join(os.path.dirname(__file__), 'test_data')

    def test_load_and_check_good_data(self):
        """Test loading and checking a good CSV data file."""
        file_path = os.path.join(self.test_data_file, 'good_data.csv')

        # Skips file if not found
        if not os.path.exists(file_path):
            self.skipTest(f"Test data file {file_path} not found.")

        data = pd.read_csv(file_path)
        checker = DataQualityChecker(data)

        expected_types = {
            'id': 'int64',
            'name': 'object',
            'age': 'int64'
        }

        result = checker.run_all_checks(expected_types)
        self.assertTrue(result['validation_passed'])
        self.assertEqual(len(result['issues_found']), 0)

    def test_load_and_check_missing_data(self):
        """Test loading and checking a CSV data file with missing values."""

        file_path = os.path.join(self.test_data_file, 'missing_data.csv')

        # Skips file if not found
        if not os.path.exists(file_path):
            self.skipTest(f"Test data file {file_path} not found.")

        data = pd.read_csv(file_path)
        checker = DataQualityChecker(data)

        result = checker.check_missing_values(threshold=0.2)
        print(f"\nMissing Check Result: {result['message']}")
        self.assertFalse(result['passed'])
        
    def test_load_and_check_duplicate_data(self):
        """Test loading and checking a CSV data file with duplicate rows."""
        file_path = os.path.join(self.test_data_file, 'duplicate_data.csv')

        # if file not found, skip the test
        if not os.path.exists(file_path):
            self.skipTest(f"Test data file {file_path} not found.")
        
        data = pd.read_csv(file_path)
        checker = DataQualityChecker(data)

        result = checker.check_duplicates()
        print(f"\nDuplicate Check Result: {result['message']}")
        self.assertFalse(result['passed'])
        self.assertGreater(result['duplicate_rows'], 0)

    def test_load_and_check_empty_data(self):
        """Test loading and checking an empty CSV data file."""
        file_path = os.path.join(self.test_data_file, 'empty_data.csv')
        # if file not found, skip the test
        if not os.path.exists(file_path):
            self.skipTest(f"Test data file {file_path} not found.")
        
        data = pd.read_csv(file_path)
        checker = DataQualityChecker(data)

        result = checker.check_empty_dataset()
        print(f"\nEmpty Check Result: {result['message']}")
        self.assertFalse(result['passed'])

if __name__ == '__main__':
    unittest.main()