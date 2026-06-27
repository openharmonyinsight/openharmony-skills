// Eval file for rule: Empty Interface Scanner - Negative Examples
// Note: This file extracts TS/ArkTS negative examples only.

// ArkTS empty method in class - does nothing with parameter
class AccountManager {
  onAccountsChanged(accounts: Array<AccountInfo>): void {
    // Parameter 'accounts' completely ignored
  }

  // Method with TODO comment - not implemented
  createAccountImplicitly(options: Options, callback: Callback): void {
    hiLogError("createAccountImplicitly is not implemented");
  }

  // Always returns default value without any work
  calculateValue(data: string): number {
    return 0;  // Does nothing with 'data'
  }

  // Method that only logs, no actual implementation
  updateConfig(config: Config): void {
    hiLogWarn("updateConfig called");
  }

  // Empty callback in custom component
  @State callback: ((data: string) => void) | null = null;

  processEvent(event: Event): void {
    // Does nothing with event
    return;
  }
}

// ArkTS struct with empty method
struct DataTable {
  // Empty method - accepts data but doesn't use it
  processData(data: DataType): void {
  }

  // Method that only returns default
  getItemById(id: string): Item | null {
    return null;
  }
}

// Empty method that only returns default value
function processData(data: string): number {
    return 0;  // Does nothing with 'data'
}

// Stub method with TODO comment
function verifyToken(token: string): boolean {
    // TODO: implement verification
    return false;
}

// Empty arrow function
const handleEvent = (event: Event): void => {};

// Method that just throws "not implemented"
function authenticate(credentials: Credentials): void {
    throw new Error("not implemented");
}

// Always returns null
function getUserById(id: string): User | null {
    return null;
}

// ArkTS class method - options parameter ignored
class ConfigManager {
  configure(options: ConfigOptions): void {
    this.setDefaultConfig();  // 'options' parameter not used
  }

  // Callback parameter accepted but never invoked
  registerCallback(callback: Function): void {
    hiLogInfo("registered");  // 'callback' never stored or called
  }

  // Multiple ignored parameters
  updateUser(id: string, name: string, email: string): void {
    hiLogInfo("user update");  // All parameters ignored
  }
}

// Options parameter ignored
function configure(options: ConfigOptions): void {
    setDefaultConfig();  // 'options' parameter not used
}

// Callback parameter accepted but never invoked
function registerCallback(callback: Function): void {
    console.log("registered");  // 'callback' never stored or called
}

// Multiple ignored parameters
function updateUser(id: string, name: string, email: string): void {
    console.log("user update");  // All parameters ignored
}

// ArkTS event emitter - external developers can subscribe but callback never fires
class AccountEventEmitter {
  private subscribers: Array<Function> = [];

  // External developers can subscribe to this event
  onAccountsChanged(callback: (accounts: Array<AccountInfo>) => void): void {
    this.subscribers.push(callback);
  }

  // But callback only fires for system apps
  notifyAccountsChanged(accounts: Array<AccountInfo>): void {
    if (!this.isSystemApp()) {
      return;  // Silently fails - external developers get no notification
    }
    this.subscribers.forEach(cb => cb(accounts));
  }

  private isSystemApp(): boolean {
    return false;
  }
}

// External developers can subscribe but callback never fires
function onAccountsChanged(accounts: AccountInfo[], callback: Function): void {
    if (!isSystemApp()) {
        return;  // Silently fails for external developers
    }
    callback(accounts);
}

// System-only event handler
function registerSystemEventHandler(handler: EventHandler): void {
    if (getCallingUid() !== SYSTEM_UID) {
        return;  // No error, just silent failure
    }
    handlers.push(handler);
}

// ArkTS method explicitly logs not implemented
class Authenticator {
  auth(name: string, options: AuthOptions): void {
    hiLogError("auth is not implemented");
  }

  // Returns "not supported" error immediately
  setProperties(props: Properties): ErrCode {
    return ErrCode.NOT_SUPPORTED;  // Always returns same error
  }

  // Comment says not supported
  enableFeature(enable: boolean): void {
    // Not supported yet
  }

  // Stub that always fails
  verifyCredential(cred: Credential): ErrCode {
    hiLogError("verifyCredential is not implemented");
    return ErrCode.NOT_SUPPORTED;
  }

  // TODO comment without implementation
  processDomainAccount(account: DomainAccount): void {
    // TODO: implement domain account processing
  }
}

// Method that only logs "not implemented"
function authenticate(credentials: Credentials): void {
    console.error("authenticate is not implemented");
}

// Always throws "not supported"
function setProperties(props: Properties): void {
    throw new Error("not supported");
}

// Comment indicates not implemented
function enableFeature(enable: boolean): void {
    // Not supported yet
}

// Stub that returns error
function verifyCredential(cred: Credential): ErrCode {
    console.error("VerifyCredential is not implemented");
    return ErrCode.NOT_SUPPORTED;
}
