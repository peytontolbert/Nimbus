import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from typing import List, Union, Dict

class datavisualization:
    
    @staticmethod
    def chartgenerator(data: Union[List, pd.DataFrame], chart_type: str, title: str, labels: List[str] = None):
        if not isinstance(data, (list, pd.DataFrame)):
            raise ValueError("Data should be a list or a pandas DataFrame.")
        
        if not isinstance(chart_type, str):
            raise ValueError("Chart type should be a string.")
        
        if not isinstance(title, str):
            raise ValueError("Title should be a string.")
        
        if labels and not isinstance(labels, list):
            raise ValueError("Labels should be a list of strings.")
        
        if isinstance(data, list):
            data = pd.DataFrame(data, columns=labels)
        
        plt.figure(figsize=(10, 6))
        
        if chart_type == 'line':
            sns.lineplot(data=data)
        elif chart_type == 'bar':
            data.plot(kind='bar')
        elif chart_type == 'hist':
            data.plot(kind='hist')
        elif chart_type == 'scatter' and len(data.columns) >= 2:
            plt.scatter(data.iloc[:, 0], data.iloc[:, 1])
            plt.xlabel(labels[0] if labels else 'X')
            plt.ylabel(labels[1] if labels else 'Y')
        else:
            raise ValueError("Unsupported chart type or incorrect data format for the selected chart type.")
        
        plt.title(title)
        plt.show()
    
    @staticmethod
    def dashboard_generator(args: Dict):
        data = args.get('data')
        dashboard_type = args.get('dashboard_type')
        filters = args.get('filters', {})
        
        if not isinstance(data, (list, pd.DataFrame)):
            raise ValueError("Data should be a list or a pandas DataFrame.")
        
        if not isinstance(dashboard_type, str):
            raise ValueError("Dashboard type should be a string.")
        
        if not isinstance(filters, dict):
            raise ValueError("Filters should be a dictionary.")
        
        if isinstance(data, list):
            data = pd.DataFrame(data)
        
        # Apply filters to the data
        for key, value in filters.items():
            if key in data.columns:
                data = data[data[key] == value]
        
        # Placeholder for actual dashboard generation logic
        print(f"Generating {dashboard_type} dashboard with the following data:")
        print(data.head())
        print("Dashboard filters applied:", filters)