from typing import List, Dict


class ObservationHistorySerializer:
    """
    Safe serializer for CLOSED observation history.

    Rules:
    - No internal object exposure
    - No mutation fields
    - No PII
    - Archived view only
    """

    def serialize(self, observation: Dict) -> Dict:
        return {
            "observation_id": observation.get("observation_id"),
            "state": observation.get("state"),
            "created_at": observation.get("created_at"),
            "updated_at": observation.get("updated_at"),
        }

    def serialize_list(self, observations: List[Dict]) -> List[Dict]:
        return [self.serialize(o) for o in observations]
