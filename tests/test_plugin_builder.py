import unittest
import zipfile
from io import BytesIO

from backend.app.plugin_builder import build_paper_plugin


class PaperPluginBuilderTests(unittest.TestCase):
    def test_creates_expected_source_archive(self):
        result = build_paper_plugin("Hello World", "com.example.hello", "1.0.0", "1.21.4")
        with zipfile.ZipFile(BytesIO(result)) as archive:
            names = set(archive.namelist())
            self.assertIn("HelloWorld/pom.xml", names)
            self.assertIn("HelloWorld/src/main/java/com/example/hello/HelloWorld.java", names)
            descriptor = archive.read("HelloWorld/src/main/resources/plugin.yml").decode()
            self.assertIn("api-version: '1.21'", descriptor)

    def test_rejects_invalid_package(self):
        with self.assertRaises(ValueError):
            build_paper_plugin("Demo", "bad-package", "1.0.0", "1.21.4")

    def test_rejects_invalid_version(self):
        with self.assertRaises(ValueError):
            build_paper_plugin("Demo", "com.example.demo", "v1", "1.21.4")

    def test_rejects_invalid_minecraft_version(self):
        with self.assertRaises(ValueError):
            build_paper_plugin("Demo", "com.example.demo", "1.0.0", "latest")


if __name__ == "__main__":
    unittest.main()
