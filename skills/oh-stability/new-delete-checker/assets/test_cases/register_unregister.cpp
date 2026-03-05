// Test Case: Register/Unregister Issues
// Issue: Registration without proper cleanup

void Register();
void Unregister();

class RegisteredObject {
public:
    RegisteredObject() {
        Register();  // ISSUE: May throw, caller must remember to Unregister
    }
    
    ~RegisteredObject() {
        Unregister();
    }
};

class RegisteredObjectWithException {
public:
    RegisteredObjectWithException() {
        Register();
        
        // ISSUE: If constructor body throws, Unregister never called
        Initialize();  // May throw
        
        Unregister();  // Never reached if Initialize throws
    }
    
    void Initialize() {
        if (ShouldFail()) {
            throw std::runtime_error("Initialization failed");
        }
    }
    
    ~RegisteredObjectWithException() {
        Unregister();  // Never called if constructor throws
    }
    
private:
    bool ShouldFail() { return true; }
};

class SafeRegisteredObject {
public:
    SafeRegisteredObject() {
        Register();
        
        try {
            Initialize();
        } catch (...) {
            Unregister();  // Cleanup on failure
            throw;
        }
    }
    
    ~SafeRegisteredObject() {
        Unregister();
    }
    
private:
    void Initialize() {
        if (ShouldFail()) {
            throw std::runtime_error("Initialization failed");
        }
    }
    
    bool ShouldFail() { return true; }
};

class DuplicateRegistration {
public:
    void RegisterTwice() {
        Register();  // First registration
        Register();  // ISSUE: Second registration - old one leaked
    }
    
    void SafeRegistration() {
        if (IsRegistered()) {
            Unregister();
        }
        Register();
    }
    
private:
    bool IsRegistered() {
        return registered_;
    }
    
    bool registered_ = false;
};
