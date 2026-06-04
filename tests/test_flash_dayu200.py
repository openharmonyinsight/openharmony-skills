import importlib.util
import io
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


download_daily = load_module("download_daily", ROOT / "skills" / "flash-dayu200" / "download_daily.py")
flash_device = load_module("flash_device", ROOT / "skills" / "flash-dayu200" / "flash_device.py")


class FlashDayu200Test(unittest.TestCase):
    def test_safe_extract_rejects_path_traversal_member(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "image.tar.gz"
            with tarfile.open(archive, "w:gz") as tf:
                info = tarfile.TarInfo("../escape.txt")
                data = b"escape"
                info.size = len(data)
                tf.addfile(info, io.BytesIO(data))

            with tarfile.open(archive) as tf:
                with self.assertRaises(ValueError):
                    download_daily.safe_extract(tf, Path(td) / "out")

    def test_download_default_output_dir_is_not_desktop_bound(self):
        parser = download_daily.build_arg_parser()
        args = parser.parse_args([])

        self.assertEqual(args.output_dir, "daily_build")

    def test_flash_default_image_dir_is_not_desktop_bound(self):
        parser = flash_device.build_arg_parser()
        args = parser.parse_args([])

        self.assertEqual(args.img_dir, "daily_build")

    def test_hdc_cmd_raises_when_command_fails(self):
        failed = subprocess.CompletedProcess(
            args=["hdc", "shell", "reboot"], returncode=1,
            stdout="", stderr="device offline"
        )

        with patch.object(subprocess, "run", return_value=failed):
            with self.assertRaises(RuntimeError) as cm:
                flash_device.hdc_cmd("hdc", "shell", "reboot")

        self.assertIn("device offline", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
