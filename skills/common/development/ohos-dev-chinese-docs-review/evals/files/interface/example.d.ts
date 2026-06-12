/**
 * Example API interface for testing documentation quality checks.
 */
export interface ExampleAPI {
  /**
   * Performs an example operation.
   * @systemapi
   * @permission ohos.permission.EXAMPLE
   * @syscap SystemCapability.Example.Feature
   * @throws BusinessError 201 - Parameter check failed.
   * @throws BusinessError 202 - Permission denied.
   */
  performOperation(input: string): void;

  /**
   * Gets the current state.
   * @systemapi
   * @syscap SystemCapability.Example.State
   */
  getState(): number;
}
