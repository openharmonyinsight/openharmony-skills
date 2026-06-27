/**
 * Feature management API interface.
 */
export interface FeatureStatus {
  enabled: boolean;
  version: string;
  priority?: number;  // NOT documented in docs/feature.md
}

export interface FeatureOptions {
  autoStart?: boolean;
  priority?: number;
  timeout?: number;  // NOT documented in docs/feature.md
}

export interface FeatureAPI {
  /**
   * Enables a feature.
   * @permission ohos.permission.MANAGE_FEATURES
   * @syscap SystemCapability.FeatureManagement
   * @throws BusinessError 401 - Feature not found.
   * @throws BusinessError 403 - Permission denied.
   * @throws BusinessError 409 - Feature already enabled.
   * @throws BusinessError 500 - Internal error (NOT documented in docs)
   */
  enableFeature(featureId: string, options?: FeatureOptions): Promise<boolean>;

  /**
   * Disables a feature.
   * @permission ohos.permission.MANAGE_FEATURES
   * @syscap SystemCapability.FeatureManagement
   * @throws BusinessError 401 - Feature not found.
   * @throws BusinessError 403 - Permission denied.
   * @throws BusinessError 410 - Feature already disabled (NOT documented in docs)
   */
  disableFeature(featureId: string): Promise<boolean>;

  /**
   * Gets feature status.
   * @syscap SystemCapability.FeatureManagement
   */
  getFeatureStatus(featureId: string): FeatureStatus;
}
