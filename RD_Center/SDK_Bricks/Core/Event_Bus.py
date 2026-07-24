# -*- coding: utf-8 -*-
# Compiled Brick from: Event_Bus.py
# Category: Core

class EventBusBrick:
    def run(self, ctx=None):
        try:
            import collections
            class EventBus:
                def __init__(self): self._subscribers = collections.defaultdict(list)
                def subscribe(self, event_type, callback): self._subscribers[event_type].append(callback)
                def publish(self, event_type, data):
                    if event_type in self._subscribers:
                        for callback in self._subscribers[event_type]: callback(data)
            global_bus = EventBus()
        except Exception as e:
            print(f"[EventBusBrick] 運行失敗: {e}")
            return False
        return True
