/**
 * @ohos.settings
 * @syscap SystemCapability.Applications.settings.Core
 * @crossplatform
 * @since 8
 */
declare namespace settings {
    /**
     * @crossplatform
     * @since 8
     */
    export function getValue(context: Context, name: string, callback: AsyncCallback<string>): void;
    
    /**
     * @crossplatform
     * @since 8
     */
    export function setValue(context: Context, name: string, value: string, callback: AsyncCallback<void>): void;
    
    /** @since 8 */
    export function getValueSync(context: Context, name: string, defValue: string): string;
    
    /** @since 8 */
    export function setValueSync(context: Context, name: string, value: string): boolean;
    
    /** @since 10 */
    export enum DateDisplayMode {
        AUTO = 0,
        TIME = 1
    }
    
    /** @since 8 */
    export const DISPLAY_DATE: string;
    
    /** @since 8 */
    export const DISPLAY_BRIGHTNESS: string;
}
