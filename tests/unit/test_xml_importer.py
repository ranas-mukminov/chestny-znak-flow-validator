from pathlib import Path

import pytest
from defusedxml.common import DefusedXmlException

from cz_validator.io_import.mapping_profiles import MappingProfile
from cz_validator.io_import.xml_importer import load_retail_export


SAMPLE_XML = """
<root>
  <movement>
    <code>XML1</code>
    <gtin>999</gtin>
    <batch>BATCH-9</batch>
    <status>AT_RETAIL</status>
    <owner>RET</owner>
  </movement>
  <movement>
    <code>XML2</code>
    <gtin>999</gtin>
    <batch>BATCH-9</batch>
    <status>WITHDRAWN</status>
    <owner>RET</owner>
  </movement>
</root>
"""


def test_load_retail_export(tmp_path: Path):
    xml_path = tmp_path / "retail.xml"
    xml_path.write_text(SAMPLE_XML)
    profile = MappingProfile(
        tag_mappings={
            "code": "code",
            "gtin": "gtin",
            "batch_id": "batch",
            "status": "status",
            "owner_id": "owner",
        }
    )
    codes = load_retail_export(xml_path, profile)
    assert len(codes) == 2
    assert codes[0].code == "XML1"
    assert codes[1].status.name == "WITHDRAWN"


def test_malicious_xml_entities_rejected(tmp_path: Path):
    malicious = """
    <!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
    <root>
      <movement>
        <code>&xxe;</code>
      </movement>
    </root>
    """
    xml_path = tmp_path / "malicious.xml"
    xml_path.write_text(malicious)
    profile = MappingProfile(tag_mappings={"code": "code"})

    with pytest.raises(DefusedXmlException):
        load_retail_export(xml_path, profile)
