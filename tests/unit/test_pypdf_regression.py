import signal
import time
from io import BytesIO

from pypdf import PdfReader, PdfWriter
from pypdf.generic import DecodedStreamObject, NameObject


class Timeout(Exception):
    pass


def _create_malicious_pdf() -> bytes:
    writer = PdfWriter()
    page = writer.add_blank_page(width=100, height=100)
    stream = DecodedStreamObject()
    stream.set_data(b"% comment without newline")
    page[NameObject("/Contents")] = writer._add_object(stream)
    buffer = BytesIO()
    writer.write(buffer)
    return buffer.getvalue()


def _timeout_handler(signum, frame):  # pragma: no cover - platform guard
    raise Timeout("PDF parsing exceeded allowed time")


def test_pdf_comment_without_newline_is_handled_quickly():
    malicious_pdf = _create_malicious_pdf()
    reader = PdfReader(BytesIO(malicious_pdf))

    signal.signal(signal.SIGALRM, _timeout_handler)
    signal.alarm(1)
    start = time.time()
    try:
        text = reader.pages[0].extract_text()
    finally:
        signal.alarm(0)
    elapsed = time.time() - start

    assert text == ""  # content stream has only a comment
    assert elapsed < 1, "Parsing should complete quickly even on malformed streams"
