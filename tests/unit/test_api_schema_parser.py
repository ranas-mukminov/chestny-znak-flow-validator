from cz_validator.io_import.api_schema_parser import parse_api_response


def test_parse_api_response_extracts_codes():
    payload = {
        "items": [
            {
                "code": "API1",
                "status": "INTRODUCED",
                "owner": "PROD",
                "gtin": "777",
                "batch_id": "B7",
            },
            {
                "code": "API2",
                "status": "IN_TRANSIT",
                "owner": "WHOLE",
                "gtin": "777",
                "batch_id": "B7",
            },
        ]
    }
    codes = parse_api_response(payload)
    assert len(codes) == 2
    assert codes[0].code == "API1"
    assert codes[1].status.name == "IN_TRANSIT"
