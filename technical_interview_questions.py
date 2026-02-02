"""
Implement a specimen batch queue with priority processing.
Each specimen has:
- id: str
- priority: int (1=highest, 3=lowest) 1,2,3
- collection_time: datetime (30 days, after that it will damage)

Requirements:
- Process highest priority specimens first  (combination of priority and collection_time)
- Within same priority, process oldest specimens first 
- Return next batch of k specimens to process (k is next batch, which is integer)

Example 1:
specimens = [
    {"id": "A", "priority": 2, "collection_time": "2024-01-01 09:00"},
    {"id": "B", "priority": 1, "collection_time": "2024-01-01 10:00"},
    {"id": "C", "priority": 1, "collection_time": "2024-01-01 08:00"}
]
k = 2
Output: ["C", "B"]  # Priority 1 specimens, oldest first 

- first check priority and collection_time

Example 2:
specimens = [
    {"id": "A", "priority": 3, "collection_time": "2024-01-01 09:00"},
    {"id": "B", "priority": 3, "collection_time": "2024-01-01 10:00"} 
]
k = 1
Output: ["A"]  # Same priority, oldest first
"""

from datetime import datetime
from typing import List

def get_next_batch(specimens: List[dict], k: int) -> List[str]:
    priority_map = {}

    # separate based on priority
    for index, specimen in enumerate(specimens):
        specimens[index]["collection_time"] = datetime.strptime(
            specimen["collection_time"], "%Y-%m-%d %H:%M"
        )

        if specimen["priority"] in priority_map:
            priority_map[specimen["priority"]].append(specimen["collection_time"])
        else:
            priority_map[specimen["priority"]] = [specimen["collection_time"]]

    # sort dictionary based on keys
    priority_map = dict(sorted(priority_map.items()))

    # flatten priority and collection_time into a list of tuples
    sorted_pairs = []
    for priority, times in priority_map.items():
        priority_map[priority] = sorted(times)

        for collection_time in priority_map[priority]:
            sorted_pairs.append((priority, collection_time))

    # dummy list of the same length as sorted_pairs
    batch = [0] * len(sorted_pairs)

    # find index and push id to the same index in batch
    for specimen in specimens:
        pair_index = sorted_pairs.index(
            (specimen["priority"], specimen["collection_time"])
        )
        batch[pair_index] = specimen["id"]

    return batch[:k]


specimens = [
    {"id": "A", "priority": 2, "collection_time": "2024-01-01 09:00"},
    {"id": "B", "priority": 1, "collection_time": "2024-01-01 10:00"},
    {"id": "C", "priority": 1, "collection_time": "2024-01-01 08:00"}
]
k = 2
print(get_next_batch(specimens, k))