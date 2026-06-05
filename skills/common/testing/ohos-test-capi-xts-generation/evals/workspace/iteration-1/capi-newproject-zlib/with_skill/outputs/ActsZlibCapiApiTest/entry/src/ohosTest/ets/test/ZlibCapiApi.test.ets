/*
 * Copyright (C) 2025 Huawei Device Co., Ltd.
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

import { hilog } from '@kit.PerformanceAnalysisKit';
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';
import testNapi from 'libentry.so';
import { BusinessError } from '@kit.BasicServicesKit';
import { util } from '@kit.ArkTS';

const DOMAIN: number = 0xFF00;
const TAG: string = 'ZlibCapiTest';

export default function actsZlibCapiApiTest() {
  describe('ActsZlibCapiApiTest', () => {

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_PARAM_001
     * @tc.desc: Test compress function with normal data
     * @tc.type: FUNC
     */
    it('CompressNormalData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressNormalData start==================');
        try {
          const testData: string = 'Hello, zlib! This is a test string for compress.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

          const compressed: ArrayBuffer = testNapi.compressNormalData(arrayBuffer);

          expect(compressed.byteLength).assertLarger(0);
          hilog.info(DOMAIN, TAG, `Compressed size: ${compressed.byteLength}, Original size: ${arrayBuffer.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressNormalData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressNormalData end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_BOUNDARY_001
     * @tc.desc: Test compress function with empty data
     * @tc.type: FUNC
     */
    it('CompressEmptyData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressEmptyData start==================');
        try {
          const emptyBuffer: ArrayBuffer = new ArrayBuffer(0);

          const compressed: ArrayBuffer = testNapi.compressEmptyData(emptyBuffer);

          expect(compressed.byteLength).assertLarger(0);
          hilog.info(DOMAIN, TAG, `Empty data compressed size: ${compressed.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressEmptyData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressEmptyData end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Compress_PARAM_002
     * @tc.desc: Test compress function with large data
     * @tc.type: FUNC
     */
    it('CompressLargeData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressLargeData start==================');
        try {
          const largeSize: number = 10240;
          const largeBuffer: ArrayBuffer = new ArrayBuffer(largeSize);
          const view: Uint8Array = new Uint8Array(largeBuffer);
          for (let i = 0; i < largeSize; i++) {
            view[i] = i % 256;
          }

          const compressed: ArrayBuffer = testNapi.compressLargeData(largeBuffer);

          expect(compressed.byteLength).assertLarger(0);
          hilog.info(DOMAIN, TAG, `Large data compressed size: ${compressed.byteLength}, Original: ${largeSize}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressLargeData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressLargeData end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_PARAM_001
     * @tc.desc: Test uncompress function with normal compressed data
     * @tc.type: FUNC
     */
    it('UncompressNormalData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================UncompressNormalData start==================');
        try {
          const originalData: string = 'Hello, zlib! This is a test string for uncompress.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const originalBuffer: ArrayBuffer = textEncoder.encodeInto(originalData).buffer;

          const compressed: ArrayBuffer = testNapi.compressNormalData(originalBuffer);

          const decompressed: ArrayBuffer = testNapi.uncompressNormalData(compressed, originalBuffer.byteLength);

          expect(decompressed.byteLength).assertEqual(originalBuffer.byteLength);

          const decompressedArray: Uint8Array = new Uint8Array(decompressed);
          const originalArray: Uint8Array = new Uint8Array(originalBuffer);
          for (let i = 0; i < decompressedArray.length; i++) {
            expect(decompressedArray[i]).assertEqual(originalArray[i]);
          }

          hilog.info(DOMAIN, TAG, `Decompressed size: ${decompressed.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `UncompressNormalData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================UncompressNormalData end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_ERROR_001
     * @tc.desc: Test uncompress function with corrupted data
     * @tc.type: FUNC
     */
    it('UncompressCorruptedData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================UncompressCorruptedData start==================');
        try {
          const corruptedBuffer: ArrayBuffer = new ArrayBuffer(16);
          const view: Uint8Array = new Uint8Array(corruptedBuffer);
          for (let i = 0; i < 16; i++) {
            view[i] = 0xFF;
          }

          const result: number = testNapi.uncompressCorruptedData(corruptedBuffer, 1024);

          let errCodeDataError = -3;
          expect(result).assertEqual(errCodeDataError);
          hilog.info(DOMAIN, TAG, `Corrupted data uncompress result: ${result}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `UncompressCorruptedData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================UncompressCorruptedData end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_Uncompress_ERROR_002
     * @tc.desc: Test uncompress function with insufficient buffer
     * @tc.type: FUNC
     */
    it('UncompressSmallBuffer', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================UncompressSmallBuffer start==================');
        try {
          const testData: string = 'Hello, zlib!';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const originalBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

          const compressed: ArrayBuffer = testNapi.compressNormalData(originalBuffer);

          const result: number = testNapi.uncompressSmallBuffer(compressed, 1);

          let errCodeBufError = -5;
          expect(result).assertEqual(errCodeBufError);
          hilog.info(DOMAIN, TAG, `Small buffer uncompress result: ${result}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `UncompressSmallBuffer error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================UncompressSmallBuffer end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_RETURN_001
     * @tc.desc: Test compressBound function with normal source length
     * @tc.type: FUNC
     */
    it('CompressBoundNormalLength', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressBoundNormalLength start==================');
        try {
          const sourceLen: number = 1024;

          const bound: number = testNapi.compressBoundNormalLength(sourceLen);

          expect(bound).assertLarger(0);
          expect(bound).assertLarger(sourceLen);
          hilog.info(DOMAIN, TAG, `compressBound(1024) = ${bound}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressBoundNormalLength error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressBoundNormalLength end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_BOUNDARY_001
     * @tc.desc: Test compressBound function with zero source length
     * @tc.type: FUNC
     */
    it('CompressBoundZeroLength', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressBoundZeroLength start==================');
        try {
          const bound: number = testNapi.compressBoundZeroLength();

          expect(bound).assertLarger(0);
          hilog.info(DOMAIN, TAG, `compressBound(0) = ${bound}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressBoundZeroLength error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressBoundZeroLength end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressBound_BOUNDARY_002
     * @tc.desc: Test compressBound function with large source length
     * @tc.type: FUNC
     */
    it('CompressBoundLargeLength', TestType.FUNCTION | Size.SMALLTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressBoundLargeLength start==================');
        try {
          const largeLen: number = 1048576;

          const bound: number = testNapi.compressBoundLargeLength(largeLen);

          expect(bound).assertLarger(0);
          hilog.info(DOMAIN, TAG, `compressBound(1048576) = ${bound}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressBoundLargeLength error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressBoundLargeLength end==================');
      });

    /**
     * @tc.name: SUB_BUNDLEMANAGER_ZLIB_CompressUncompress_RETURN_001
     * @tc.desc: Test compress then uncompress round trip
     * @tc.type: FUNC
     */
    it('CompressUncompressRoundTrip', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressUncompressRoundTrip start==================');
        try {
          const testData: string = 'Hello, zlib! Round trip test for compress and uncompress.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const arrayBuffer: ArrayBuffer = textEncoder.encodeInto(testData).buffer;

          const result: number = testNapi.compressUncompressRoundTrip(arrayBuffer);

          expect(result).assertEqual(0);
          hilog.info(DOMAIN, TAG, `Round trip result: ${result}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressUncompressRoundTrip error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressUncompressRoundTrip end==================');
      });

  });
}
