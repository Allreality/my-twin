# FILE: emotional_state.py

from enum import Enum
from datetime import datetime, timedelta

class Emotion(Enum):
    NEUTRAL = "neutral"
    HAPPY = "happy"
    SAD = "sad"
    EXCITED = "excited"
    ANXIOUS = "anxious"
    CONTENT = "content"
    CONTEMPLATIVE = "contemplative"

class EmotionalState:
    """Tracks persistent emotional state"""
    
    def __init__(self):
        self.current_emotion = Emotion.NEUTRAL
        self.intensity = 0.5  # 0-1
        self.last_update = datetime.now()
        self.trigger = ""
        self.momentum = 0.5  # How much emotion persists
    
    def update(self, event_sentiment, trigger):
        """Update emotional state based on event"""
        
        # Calculate time decay
        hours_since_update = (datetime.now() - self.last_update).seconds / 3600
        decay = min(hours_since_update * 0.1, 0.5)  # Emotions fade over time
        
        # Apply momentum (emotions don't change instantly)
        current_intensity = self.intensity - decay
        new_intensity = (current_intensity * self.momentum) + (event_sentiment * (1 - self.momentum))
        
        # Determine new emotion
        if new_intensity > 0.6:
            self.current_emotion = Emotion.HAPPY if event_sentiment > 0 else Emotion.SAD
        elif new_intensity > 0.4:
            self.current_emotion = Emotion.CONTENT if event_sentiment > 0 else Emotion.ANXIOUS
        else:
            self.current_emotion = Emotion.NEUTRAL
        
        self.intensity = new_intensity
        self.last_update = datetime.now()
        self.trigger = trigger
    
    def get_context(self):
        """Get emotional context for Claude"""
        hours_since = (datetime.now() - self.last_update).seconds / 3600
        
        context = f"""Current emotional state:
Emotion: {self.current_emotion.value}
Intensity: {self.intensity:.1f}/1.0
Trigger: {self.trigger}
Duration: {hours_since:.1f} hours

Respond in a way that reflects this emotional state.
"""
        return context

# Usage:
emotion = EmotionalState()

# When user shares sad news:
emotion.update(event_sentiment=-0.7, trigger="user's dog passed away")

# Include in Claude context:
emotional_context = emotion.get_context()