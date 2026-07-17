# Quality Assurance

## Automated Testing

This skill includes automated tests to ensure quality.

### Running Tests Locally

```bash
# Run all tests
cd /path/to/skill
python3 tests/run_tests.py

# Run specific test file
python3 tests/test_extract_imports.py
python3 tests/test_map_domain.py
```

### Test Coverage

| Script | Test File | Coverage |
|--------|-----------|----------|
| extract_imports.py | test_extract_imports.py | ✅ import提取、分类 |
| map_domain.py | test_map_domain.py | ✅ API映射、Kit展开 |
| explore_import_chain.py | - | 🚧 待补充 |
| generate_evidence_chain.py | - | 🚧 待补充 |

### CI/CD

Tests are automatically run on:
- Push to main/master branch
- Pull requests to main/master branch

See `.github/workflows/test.yml` for details.

## Quality Checklist

Before releasing:

- [ ] All tests pass
- [ ] No Python syntax errors
- [ ] Scripts have proper error handling
- [ ] Documentation is up to date
- [ ] Database has required tables

## Reporting Issues

If you find a bug or have a suggestion:

1. Check existing issues
2. Create a new issue with:
   - Steps to reproduce
   - Expected behavior
   - Actual behavior
   - Environment details