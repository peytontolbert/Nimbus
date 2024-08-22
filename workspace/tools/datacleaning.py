import pandas as pd
import numpy as np

class datacleaning:
    """
    A class for cleaning and sanitizing data sets.
    """
    
    @staticmethod
    def datasanitizer(data, fill_method='mean', normalize=False):
        """
        Cleans and sanitizes the provided data set.

        Args:
            data (list or pd.DataFrame): The data to be sanitized.
            fill_method (str): The method to fill missing values. Options are 'mean', 'median', or 'mode'.
            normalize (bool): Whether to normalize the data or not.

        Returns:
            pd.DataFrame: The cleaned and optionally normalized data.
        """
        # Convert list to DataFrame if necessary
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        if not isinstance(data, pd.DataFrame):
            raise ValueError("Data must be a list or a pandas DataFrame.")
        
        # Fill missing values
        if fill_method == 'mean':
            data = data.fillna(data.mean())
        elif fill_method == 'median':
            data = data.fillna(data.median())
        elif fill_method == 'mode':
            data = data.fillna(data.mode().iloc[0])
        else:
            raise ValueError("Invalid fill_method. Choose from 'mean', 'median', or 'mode'.")

        # Normalize the data if requested
        if normalize:
            data = (data - data.min()) / (data.max() - data.min())

        return data