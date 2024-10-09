import pandas as pd
import traceback

class CSVBase:
    def __init__(self, csv_path=None):
        self.csv_path = csv_path
        self.df = None
        if csv_path:
            self.load_csv(csv_path)

    def log(self, message: str, title: str = "Info"):
        print(f"{title}: {message}")

    def load_csv(self, csv_path: str):
        try:
            self.df = pd.read_csv(csv_path)
            self.log(f"Loaded CSV: {csv_path}")
        except Exception as e:
            self.log(f"Error loading CSV: {e}", "Error")
            raise

    def generate_question(self, question: str) -> str:
        """
        Simulates processing a question by returning a canned response.
        """
        return f"Processing question: {question}"

    def generate_summary(self) -> str:
        """
        Generate a summary of the CSV data.
        """
        if self.df is None:
            return "No CSV loaded."
        
        summary = self.df.describe(include='all').to_string()
        self.log(f"Data Summary: \n{summary}")
        return summary

    def get_columns(self) -> list:
        """
        Return a list of column names from the CSV.
        """
        if self.df is None:
            return []
        return list(self.df.columns)

    def filter_data(self, column_name: str, value) -> pd.DataFrame:
        """
        Filter the CSV data based on the specified column and value.
        """
        if self.df is None:
            return None
        try:
            filtered_df = self.df[self.df[column_name] == value]
            return filtered_df
        except Exception as e:
            self.log(f"Error filtering data: {e}", "Error")
            return None

    def ask(self, question: str, column_name: str = None, value=None):
        """
        Simulates asking a question and returns the filtered data.
        """
        try:
            self.log(f"Asked question: {question}")
            if column_name and value:
                result_df = self.filter_data(column_name, value)
                if result_df is not None:
                    self.log(f"Filtered Data: \n{result_df.head()}")
                return result_df
            else:
                self.log("No column and value specified, returning full data.")
                return self.df
        except Exception as e:
            self.log(f"Error in ask: {e}", "Error")
            traceback.print_exc()

# Example usage
csv_base = CSVBase("data.csv")
csv_base.ask("What is the data for value X?", column_name="Column1", value="X")
