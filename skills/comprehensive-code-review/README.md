# Comprehensive Code Review Skill for ACE Engine

A complete code review system for the OpenHarmony ArkUI framework (ACE Engine), covering C++, JavaScript, TypeScript, and ArkTS codebases.

## Features

- **19+ Analysis Dimensions**: Stability, Performance, Threading, Security, Memory, Modern C++, Effective C++, Code Smells, SOLID principles, Design Patterns, Robustness, Testability, Maintainability, Observability, API Design, Technical Debt, and more

- **Automated Analysis**: Python scripts for static code analysis
- **Comprehensive Reports**: Markdown reports with severity levels and actionable recommendations
- **ACE Engine Specific**: Checks for RefPtr usage, architecture compliance, component lifecycle, naming conventions
- **Multi-Language Support**: C++ and TypeScript/ArkTS

## Quick Start

```bash
# Analyze code
python scripts/analyze_code.py path/to/code --recursive --output results.json

# Generate report
python scripts/generate_report.py --analysis results.json --output review_report.md
```

## Documentation

- **[SKILL.md](SKILL.md)** - Main skill documentation
- **[Quick Start Guide](assets/QUICKSTART.md)** - Getting started tutorial
- **[references/DIMENSIONS.md](references/DIMENSIONS.md)** - Quick reference for all dimensions

## Reference Documentation

Detailed guides for each dimension:

- **[STABILITY.md](references/STABILITY.md)** - Error handling, boundary conditions
- **[PERFORMANCE.md](references/PERFORMANCE.md)** - Algorithm complexity, optimization
- **[THREADING.md](references/THREADING.md)** - Concurrency, synchronization
- **[SECURITY.md](references/SECURITY.md)** - Input validation, vulnerabilities
- **[MEMORY.md](references/MEMORY.md)** - Smart pointers, leaks, ownership
- **[CODE_SMELLS.md](references/CODE_SMELLS.md)** - 22 types of code smells
- **[SOLID.md](references/SOLID.md)** - Five design principles
- **[ACE_ENGINE_SPECIFIC.md](references/ACE_ENGINE_SPECIFIC.md)** - Project-specific rules

## Scripts

- **analyze_code.py** - Automated static analysis
- **generate_report.py** - Report generation from analysis results

## Assets

- **report_template.md** - Customizable report template
- **QUICKSTART.md** - Usage examples and workflows

## Dimension Coverage

| Dimension | Focus | Severity Levels |
|-----------|-------|----------------|
| Stability | Error handling, boundaries | CRITICAL, HIGH, MEDIUM, LOW |
| Performance | Algorithms, efficiency | CRITICAL, HIGH, MEDIUM, LOW |
| Threading | Data races, deadlocks | CRITICAL, HIGH, MEDIUM |
| Security | Input validation, vulnerabilities | CRITICAL, HIGH, MEDIUM |
| Memory | Smart pointers, leaks | CRITICAL, HIGH, MEDIUM |
| Modern C++ | C++11/14/17/20 features | HIGH, MEDIUM, LOW |
| Code Smells | Design issues (22 types) | HIGH, MEDIUM, LOW |
| SOLID | Design principles | HIGH, MEDIUM, LOW |
| Architecture | ACE Engine compliance | CRITICAL, HIGH, MEDIUM |

## Usage Examples

### Review a PR
```bash
analyze_code.py path/to/pr/code --recursive --output pr_analysis.json
generate_report.py --analysis pr_analysis.json --output pr_review.md
```

### Security Audit
```bash
analyze_code.py . --dimension Security --recursive --output security_audit.json
```

### Memory Check
```bash
analyze_code.py . --dimension Memory --recursive --output memory_check.json
```

## Integration

### Pre-commit Hook
```bash
#!/bin/bash
analyze_code.py $CHANGED_FILES --output commit_review.json
# Check for critical issues
if grep -q '"severity": "CRITICAL"' commit_review.json; then
    echo "CRITICAL issues found!"
    exit 1
fi
```

### CI/CD Pipeline
```yaml
code_review:
  script:
    - analyze_code.py . --recursive --output review.json
    - generate_report.py --analysis review.json --output report.md
```

## ACE Engine Specific Checks

- ✅ Four-layer architecture compliance
- ✅ Pattern/Model/Property separation
- ✅ RefPtr usage (MakeRefPtr, DynamicCast)
- ✅ WeakPtr for breaking cycles
- ✅ Safe callback captures (WeakClaim)
- ✅ Component lifecycle methods
- ✅ Naming conventions (PascalCase, snake_case_)

## Severity Guidelines

🔴 **CRITICAL** - Must fix before merge
- Memory leaks, crashes, security vulnerabilities

🟠 **HIGH** - Should fix before merge
- Performance issues, API violations, SOLID violations

🟡 **MEDIUM** - Fix soon
- Code smells, style violations

🟢 **LOW** - Nice to have
- Comments, minor optimizations

## Contributing

When adding new checks:
1. Update `scripts/analyze_code.py`
2. Add documentation to `references/`
3. Update this README
4. Test with real code

## License

Part of ACE Engine project. Follows project license.

## Support

For issues or questions, please refer to:
- ACE Engine documentation
- Project knowledge base in `docs/`
- Component-specific guides in `docs/pattern/`

---

**Version:** 1.0.0
**Last Updated:** 2025-01-27
**Compatible with:** ACE Engine (OpenHarmony ArkUI Framework)
