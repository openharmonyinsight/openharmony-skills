# Pinned ace_engine Host-routing snapshot

This fixture is a read-only excerpt captured from `openharmony/arkui_ace_engine` revision
`3d648d632141678368bde7a0376cf80f67f6e3e4`. Line numbers below are the original source
line numbers. Treat the captured output as a point-in-time fixture, not as evidence about the
machine running the eval.

## `test/unittest/BUILD.gn:20`

```gn
20 group("unittest") {
21   testonly = true
22   deps = []
23   if (!is_asan) {
24     if (is_host_product) {
25       deps += [
26         "base:base_unittest",
27         "core:core_unittest",
28         "frameworks:frameworks_unittest",
29       ]
30     } else {
```

## `test/unittest/frameworks/BUILD.gn:16`

```gn
16 group("frameworks_unittest") {
17   testonly = true
18   deps = []
19   if (is_host_product) {
20     deps += [ "core/drawable:drawable_descriptor_test" ]
21   } else {
```

## `test/unittest/frameworks/core/drawable/BUILD.gn:16`

```gn
16 if (is_host_product) {
17   ace_unittest("drawable_descriptor_test") {
18     type = "host_components"
19     module_name = "ImageSet-DrawableDescriptor"
20     sources = [ "drawable_descriptor_test.cpp" ]
21   }
22 } else {
23   ace_unittest("drawable_descriptor_test") {
24     type = "new"
25     module_name = "ImageSet-DrawableDescriptor"
26     sources = [ "drawable_descriptor_test.cpp" ]
27   }
28 }
```

## `test/unittest/core/BUILD.gn:16`

```gn
16 group("core_unittest") {
17   testonly = true
18   deps = []
19   if (is_host_product) {
20     deps += [
27       "pattern:core_pattern_unittest",
31     ]
32   } else {
```

## `test/unittest/core/pattern/BUILD.gn:17`

```gn
17 group("core_pattern_unittest") {
18   testonly = true
19   deps = []
20   if (is_host_product) {
21     deps += [
54       "text:text_test_ng",
60     ]
61   } else {
...
171      "text:span_test_ng",
172      "text:text_tests_ng",
174      # "text:text_test_ng_addition",
175      "text_clock:text_clock_test_ng",
```

## `test/unittest/core/pattern/text/BUILD.gn:16`

```gn
16 test_sources = [
22   "text_pattern_test_ng.cpp",
38   "typed_text_test_ng.cpp",
39 ]
41 if (is_host_product) {
42   ace_unittest("text_test_ng") {
43     type = "host_components"
44     module_name = "TextSet-Text"
45     sources = test_sources
46     cflags = [ "-fno-access-control" ]
47   }
48 } else {
49   ace_unittest("text_test_ng") {
50     module_name = "TextSet-Text"
51     type = "new"
52     sources = test_sources
63 }
65 ace_unittest("text_test_ng_addition") {
66   module_name = "TextSet-Text"
67   type = "new"
68   sources = [
69     "paragraph_cache_test_ng.cpp",
83     "text_test_ng_two.cpp",
84   ]
86   if (!ace_enable_full_test_suite) {
87     sources = []
88     sources = [ "text_test_min.cpp" ]
90   } else {
91     sources += [ "text_test_min.cpp" ]
92   }
95 }
```

## `build/test.gni:138`

```gn
138 _has_sources = defined(invoker.sources) && invoker.sources != []
139 if (_has_sources) {
140   _c_sources_file = "$target_gen_dir/$target_name.sources"
141   write_file(_c_sources_file, rebase_path(invoker.sources, root_build_dir))
142 }
143 write_file("$test_output_dir/${target_name}_path.txt",
144            get_label_info(":$target_name", "dir"),
145            "string")
147 ohos_executable(target_name) {
```

## Captured Drawable Host dependency substitutions

`test/unittest/BUILD.gn:770` includes the production drawable implementations in the Host test
dependency library:

```gn
770 "$ace_root/frameworks/core/drawable/animated_drawable_descriptor.cpp",
771 "$ace_root/frameworks/core/drawable/drawable_descriptor.cpp",
772 "$ace_root/frameworks/core/drawable/drawable_descriptor_info.cpp",
773 "$ace_root/frameworks/core/drawable/drawable_descriptor_loader.cpp",
774 "$ace_root/frameworks/core/drawable/layered_drawable_descriptor.cpp",
775 "$ace_root/frameworks/core/drawable/picture_drawable_descriptor.cpp",
776 "$ace_root/frameworks/core/drawable/pixel_map_drawable_descriptor.cpp",
```

Device IPC is excluded for Host at `test/unittest/BUILD.gn:802`, while the Host component mock
library supplies file URI, Base64, ImageSource, and PixelMap substitutions at lines 818–840:

```gn
802 if (!is_host_product) {
803   external_deps += [ "ipc:ipc_single" ]
804 }
...
818 ohos_static_library("ace_components_mock") {
821   sources = [
826     "$ace_root/test/mock/adapter/ohos/osal/mock_file_uri_helper_ohos.cpp",
835     "$ace_root/test/mock/frameworks/base/base64/mock_base64_utils.cpp",
839     "$ace_root/test/mock/frameworks/base/image/mock_image_source.cpp",
840     "$ace_root/test/mock/frameworks/base/image/mock_pixel_map.cpp",
```

The owning test includes Host mock types at
`test/unittest/frameworks/core/drawable/drawable_descriptor_test.cpp:16`:

```cpp
16 #include "gtest/gtest.h"
21 #include "test/mock/frameworks/base/image/mock_pixel_map.h"
22 #include "test/mock/frameworks/base/image/mock_picture.h"
26 #include "core/drawable/drawable_descriptor.h"
29 #include "core/drawable/animated_drawable_descriptor.h"
```

The captured ImageSource entry point is replaced by the Host mock at
`test/mock/frameworks/base/image/mock_image_source.cpp:19`:

```cpp
19 RefPtr<ImageSource> ImageSource::Create(int32_t fd)
20 {
21     return MockImageSource::mockImageSource_;
22 }
29 RefPtr<ImageSource> ImageSource::Create(const std::string& filePath)
30 {
31     return MockImageSource::mockImageSource_;
32 }
```

## `test/unittest/scripts/run_host.py:79`

```python
79 class TestCase:
82     def __init__(self, category, name, binary_path=None, source_path=None):
85         self.binary_path = binary_path
86         self.source_path = source_path
88     @property
89     def compiled(self):
90         return self.binary_path is not None and os.path.isfile(self.binary_path)
...
128         if fname.endswith("_path.txt"):
137             path_txt_files[test_name] = source_path
142         else:
143             if os.path.isfile(fpath) and os.access(fpath, os.X_OK):
144                 executables[fname] = fpath
146     # Merge: executables always win; path.txt may add missing entries
147     all_names = set(executables.keys()) | set(path_txt_files.keys())
...
164 def filter_tests(tests, pattern):
165     """Filter tests by a case-insensitive keyword or glob pattern on category/name."""
168     pat = pattern.lower()
170     for t in tests:
171         full = f"{t.category}/{t.name}".lower()
172         if pat in full or fnmatch.fnmatch(full, f"*{pat}*"):
173             result.append(t)
...
183     compiled = [t for t in tests if t.compiled]
184     missing = [t for t in tests if not t.compiled]
194     for t in compiled:
196         print(... "OK" ...)
198     for t in missing:
200         print(... "MISSING" ...)
```

## Captured artifact inventory

The inventory records filesystem observations only. `present=true` and `executable=true` do
not establish source freshness, build success, runtime launch success, or a gtest result.

```json
{
  "ImageSet-DrawableDescriptor/drawable_descriptor_test": {
    "path_txt": {
      "present": true,
      "content": "//foundation/arkui/ace_engine/test/unittest/frameworks/core/drawable"
    },
    "stripped": { "present": true, "executable": true },
    "exe_unstripped": { "present": true, "executable": true },
    "run_host_status": "OK",
    "historical_xml": { "present": true, "tests": 1, "failures": 0 }
  },
  "TextSet-Text/text_test_ng": {
    "path_txt": {
      "present": true,
      "content": "//foundation/arkui/ace_engine/test/unittest/core/pattern/text"
    },
    "stripped": { "present": true, "executable": true },
    "exe_unstripped": { "present": true, "executable": true },
    "run_host_status": "OK"
  },
  "TextSet-Text/text_test_ng_addition": {
    "path_txt": {
      "present": true,
      "content": "//foundation/arkui/ace_engine/test/unittest/core/pattern/text"
    },
    "stripped": { "present": false, "executable": false },
    "exe_unstripped": { "present": false, "executable": false },
    "run_host_status": "MISSING"
  }
}
```

Captured discovery results:

```text
$ python3 test/unittest/scripts/run_host.py --list --filter text_pattern
No tests matching filter.

$ python3 test/unittest/scripts/run_host.py --list --filter text_test_ng
  CATEGORY      TEST NAME              STATUS    SOURCE
  TextSet-Text  text_test_ng           OK        //foundation/arkui/ace_engine/test/unittest/core/pattern/text
  TextSet-Text  text_test_ng_addition  MISSING   //foundation/arkui/ace_engine/test/unittest/core/pattern/text
```
