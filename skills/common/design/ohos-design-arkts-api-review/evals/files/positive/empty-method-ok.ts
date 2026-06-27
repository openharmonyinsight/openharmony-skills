// Eval file for rule: Empty Interface Scanner - Positive Examples
// Note: This file extracts TS/ArkTS positive examples only.

// ArkTS abstract method - must be implemented by derived classes
abstract class BaseSubscriber {
  abstract onAccountsChanged(accounts: Array<AccountInfo>): void;  // OK: abstract
}

// ArkTS interface with abstract method
interface IEventHandler {
  handleEvent(event: Event): void;  // OK: interface definition
}

// ArkTS struct with valid empty constructor
struct MyComponent {
  // OK: default constructor
  constructor() {
  }

  // Empty default implementation that can be overridden
  protected onStateChange(): void {
    // Default: do nothing, subclasses can override
  }
}

// ArkTS optional parameter with valid empty implementation
processOptionalFeature(feature?: Feature): void {
  if (!feature) {
    return;  // OK: feature is optional
  }
  // process feature...
}

// ArkTS lifecycle method with intentional empty implementation
@Entry
@Component
struct MyPage {
  // OK: Optional lifecycle method
  aboutToAppear(): void {
    // Intentionally empty - no setup needed
  }

  // Valid empty method for optional callback
  onDismiss(): void {
    // User chose not to handle dismiss
  }
}

// ArkTS method with conditional processing
class DataProcessor {
  processFeature(feature: Feature): void {
    if (!feature.isEnabled()) {
      return;  // OK: feature is optional, skipping is valid
    }
    this.doProcessFeature(feature);
  }

  private doProcessFeature(feature: Feature): void {
    // Actual implementation
  }
}

// Empty abstract method (must be overridden)
abstract class Subscriber {
    abstract onAccountsChanged(accounts: AccountInfo[]): void;  // OK: abstract
}

// Empty default implementation
class BaseHandler {
    handle(data: string): void {
        // Default: do nothing, subclasses can override
    }
}

// Optional feature with valid empty implementation
function processOptionalFeature(feature?: Feature): void {
    if (!feature) {
        return;  // OK: feature is optional
    }
    // process feature...
}

// No-op for logging/debugging purposes
const NOOP: () => void = () => {};  // OK: intentional no-op
