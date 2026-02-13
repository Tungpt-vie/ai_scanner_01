from datetime import datetime
from typing import Dict

from scanner.observation.state_transition import (
    ObservationState,
    ObservationStateTransition,
)


class ObservationRecord:
    """
    In-memory observation record.

    Rules:
    - Independent from TA core
    - No escalation to STANDARD
    - No reopen after CLOSED
    """

    def __init__(self, observation_id: str):
        self.observation_id = observation_id
        self.state = ObservationState.OPEN
        self.created_at = datetime.utcnow()
        self.updated_at = self.created_at

    def to_dict(self):
        return {
            "observation_id": self.observation_id,
            "state": self.state.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


class ObservationLifecycleManager:
    """
    Controls observation lifecycle strictly via state machine.
    """

    def __init__(self):
        self._records: Dict[str, ObservationRecord] = {}
        self._transition = ObservationStateTransition()

    def create(self, observation_id: str) -> ObservationRecord:
        if observation_id in self._records:
            raise ValueError("OBSERVATION_ALREADY_EXISTS")

        record = ObservationRecord(observation_id)
        self._records[observation_id] = record
        return record

    def get(self, observation_id: str) -> ObservationRecord:
        if observation_id not in self._records:
            raise ValueError("OBSERVATION_NOT_FOUND")
        return self._records[observation_id]

    def transition(self, observation_id: str, new_state: ObservationState):
        record = self.get(observation_id)

        # Validate state transition
        self._transition.validate(record.state, new_state)

        # Apply transition
        record.state = new_state
        record.updated_at = datetime.utcnow()

    def list_all(self):
        return [record.to_dict() for record in self._records.values()]
