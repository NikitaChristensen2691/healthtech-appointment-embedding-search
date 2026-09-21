from src.appointment_search import AppointmentRequest, notification_decision


def test_sensitive_appointment_details_are_blocked() -> None:
    request = AppointmentRequest(
        patient_id="p-42",
        appointment_id="a-17",
        channel="sms",
        message="Your oncology appointment is tomorrow at 10:00.",
        includes_sensitive_details=True,
    )

    decision = notification_decision(request)

    assert decision.send is False
    assert decision.safe_message == ""


def test_plain_operational_reminder_is_allowed() -> None:
    request = AppointmentRequest(
        patient_id="p-42",
        appointment_id="a-17",
        channel="email",
        message="Your appointment is tomorrow at 10:00 at Main Clinic.",
    )

    assert notification_decision(request).send is True
