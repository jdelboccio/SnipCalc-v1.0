import numpy as np
from typing import List, Dict

def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """
    Calculate statistics (SUM, AVG, COUNT) from a list of numbers
    
    Args:
        numbers: List of numbers extracted from the image
        
    Returns:
        Dictionary containing SUM, AVG, and COUNT values
    """
    try:
        if not numbers:
            return {
                'SUM': 0.0,
                'AVG': 0.0,
                'COUNT': 0
            }
        
        # Calculate statistics
        total = np.sum(numbers)
        average = np.mean(numbers)
        count = len(numbers)
        
        # Round results to 2 decimal places
        return {
            'SUM': round(float(total), 2),
            'AVG': round(float(average), 2),
            'COUNT': count
        }
        
    except Exception as e:
        raise Exception(f"Error calculating statistics: {str(e)}")
