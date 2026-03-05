// Test Case: Container Pointer Issues
// Issue: Container with raw pointers not cleaned up in destructor

class Item {
public:
    Item() {}
    ~Item() {}
};

class ContainerWithoutCleanup {
public:
    void AddItem(Item* item) {
        items_.push_back(item);
    }
    
    // ISSUE: Destructor missing - items will leak
    
private:
    std::vector<Item*> items_;
};

class ContainerWithCleanup {
public:
    void AddItem(Item* item) {
        items_.push_back(item);
    }
    
    ~ContainerWithCleanup() {
        for (auto* item : items_) {
            delete item;
        }
        items_.clear();
    }
    
private:
    std::vector<Item*> items_;
};

class ContainerWithSmartPointers {
public:
    void AddItem(Item* item) {
        items_.push_back(AceType::MakeRefPtr<Item>(item));
    }
    
    // Destructor not needed - smart pointers auto-clean
    
private:
    std::vector<RefPtr<Item>> items_;
};

class IteratorInvalidation {
public:
    IteratorInvalidation() {
        for (int i = 0; i < 10; i++) {
            items_.push_back(new Item());
        }
    }
    
    ~IteratorInvalidation() {
        // ISSUE: This pattern can cause iterator invalidation
        for (auto it = items_.begin(); it != items_.end(); ++it) {
            delete *it;
        }
        items_.clear();
    }
    
private:
    std::vector<Item*> items_;
};

class SafeIteratorCleanup {
public:
    SafeIteratorCleanup() {
        for (int i = 0; i < 10; i++) {
            items_.push_back(new Item());
        }
    }
    
    ~SafeIteratorCleanup() {
        // Safe: Clear the vector first, then delete
        while (!items_.empty()) {
            Item* item = items_.back();
            items_.pop_back();
            delete item;
        }
    }
    
private:
    std::vector<Item*> items_;
};
