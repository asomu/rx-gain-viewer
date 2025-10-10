"""
Progress Tracker for Long-Running Tasks
Uses Django cache to store and retrieve progress information
"""
from django.core.cache import cache
import time


class ProgressTracker:
    """Track progress of long-running tasks using Django cache"""

    CACHE_TIMEOUT = 3600  # 1 hour

    def __init__(self, task_id):
        """
        Initialize progress tracker for a task

        Args:
            task_id: Unique identifier for the task (e.g., session_id)
        """
        self.task_id = task_id
        self.cache_key = f"progress_{task_id}"

    def start(self, total_items, description="Processing"):
        """
        Start tracking progress

        Args:
            total_items: Total number of items to process
            description: Task description
        """
        progress_data = {
            'status': 'running',
            'current': 0,
            'total': total_items,
            'percentage': 0.0,
            'description': description,
            'current_item': '',
            'elapsed_time': 0.0,
            'estimated_remaining': 0.0,
            'start_time': time.time(),
            'message': f'Starting {description}...'
        }
        cache.set(self.cache_key, progress_data, self.CACHE_TIMEOUT)

    def update(self, current, current_item=''):
        """
        Update progress

        Args:
            current: Current item number (1-indexed)
            current_item: Description of current item (e.g., "B1 G0_H ANT1")
        """
        progress_data = cache.get(self.cache_key)
        if not progress_data:
            return

        total = progress_data['total']
        start_time = progress_data['start_time']

        # Calculate progress
        percentage = (current / total) * 100 if total > 0 else 0
        elapsed_time = time.time() - start_time

        # Calculate ETA
        if current > 0:
            avg_time_per_item = elapsed_time / current
            remaining_items = total - current
            estimated_remaining = avg_time_per_item * remaining_items
        else:
            estimated_remaining = 0.0

        progress_data.update({
            'current': current,
            'percentage': round(percentage, 1),
            'current_item': current_item,
            'elapsed_time': round(elapsed_time, 1),
            'estimated_remaining': round(estimated_remaining, 1),
            'message': f'Processing {current}/{total} - {current_item}'
        })

        cache.set(self.cache_key, progress_data, self.CACHE_TIMEOUT)

    def complete(self, success=True, message=''):
        """
        Mark task as complete

        Args:
            success: Whether task completed successfully
            message: Completion message
        """
        progress_data = cache.get(self.cache_key)
        if not progress_data:
            return

        elapsed_time = time.time() - progress_data['start_time']

        progress_data.update({
            'status': 'completed' if success else 'failed',
            'percentage': 100.0 if success else progress_data['percentage'],
            'elapsed_time': round(elapsed_time, 1),
            'estimated_remaining': 0.0,
            'message': message or ('Task completed successfully' if success else 'Task failed')
        })

        cache.set(self.cache_key, progress_data, self.CACHE_TIMEOUT)

    def get_progress(self):
        """
        Get current progress data

        Returns:
            dict: Progress information or None if not found
        """
        return cache.get(self.cache_key)

    def cancel(self):
        """
        Cancel the task
        Sets status to 'cancelled' to signal the task to stop
        """
        progress_data = cache.get(self.cache_key)
        if not progress_data:
            return

        progress_data.update({
            'status': 'cancelled',
            'message': 'Task cancelled by user'
        })

        cache.set(self.cache_key, progress_data, self.CACHE_TIMEOUT)

    def is_cancelled(self):
        """
        Check if task has been cancelled

        Returns:
            bool: True if task is cancelled, False otherwise
        """
        progress_data = cache.get(self.cache_key)
        return progress_data and progress_data.get('status') == 'cancelled'

    def clear(self):
        """Clear progress data from cache"""
        cache.delete(self.cache_key)
