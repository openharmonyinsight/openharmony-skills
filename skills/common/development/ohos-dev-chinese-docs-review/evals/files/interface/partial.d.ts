/**
 * Partial API interface - only public API documented.
 */
export interface DataItem {
  id: string;
  name: string;
  value?: number;
}

export interface PartialAPI {
  /**
   * Gets data items.
   * @systemapi
   * @syscap SystemCapability.PartialAPI.Data
   */
  getData(): Promise<DataItem[]>;

  /**
   * Sets data items.
   * @systemapi
   * @syscap SystemCapability.PartialAPI.Data
   * @throws BusinessError 201 - Parameter validation failed.
   * @throws BusinessError 202 - Data size exceeds limit.
   */
  setData(items: DataItem[]): Promise<void>;
}
