import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class ChartGenerator:

    @staticmethod
    def create_chart(df: pd.DataFrame):
        """
        Automatically create a chart from query results.
        """

        if df.empty:
            return None

        numeric_cols = df.select_dtypes(include="number").columns
        categorical_cols = df.select_dtypes(exclude="number").columns

        # Case 1
        # Category + Number
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            fig, ax = plt.subplots(figsize=(8,4))

            sns.barplot(
                data=df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                ax=ax
            )

            plt.xticks(rotation=30)
            plt.tight_layout()

            return fig

        # Case 2
        # Two numeric columns

        if len(numeric_cols) >= 2:

            fig, ax = plt.subplots(figsize=(8,4))

            sns.scatterplot(
                data=df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                ax=ax
            )

            plt.tight_layout()

            return fig

        return None