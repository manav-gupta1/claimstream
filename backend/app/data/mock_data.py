from typing import Any, Dict, List, Optional

MOCK_CASES: Dict[str, Dict[str, Any]] = {
    "CASE_001": {
        "case_id": "CASE_001",
        "title": "Knee Arthroscopy - Complete Conservative Therapy Log",
        "query": (
            "TPA Request for Claim #CLM-89211: Please provide documented clinical evidence "
            "of at least 6 weeks of failed conservative physical therapy prior to approving "
            "Right Knee Arthroscopic Partial Meniscectomy performed on 2026-08-15."
        ),
        "patient_id": "PAT-1001",
        "expected_result": "VERIFIED",
        "expected_confidence_min": 90.0,
        "patient_data": {
            "resourceType": "Bundle",
            "type": "collection",
            "patient": {
                "id": "PAT-1001",
                "name": "Eleanor Vance",
                "gender": "female",
                "birthDate": "1978-04-12",
            },
            "entry": [
                {
                    "resourceType": "Condition",
                    "id": "COND-101",
                    "clinicalStatus": "active",
                    "verificationStatus": "confirmed",
                    "code": "ICD-10 M23.22 - Derangement of meniscus due to old tear or injury, right knee",
                    "onsetDateTime": "2026-05-10",
                    "recordedDate": "2026-05-12",
                },
                {
                    "resourceType": "Encounter",
                    "id": "ENC-101",
                    "status": "finished",
                    "class": "AMB",
                    "type": "Initial Orthopedic Evaluation",
                    "period": {"start": "2026-05-15T09:00:00Z"},
                    "reasonCode": ["Right knee pain and mechanical catching"],
                    "note": [
                        (
                            "Patient presents with persistent right knee pain following strain. "
                            "Prescribed 6-8 weeks of structured physical therapy, NSAIDs, and activity modification."
                        )
                    ],
                },
                {
                    "resourceType": "Procedure",
                    "id": "PROC-PT-SERIES",
                    "status": "completed",
                    "code": "CPT 97110 - Therapeutic Exercises (Physical Therapy)",
                    "performedPeriod": {
                        "start": "2026-05-20",
                        "end": "2026-07-22",
                    },
                    "note": [
                        "Completed 10 sessions of physical therapy over 9 weeks. Patient demonstrated minimal pain relief (VAS 7/10). Failed conservative therapy."
                    ],
                },
                {
                    "resourceType": "Observation",
                    "id": "OBS-MRI-101",
                    "status": "final",
                    "code": "Diagnostic Imaging - Right Knee MRI",
                    "effectiveDateTime": "2026-07-25",
                    "valueString": "Complex tear of posterior horn of right medial meniscus. Moderate joint effusion.",
                },
                {
                    "resourceType": "Procedure",
                    "id": "PROC-SURGERY-101",
                    "status": "completed",
                    "code": "CPT 29881 - Arthroscopy, knee, surgical; with meniscectomy",
                    "performedDateTime": "2026-08-15",
                    "note": ["Right knee arthroscopic partial medial meniscectomy performed without complications."],
                },
            ],
        },
    },
    "CASE_002": {
        "case_id": "CASE_002",
        "title": "Lumbar Spine MRI - Missing Conservative Therapy & Date Discrepancy",
        "query": (
            "TPA Clarification for Claim #CLM-94022: Requesting 6 weeks of conservative treatment logs "
            "and detailed symptom onset timeline for Lumbar Spine MRI requested on 2026-08-20 "
            "due to suspected L4-L5 herniation."
        ),
        "patient_id": "PAT-2004",
        "expected_result": "NEEDS_REVIEW",
        "expected_confidence_max": 80.0,
        "patient_data": {
            "resourceType": "Bundle",
            "type": "collection",
            "patient": {
                "id": "PAT-2004",
                "name": "Marcus Brody",
                "gender": "male",
                "birthDate": "1985-11-03",
            },
            "entry": [
                {
                    "resourceType": "Condition",
                    "id": "COND-201",
                    "clinicalStatus": "active",
                    "verificationStatus": "unconfirmed",
                    "code": "ICD-10 M54.5 - Low back pain",
                    "onsetDateTime": "2026-08-01",  # Conflict 1: Onset date 2026-08-01
                    "note": ["Patient reports severe low back pain starting 2026-08-01 after heavy lifting."],
                },
                {
                    "resourceType": "Encounter",
                    "id": "ENC-201",
                    "status": "finished",
                    "class": "AMB",
                    "type": "PCP Intake Note",
                    "period": {"start": "2026-08-05T10:30:00Z"},
                    "note": [
                        (
                            "Patient states low back pain with radiculopathy began 4 months ago (2026-04-10). "  # Conflict 2: Onset date 2026-04-10
                            "Prescribed muscle relaxants and recommended physical therapy."
                        )
                    ],
                },
                {
                    "resourceType": "Procedure",
                    "id": "PROC-PT-SHORT",
                    "status": "in-progress",
                    "code": "CPT 97110 - Physical Therapy Exercises",
                    "performedPeriod": {
                        "start": "2026-08-08",
                        "end": "2026-08-18",
                    },
                    "note": [
                        "Attended 2 sessions of physical therapy over 10 days. Patient discontinued due to work schedule. (Incomplete conservative therapy)."
                    ],
                },
                {
                    "resourceType": "Observation",
                    "id": "OBS-MRI-REQ",
                    "status": "preliminary",
                    "code": "Order - Lumbar Spine MRI",
                    "effectiveDateTime": "2026-08-20",
                    "valueString": "MRI ordered prior to completing required 6-week conservative physical therapy regimen.",
                },
            ],
        },
    },
}


def list_mock_cases() -> List[Dict[str, Any]]:
    """Return summary list of all available mock cases."""
    return [
        {
            "case_id": case["case_id"],
            "title": case["title"],
            "query": case["query"],
            "patient_id": case["patient_id"],
            "expected_result": case["expected_result"],
        }
        for case in MOCK_CASES.values()
    ]


def get_mock_case(case_id: str) -> Optional[Dict[str, Any]]:
    """Retrieve full mock case dictionary by case_id."""
    return MOCK_CASES.get(case_id)
