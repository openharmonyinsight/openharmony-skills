import sys
import tempfile
import unittest
import warnings
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_DIR / "scripts"))

from deckbuilder import Deck  # noqa: E402


class DeckBuilderSmokeTest(unittest.TestCase):
    def test_requirement_review_deck_skips_invalid_logo(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            bad_logo = tmp_path / "bad-logo.png"
            bad_logo.write_bytes(b"not a png")
            out = tmp_path / "smoke.pptx"

            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                Deck(logo=str(bad_logo)).requirement_review_deck(
                    {
                        "title": "Skill Eval Smoke",
                        "feature_name": "测试特性",
                        "value": {
                            "background": ["现有流程验证"],
                            "features": ["自动生成固定评审页"],
                            "scope": ["OpenHarmony 需求评审"],
                        },
                        "design": {
                            "design": ["复用 deckbuilder"],
                            "changes": ["无"],
                            "extra": [{"heading": "验证", "lines": ["最小 spec 可生成"]}],
                        },
                        "delivery": {
                            "items": [
                                {"name": "子需求1", "owner": "owner", "workload": "1"}
                            ]
                        },
                    }
                ).save(str(out))

            self.assertTrue(out.exists())
            self.assertGreater(out.stat().st_size, 0)
            self.assertTrue(any("logo" in str(w.message).lower() for w in caught))


if __name__ == "__main__":
    unittest.main()
