/**
 * Example component interface for repository-root path testing.
 */
export interface ExampleComponent {
  /**
   * Sets a property value.
   * @permission ohos.permission.EXAMPLE
   * @syscap SystemCapability.Example.Property
   */
  setProperty(name: string, value: any): void;

  /**
   * Gets a property value.
   * @syscap SystemCapability.Example.Property
   */
  getProperty(name: string): any;
}
