from typing import List, Dict

def calculate_stats(numbers: List[float]) -> Dict[str, float]:
    """
    Calculate statistics (SUM, AVG, COUNT) from a list of numbers
    
    Args:
        numbers: List of numbers extracted from the image
        
    Returns:
        Dictionary containing SUM, AVG, and COUNT values
    """
    if not numbers:
        return {
            'SUM': 0.0,
            'AVG': 0.0,
            'COUNT': 0
        }
    
    total = sum(numbers)
    count = len(numbers)
    avg = total / count
    
    return {
        'SUM': round(total, 2),
        'AVG': round(avg, 2),
        'COUNT': count
    }
