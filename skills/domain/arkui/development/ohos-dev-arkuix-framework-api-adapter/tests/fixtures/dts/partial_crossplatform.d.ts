/**
 * @ohos.net.http
 * @syscap SystemCapability.Communication.NetStack
 * @since 6
 */
declare namespace http {
    /**
     * @crossplatform
     * @since 6
     */
    export function createHttp(): HttpRequest;
    
    /**
     * @crossplatform
     * @since 6
     */
    export interface HttpRequest {
        /**
         * @crossplatform
         * @since 6
         */
        request(url: string, callback: AsyncCallback<void>): void;
        
        /**
         * @crossplatform
         * @since 6
         */
        request(url: string, options: HttpRequestOptions, callback: AsyncCallback<void>): void;
        
        /** @since 6 */
        requestInStream(url: string, callback: AsyncCallback<void>): void;
        
        /** @since 10 */
        requestInStream(url: string, options: HttpRequestOptions, callback: AsyncCallback<void>): void;
    }
    
    /** @since 6 */
    export interface HttpRequestOptions {
        method: HttpMethod;
        header: Object;
        extraData: string | Object | ArrayBuffer;
        expectDataType: HttpDataType;
        usingCache: boolean;
    }
    
    /** @since 6 */
    export enum HttpMethod {
        OPTIONS = "OPTIONS",
        GET = "GET",
        HEAD = "HEAD",
        POST = "POST",
        PUT = "PUT",
        DELETE = "DELETE",
        TRACE = "TRACE"
    }
    
    /** @since 6 */
    export enum HttpDataType {
        STRING = 0,
        OBJECT = 1,
        ARRAY_BUFFER = 2
    }
    
    /** @since 6 */
    export type HttpResponsedata = string | Object | ArrayBuffer;
}
