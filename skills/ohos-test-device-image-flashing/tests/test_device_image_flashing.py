import importlib.util
import io
import subprocess
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


SKILL_DIR = Path(__file__).resolve().parents[1]
download_daily = load_module("download_daily", SKILL_DIR / "download_daily.py")
flash_device = load_module("flash_device", SKILL_DIR / "flash_device.py")


class DeviceImageFlashingTest(unittest.TestCase):
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

    def test_safe_extract_rejects_link_members(self):
        with tempfile.TemporaryDirectory() as td:
            archive = Path(td) / "image.tar.gz"
            with tarfile.open(archive, "w:gz") as tf:
                info = tarfile.TarInfo("escape-link")
                info.type = tarfile.SYMTYPE
                info.linkname = "/tmp"
                tf.addfile(info)

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
        self.assertFalse(args.yes)
        self.assertFalse(args.allow_fallback_partitions)

    def test_confirm_flash_requires_exact_confirmation(self):
        parser = flash_device.build_arg_parser()
        args = parser.parse_args([])

        with patch("builtins.input", return_value="no"):
            with self.assertRaises(RuntimeError):
                flash_device.confirm_flash(args)

        with patch("builtins.input", return_value="FLASH"):
            flash_device.confirm_flash(args)

    def test_confirm_flash_can_be_skipped_with_yes(self):
        parser = flash_device.build_arg_parser()
        args = parser.parse_args(["--yes"])

        with patch("builtins.input") as prompt:
            flash_device.confirm_flash(args)

        prompt.assert_not_called()

    def test_hdc_cmd_raises_when_command_fails(self):
        failed = subprocess.CompletedProcess(
            args=["hdc", "shell", "reboot"], returncode=1,
            stdout="", stderr="device offline"
        )

        with patch.object(subprocess, "run", return_value=failed):
            with self.assertRaises(RuntimeError) as cm:
                flash_device.hdc_cmd("hdc", "shell", "reboot")

        self.assertIn("device offline", str(cm.exception))

    def test_flash_userdata_writes_from_temp_file_and_verifies_sync(self):
        calls = []

        def fake_hdc_cmd(hdc, *args):
            calls.append((hdc, *args))

        with tempfile.TemporaryDirectory() as td:
            img_dir = Path(td)
            userdata = img_dir / "userdata.img"
            userdata.write_bytes(b"userdata")

            with patch.object(flash_device, "hdc_cmd", side_effect=fake_hdc_cmd):
                flash_device.flash_userdata("hdc", str(img_dir), ("userdata.img", "userdata"))

        self.assertEqual(calls, [
            ("hdc", "shell", "umount /data"),
            ("hdc", "file", "send", str(userdata), "/tmp/userdata.img"),
            ("hdc", "shell", "dd if=/tmp/userdata.img of=/dev/block/by-name/userdata bs=4M"),
            ("hdc", "shell", "sync /dev/block/by-name/userdata"),
            ("hdc", "shell", "rm -f /tmp/userdata.img"),
        ])


if __name__ == "__main__":
    unittest.main()
