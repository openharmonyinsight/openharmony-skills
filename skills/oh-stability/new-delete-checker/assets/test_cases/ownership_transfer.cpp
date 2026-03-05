// Test Case: Ownership Transfer
// Issue: Unclear ownership transfer patterns

class Resource {
public:
    Resource() {}
    ~Resource() {}
};

Resource* CreateResource() {
    return new Resource();  // ISSUE: Who deletes this?
}

class ResourceFactory {
public:
    Resource* CreateResource() {
        return new Resource();  // ISSUE: Unclear ownership
    }
};

class CorrectFactory {
public:
    RefPtr<Resource> CreateResource() {
        return AceType::MakeRefPtr<Resource>();
    }
};

class Owner {
public:
    Owner() : resource_(new Resource()) {}  // ISSUE: Exception unsafe
    
    ~Owner() {
        delete resource_;
    }
    
    Resource* GetResource() {
        return resource_;  // ISSUE: Ownership transfer unclear
    }
    
    void SetResource(Resource* resource) {
        delete resource_;  // ISSUE: If new throws, resource_ is deleted
        resource_ = new Resource(*resource);  // May throw
    }
    
private:
    Resource* resource_;
};

class SafeOwner {
public:
    SafeOwner() : resource_(AceType::MakeRefPtr<Resource>()) {}
    
    RefPtr<Resource> GetResource() {
        return resource_;
    }
    
    void SetResource(const RefPtr<Resource>& resource) {
        resource_ = resource;  // Safe: smart pointer assignment
    }
    
private:
    RefPtr<Resource> resource_;
};

class TransferOwner {
public:
    void TakeOwnership(Resource* resource) {
        delete resource_;  // Clean up old resource
        resource_ = resource;  // Take ownership
    }
    
    ~TransferOwner() {
        delete resource_;
    }
    
private:
    Resource* resource_ = nullptr;
};
