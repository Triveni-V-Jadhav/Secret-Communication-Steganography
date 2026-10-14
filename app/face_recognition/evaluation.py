import numpy as np

class BiometricEvaluator:
    """
    Evaluates Face Verification performance across varying decision thresholds.
    Computes False Acceptance Rate (FAR), False Rejection Rate (FRR),
    Receiver Operating Characteristic (ROC), and Equal Error Rate (EER).
    """
    
    @staticmethod
    def evaluate_thresholds(genuine_scores: list, impostor_scores: list, thresholds: list = None) -> dict:
        """
        genuine_scores: List of similarity scores between pairs of the same identity (1.0 = perfect match)
        impostor_scores: List of similarity scores between pairs of different identities
        """
        if thresholds is None:
            thresholds = np.linspace(0.40, 0.95, 25).tolist()
            
        gen = np.array(genuine_scores)
        imp = np.array(impostor_scores)
        
        results = []
        eer = None
        min_diff = 1.0
        eer_threshold = 0.70
        
        for t in thresholds:
            # False Rejection Rate (FRR): genuine attempts wrongly rejected (score < t)
            frr = float(np.mean(gen < t)) if len(gen) > 0 else 0.0
            
            # False Acceptance Rate (FAR): impostor attempts wrongly accepted (score >= t)
            far = float(np.mean(imp >= t)) if len(imp) > 0 else 0.0
            
            diff = abs(far - frr)
            if diff < min_diff:
                min_diff = diff
                eer = (far + frr) / 2.0
                eer_threshold = t
                
            results.append({
                "threshold": round(t, 3),
                "far": round(far, 4),
                "frr": round(frr, 4),
                "accuracy": round(1.0 - (far + frr) / 2.0, 4)
            })
            
        return {
            "eval_points": results,
            "eer": round(eer, 4) if eer is not None else 0.05,
            "eer_threshold": round(eer_threshold, 3),
            "total_genuine": len(genuine_scores),
            "total_impostor": len(impostor_scores)
        }
