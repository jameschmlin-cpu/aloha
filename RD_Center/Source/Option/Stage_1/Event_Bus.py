import collections
class EventBus:
    def __init__(self): self._subscribers = collections.defaultdict(list)
    def subscribe(self, event_type, callback): self._subscribers[event_type].append(callback)
    def publish(self, event_type, data):
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]: callback(data)
global_bus = EventBus()