"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'segments.csv': ['edition', 'segment', 'previous', 'from_sec', 'to_sec', 'rev'], 'rooms.csv': ['show', 'round', 'room', 'date', 'capacity', 'edition', 'segments'], 'assignments.csv': ['allocation', 'viewer', 'show', 'stratum', 'status'], 'attendance.csv': ['viewer', 'show', 'observed_start', 'observed_end', 'prior_edition', 'prior_segment', 'known_on'], 'forms.csv': ['form', 'viewer', 'show', 'segment', 'score'], 'availability.csv': ['viewer', 'can_attend', 'stratum', 'screened', 'requires_access'], 'room_capability.csv': ['room', 'accessible_seats']}
REFERENCES = [('assignments.csv', 'show', 'rooms.csv', 'show'), ('attendance.csv', 'show', 'rooms.csv', 'show'), ('forms.csv', 'show', 'rooms.csv', 'show'), ('rooms.csv', 'edition', 'segments.csv', 'edition'), ('rooms.csv', 'room', 'room_capability.csv', 'room')]
OBSERVED_VALUES = [('attendance.csv', 'viewer', 'V4', 2), ('segments.csv', 'segment', 'arrival', 3), ('assignments.csv', 'viewer', 'V1', 2)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
