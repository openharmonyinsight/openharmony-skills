// Fixture: clean, well-structured code sample. No oversized functions, no circular deps.
// Used for false-positive control: a with-skill run must produce no findings.
// Each function stays well under the default 50 effective-line threshold.

#include <string>
#include <vector>

namespace metrics {

class MetricsLogger {
public:
    void LogCounter(const std::string &name, int value) {
        if (name.empty()) {
            return;
        }
        entries_.push_back({name, value});
    }

    int GetCounter(const std::string &name) const {
        for (const auto &e : entries_) {
            if (e.name == name) {
                return e.value;
            }
        }
        return 0;
    }

    std::vector<std::string> ListNames() const {
        std::vector<std::string> names;
        names.reserve(entries_.size());
        for (const auto &e : entries_) {
            names.push_back(e.name);
        }
        return names;
    }

    void Clear() {
        entries_.clear();
    }

private:
    struct Entry {
        std::string name;
        int value;
    };
    std::vector<Entry> entries_;
};

} // namespace metrics
