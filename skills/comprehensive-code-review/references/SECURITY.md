# Security Code Review Guidelines

## Overview

Security focuses on preventing vulnerabilities, protecting sensitive data, and ensuring safe handling of user input. Security issues are often CRITICAL severity as they can lead to exploits.

## Critical Security Vulnerabilities

### 1. Command Injection

**Severity:** 🔴 CRITICAL

**Description:** Attacker can execute arbitrary commands

**Detection:**
```cpp
// ❌ CRITICAL: Command injection
std::string command = "ls " + user_input;
system(command.c_str());

// ❌ CRITICAL: Command injection via popen
FILE* fp = popen(user_input.c_str(), "r");

// ❌ CRITICAL: Shell command execution
execl("/bin/sh", "sh", "-c", user_input.c_str(), NULL);
```

**Fix:**
```cpp
// ✅ GOOD: Whitelist validation
bool IsValidFileName(const std::string& name) {
    // Only allow alphanumeric, underscore, dot
    return std::all_of(name.begin(), name.end(),
        [](char c) {
            return std::isalnum(c) || c == '_' || c == '.' || c == '-';
        });
}

// ✅ GOOD: Use safe APIs
posix_spawnp(...);  // No shell involved
// Or use library functions instead of shell commands

// ✅ GOOD: Input sanitization
std::string SanitizePath(const std::string& path) {
    std::string result;
    for (char c : path) {
        if (std::isalnum(c) || c == '/' || c == '.' || c == '_' || c == '-') {
            result += c;
        }
    }
    return result;
}
```

---

### 2. SQL Injection

**Severity:** 🔴 CRITICAL

**Description:** Attacker can manipulate database queries

**Detection:**
```cpp
// ❌ CRITICAL: SQL injection
std::string query = "SELECT * FROM users WHERE name = '" + username + "'";
db.Execute(query.c_str());

// ❌ CRITICAL: SQL injection
char query[256];
snprintf(query, sizeof(query),
         "SELECT * FROM items WHERE id = %s", user_input.c_str());
db.Execute(query);
```

**Fix:**
```cpp
// ✅ GOOD: Parameterized queries
// Using prepared statements
sqlite3_stmt* stmt;
sqlite3_prepare_v2(db,
    "SELECT * FROM users WHERE name = ?",
    -1, &stmt, NULL);
sqlite3_bind_text(stmt, 1, username.c_str(), -1, SQLITE_TRANSIENT);
sqlite3_step(stmt);
```

---

### 3. Buffer Overflow

**Severity:** 🔴 CRITICAL

**Description:** Writing beyond allocated memory bounds

**Detection:**
```cpp
// ❌ CRITICAL: Buffer overflow
char buffer[10];
strcpy(buffer, user_input);  // No bounds checking
scanf("%s", buffer);         // No bounds checking

// ❌ CRITICAL: Off-by-one
char buf[10];
for (int i = 0; i <= 10; i++) {  // Off-by-one
    buf[i] = '\0';
}

// ❌ CRITICAL: Unsafe format string
char buffer[100];
sprintf(buffer, user_input);  // user_input may contain %s, %n, etc.
```

**Fix:**
```cpp
// ✅ GOOD: Safe string functions
strlcpy(buffer, user_input, sizeof(buffer));  // Bounds checked
strlcat(buffer, more_data, sizeof(buffer));

// ✅ GOOD: Safe formatted output
snprintf(buffer, sizeof(buffer), "%s", user_input);

// ✅ GOOD: Use std::string
std::string buffer = user_input;

// ✅ GOOD: Explicit bounds checking
if (strlen(user_input) < sizeof(buffer)) {
    strcpy(buffer, user_input);
} else {
    LOGE("Input too long");
}
```

---

### 4. Integer Overflow

**Severity:** 🟠 HIGH

**Description:** Integer arithmetic overflow leading to unexpected behavior

**Detection:**
```cpp
// ❌ BAD: Potential overflow
int size = count * item_size;  // Can overflow
int index = user_input;         // Can be negative
char* array = new array[size];  // May allocate wrong size

// ❌ BAD: Signed/unsigned comparison
int count = -1;
if (count < items.size()) {  // count promoted to unsigned, always true!
    items[count] = value;  // Crash!
}
```

**Fix:**
```cpp
// ✅ GOOD: Check for overflow
bool CalculateSize(int count, int item_size, int& out_size) {
    if (count <= 0 || item_size <= 0) return false;

    // Check for overflow
    if (count > INT_MAX / item_size) {
        LOGE("Integer overflow in size calculation");
        return false;
    }

    out_size = count * item_size;
    return true;
}

// ✅ GOOD: Use size_t for sizes
size_t count = static_cast<size_t>(user_input);
if (count < items.size()) {
    items[count] = value;
}

// ✅ GOOD: Safe arithmetic with std::mul_overflow
#include <numeric>
int result;
if (std::mul_overflow(a, b, &result)) {
    LOGE("Multiplication overflow");
}
```

---

### 5. Format String Vulnerabilities

**Severity:** 🔴 CRITICAL

**Description:** User input as format string can read/write arbitrary memory

**Detection:**
```cpp
// ❌ CRITICAL: Format string vulnerability
printf(user_input);  // user_input can contain %n to write memory!
sprintf(buffer, user_input);
fprintf(fp, user_input);

// ❌ CRITICAL: User-controlled format string
const char* fmt = user_input;
printf(fmt);
```

**Fix:**
```cpp
// ✅ GOOD: Use format specifier
printf("%s", user_input);
fprintf(fp, "%s", user_input);
snprintf(buffer, sizeof(buffer), "%s", user_input);

// ✅ GOOD: Validate format string
void SafePrint(const char* fmt, ...) {
    // Whitelist allowed format specifiers
    if (strchr(fmt, '%n')) {  // %n is dangerous
        LOGE("Dangerous format specifier");
        return;
    }
    va_list args;
    va_start(args, fmt);
    vprintf(fmt, args);
    va_end(args);
}
```

---

## Sensitive Data Protection

### Passwords and Secrets

**❌ BAD:**
```cpp
// Logging passwords
LOGI("User password: %{public}s", password.c_str());

// Storing passwords in plain text
std::string stored_password = password;

// Comparing passwords with ==
if (input_password == stored_password) {
    // Vulnerable to timing attacks
}
```

**✅ GOOD:**
```cpp
// Never log passwords
LOGI("Password length: %{public}zu", password.size());
// Or use private tag (auto-sanitized)
LOGI("Password: %{private}s", password.c_str());

// Hash passwords
std::string HashPassword(const std::string& password) {
    // Use proper hashing algorithm (bcrypt, Argon2, etc.)
    return bcrypt_hash(password);
}

// Constant-time comparison
bool ConstantTimeCompare(const std::string& a, const std::string& b) {
    if (a.size() != b.size()) return false;
    volatile int result = 0;
    for (size_t i = 0; i < a.size(); i++) {
        result |= a[i] ^ b[i];
    }
    return result == 0;
}

// Zero sensitive data when done
void SecureClear(std::string& str) {
    explicit_bzero(&str[0], str.size());
    str.clear();
}
```

### Tokens and Keys

```cpp
// ❌ BAD: Logging tokens
LOGI("API token: %{public}s", api_token.c_str());

// ❌ BAD: Hardcoded secrets
const char* API_KEY = "sk-1234567890abcdef";

// ✅ GOOD: Use environment variables
const char* api_key = getenv("API_KEY");
if (!api_key) {
    LOGE("API_KEY not set");
    return;
}

// ✅ GOOD: Don't log sensitive data
LOGI("Using API key: %{private}s", api_key);  // Auto-sanitized
```

---

## Input Validation

### Validate All External Input

```cpp
// ❌ BAD: No validation
void ProcessInput(const std::string& input) {
    int value = std::stoi(input);  // May throw, may be negative
    UseValue(value);
}

// ✅ GOOD: Complete validation
bool ProcessInput(const std::string& input, std::string& error) {
    // Check for empty
    if (input.empty()) {
        error = "Input is empty";
        return false;
    }

    // Check for valid characters
    if (!std::all_of(input.begin(), input.end(),
                     [](char c) { return std::isdigit(c) || c == '-'; })) {
        error = "Input contains invalid characters";
        return false;
    }

    // Check range
    try {
        int value = std::stoi(input);
        if (value < 0 || value > MAX_ALLOWED_VALUE) {
            error = "Input out of range";
            return false;
        }
        UseValue(value);
        return true;
    } catch (const std::exception& e) {
        error = "Invalid number format";
        return false;
    }
}
```

### Path Traversal Prevention

```cpp
// ❌ BAD: Path traversal vulnerability
std::string user_path = "../../etc/passwd";
std::string full_path = "/var/data/" + user_path;
ReadFile(full_path);  // Reads /etc/passwd!

// ✅ GOOD: Validate and sanitize paths
std::string SanitizePath(const std::string& base_dir, const std::string& user_path) {
    // Remove ".." and "."
    std::string sanitized;

    for (const auto& part : Split(user_path, '/')) {
        if (part == "..") {
            LOGE("Path traversal attempt: ../");
            return "";  // Reject
        }
        if (part == ".") continue;
        if (part.empty()) continue;

        if (!sanitized.empty()) sanitized += "/";
        sanitized += part;
    }

    // Ensure result is within base_dir
    std::string full_path = base_dir + "/" + sanitized;
    char real_path[PATH_MAX];
    if (realpath(full_path.c_str(), real_path) == nullptr) {
        LOGE("Invalid path");
        return "";
    }

    char real_base[PATH_MAX];
    if (realpath(base_dir.c_str(), real_base) == nullptr) {
        return "";
    }

    // Check if result starts with base_dir
    if (strncmp(real_path, real_base, strlen(real_base)) != 0) {
        LOGE("Path traversal attempt");
        return "";
    }

    return real_path;
}
```

---

## ACE Engine Specific Security

### ArkTS/TypeScript Security

```typescript
// ❌ BAD: Using eval
const result = eval(userInput);

// ❌ BAD: Dynamic code execution
const fn = new Function(userInput);
fn();

// ❌ BAD: InnerHTML with user input
element.innerHTML = userInput;  // XSS!

// ✅ GOOD: Use textContent instead
element.textContent = userInput;

// ✅ GOOD: Sanitize HTML
import { sanitize } from 'sanitize-html';
element.innerHTML = sanitize(userInput);

// ✅ GOOD: Template literals are safe (for values)
const message = `Value: ${sanitizedValue}`;
```

### Component Security

```cpp
// ❌ BAD: Trusting component properties from untrusted source
void SetPropertiesFromJSON(const std::string& json) {
    auto props = ParseJSON(json);
    width_ = props["width"];  // No validation!
    height_ = props["height"];  // Could be negative!
}

// ✅ GOOD: Validate all properties
bool SetPropertiesFromJSON(const std::string& json, std::string& error) {
    auto props = ParseJSON(json);
    if (!props.IsObject()) {
        error = "Invalid JSON";
        return false;
    }

    auto width = props["width"];
    if (!width.IsNumber() || width.AsInt() < 0 || width.AsInt() > MAX_WIDTH) {
        error = "Invalid width";
        return false;
    }

    width_ = width.AsInt();
    return true;
}
```

---

## Security Review Checklist

- [ ] All user input is validated
- [ ] No command injection vulnerabilities
- [ ] No SQL injection vulnerabilities
- [ ] No buffer overflows
- [ ] Sensitive data is not logged
- [ ] Secrets are not hardcoded
- [ ] Passwords are hashed
- [ ] Cryptographic functions used correctly
- [ ] Path traversal prevented
- [ ] Format string vulnerabilities fixed
- [ ] Integer overflow checked
- [ ] Type safety maintained

---

## Common Security Mistakes

### 1. Trusting Environment Variables

```cpp
// ❌ BAD: Environment variables can be modified by attacker
const char* mode = getenv("MODE");
if (strcmp(mode, "admin") == 0) {
    GrantAdminAccess();  // Attacker can set MODE=admin
}

// ✅ GOOD: Use secure configuration
const char* mode = getenv("MODE");
const char* expected_mode = GetSecureConfig("mode");
if (mode && strcmp(mode, expected_mode) == 0) {
    GrantAdminAccess();
}
```

### 2. Temporary Files

```cpp
// ❌ BAD: Predictable temporary file names
std::string tmpfile = "/tmp/menu_" + std::to_string(getpid());
// Race condition: attacker can create file between check and use

// ✅ GOOD: Use secure temporary file creation
int fd = open("/tmp/menuXXXXXX",
             O_RDWR | O_CREAT | O_EXCL,
             0600);  // Secure permissions
if (fd == -1) {
    perror("open");
    return;
}
// Or use mkstemp()
char tmpfile[] = "/tmp/menuXXXXXX";
int fd = mkstemp(tmpfile);
```

---

## Severity Guidelines

**🔴 CRITICAL:**
- Command injection
- SQL injection
- Buffer overflow
- Format string vulnerability
- Hardcoded secrets in production code

**🟠 HIGH:**
- Integer overflow
- Missing input validation
- Path traversal
- Insecure temporary files
- Sensitive data logging

**🟡 MEDIUM:**
- Missing HTTPS
- Weak crypto algorithms
- Timing attack vulnerabilities

**🟢 LOW:**
- Information leakage through error messages
- Missing security headers
- Overly permissive CORS

---

For more information, see:
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [CERT C Coding Standards](https://wiki.sei.cmu.edu/confluence/display/c/SEI+CERT+C+Coding+Standard)
