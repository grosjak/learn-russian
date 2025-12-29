from datetime import timedelta
from django.utils import timezone
from thefuzz import fuzz
import diff_match_patch as dmp_module

class SM2Service:
    """
    Implementation of the SuperMemo 2 (SM-2) Algorithm.
    """
    
    @staticmethod
    def calculate_review(quality, previous_interval, previous_ease, previous_streak):
        """
        Calculate next review data based on SM-2.
        
        Args:
            quality (int): 0-5 rating (0=blackout, 5=perfect)
            previous_interval (int): Last interval in days
            previous_ease (float): Last ease factor
            previous_streak (int): Current streak count
            
        Returns:
            dict: {
                'interval': new_interval_days,
                'ease_factor': new_ease_factor,
                'next_review_date': datetime,
                'streak': new_streak
            }
        """
        # 1. Update Streak and Interval start
        if quality >= 3:
            if previous_interval == 0:
                interval = 1
            elif previous_interval == 1:
                interval = 6
            else:
                interval = int(round(previous_interval * previous_ease))
            streak = previous_streak + 1
        else:
            interval = 1
            streak = 0
            
        # 2. Update Ease Factor
        # EF' = EF + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
        ease_factor = previous_ease + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        
        # Ease Factor minimum is 1.3
        if ease_factor < 1.3:
            ease_factor = 1.3
            
        next_date = timezone.now() + timedelta(days=interval)
        
        return {
            'interval': interval,
            'ease_factor': ease_factor,
            'next_review_date': next_date,
            'streak': streak
        }

class TextValidationService:
    """
    Service for validating text input using fuzzy matching.
    """
    
    @staticmethod
    def normalize_text(text):
        return text.lower().strip()
        
    @staticmethod
    def validate(user_input, correct_answer, threshold=90):
        """
        Validates user input against correct answer using fuzz.ratio.
        
        Returns:
            dict: {
                'is_correct': bool,
                'similarity': int (0-100),
                'diff': list (html diff)
            }
        """
        norm_input = TextValidationService.normalize_text(user_input)
        norm_correct = TextValidationService.normalize_text(correct_answer)
        
        # Calculate Levenshtein Similarity
        similarity = fuzz.ratio(norm_input, norm_correct)
        
        is_correct = similarity >= threshold
        
        # Generate Diff
        dmp = dmp_module.diff_match_patch()
        diffs = dmp.diff_main(norm_input, norm_correct)
        dmp.diff_cleanupSemantic(diffs)
        
        html_diff = dmp.diff_prettyHtml(diffs)
        
        return {
            'is_correct': is_correct,
            'similarity': similarity,
            'diff_html': html_diff
        }
