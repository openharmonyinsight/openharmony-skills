/**
 * @ohos.bluetooth.socket
 * @syscap SystemCapability.Communication.Bluetooth.Core
 * @since 10
 */
declare namespace socket {
    /** @since 10 */
    export function sppListen(name: string, option: SppOption, callback: AsyncCallback<number>): void;
    
    /** @since 10 */
    export function sppAccept(serverSocketCode: number, callback: AsyncCallback<number>): void;
    
    /** @since 10 */
    export function sppConnect(deviceId: string, option: SppOption, callback: AsyncCallback<void>): void;
    
    /** @since 10 */
    export interface SppOption {
        type: SppType;
        uuid: string;
        secure: boolean;
    }
    
    /** @since 10 */
    export enum SppType {
        SPP_RFCOMM = 0,
        SPP_LE = 1
    }
}
