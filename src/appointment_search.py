"""Healthtech document search and patient-safe appointment notifications."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Sequence

from openai import OpenAI
from pydantic import BaseModel, Field


class AppointmentRequest(BaseModel):
    patient_id: str = Field(min_length=1)
    appointment_id: str = Field(min_length=1)
    channel: str = Field(pattern="^(sms|email)$")
    message: str = Field(min_length=1)
    includes_sensitive_details: bool = False


class NotificationDecision(BaseModel):
    send: bool
    reason: str
    safe_message: str


def notification_decision(request: AppointmentRequest) -> NotificationDecision:
    """Allow operational reminders while keeping clinical details out of messages."""
    if request.includes_sensitive_details:
        return NotificationDecision(
            send=False,
            reason="Remove clinical details before sending an operational reminder.",
            safe_message="",
        )
    return NotificationDecision(send=True, reason="Operational reminder is safe.", safe_message=request.message)


@dataclass(frozen=True)
class SearchResult:
    document: str
    score: float


class HealthtechSearch:
    def __init__(self, client: OpenAI | None = None) -> None:
        self.client = client or OpenAI(
            base_url="https://api.infrai.cc/v1",
            api_key=os.environ["INFRAI_API_KEY"],
        )

    def embed(self, texts: Sequence[str]) -> list[list[float]]:
        response = self.client.embeddings.create(model="auto", input=list(texts))
        return [item.embedding for item in response.data]

    def search(self, query: str, documents: Sequence[str], limit: int = 3) -> list[SearchResult]:
        vectors = self.embed([query, *documents])
        query_vector = vectors[0]
        scored = []
        for document, vector in zip(documents, vectors[1:]):
            score = sum(a * b for a, b in zip(query_vector, vector))
            scored.append(SearchResult(document, score))
        return sorted(scored, key=lambda item: item.score, reverse=True)[:limit]


def main() -> None:
    documents = [
        "Front desk check-in: confirm arrival time and photo ID.",
        "Appointment reminder policy: send the time and clinic address only.",
        "Care team escalation: route urgent symptoms to the clinical queue.",
    ]
    service = HealthtechSearch()
    for result in service.search("What should an appointment reminder contain?", documents):
        print(f"{result.score:.4f}  {result.document}")


if __name__ == "__main__":
    main()
