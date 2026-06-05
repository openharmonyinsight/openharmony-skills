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
const TAG: string = 'ZlibCompressTest';

export default function actsZlibCompressTest() {
  describe('ZlibCompressTest', () => {

    /**
     * @tc.name: SUB_ZLIB_Compress_PARAM_001
     * @tc.desc: 测试 compress 函数，正常数据压缩
     * @tc.type: FUNC
     */
    it('Compress_NormalData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================Compress_NormalData start==================');
        try {
          const testData: string = 'Hello, zlib! This is a test string for compress.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const encoded: Uint8Array = textEncoder.encodeInto(testData);
          const arrayBuffer: ArrayBuffer = encoded.buffer;

          const compressed: ArrayBuffer = testNapi.compressNormalData(arrayBuffer);

          expect(compressed.byteLength).assertLarger(0);
          expect(compressed.byteLength).assertLess(arrayBuffer.byteLength);

          hilog.info(DOMAIN, TAG, `Compressed: ${compressed.byteLength}, Original: ${arrayBuffer.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Compress_NormalData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================Compress_NormalData end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_Compress_PARAM_002
     * @tc.desc: 测试 compress 函数，空数据压缩
     * @tc.type: FUNC
     */
    it('Compress_EmptyData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================Compress_EmptyData start==================');
        try {
          const emptyBuffer: ArrayBuffer = new ArrayBuffer(0);

          const compressed: ArrayBuffer = testNapi.compressEmptyData(emptyBuffer);

          expect(compressed.byteLength).assertLarger(0);

          hilog.info(DOMAIN, TAG, `Compressed empty data size: ${compressed.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Compress_EmptyData error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================Compress_EmptyData end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_Compress_ERROR_001
     * @tc.desc: 测试 compress 函数，输出缓冲区不足
     * @tc.type: FUNC
     */
    it('Compress_BufError', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================Compress_BufError start==================');
        try {
          const testData: string = 'This is a longer string that will not fit in a tiny buffer.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const encoded: Uint8Array = textEncoder.encodeInto(testData);
          const arrayBuffer: ArrayBuffer = encoded.buffer;

          testNapi.compressBufError(arrayBuffer);

          expect.fail('Test should throw error but no error thrown');
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.info(DOMAIN, TAG, `Compress_BufError caught error: errCode:${code} message:${errMsg}`);
          expect(code).assertEqual('-5');
        }
        done();
        hilog.info(DOMAIN, TAG, '==================Compress_BufError end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_Uncompress_PARAM_001
     * @tc.desc: 测试 uncompress 函数，正常数据解压缩完整往返测试
     * @tc.type: FUNC
     */
    it('Uncompress_RoundTrip', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================Uncompress_RoundTrip start==================');
        try {
          const originalData: string = 'Hello, zlib! This is a test string for uncompress round trip.';
          const textEncoder: util.TextEncoder = new util.TextEncoder();
          const encoded: Uint8Array = textEncoder.encodeInto(originalData);
          const originalBuffer: ArrayBuffer = encoded.buffer;

          const compressed: ArrayBuffer = testNapi.compressNormalData(originalBuffer);

          const decompressed: ArrayBuffer =
            testNapi.uncompressRoundTrip(compressed, originalBuffer.byteLength);

          expect(decompressed.byteLength).assertEqual(originalBuffer.byteLength);

          const decompressedArray: Uint8Array = new Uint8Array(decompressed);
          const originalArray: Uint8Array = new Uint8Array(originalBuffer);
          for (let i = 0; i < decompressedArray.length; i++) {
            expect(decompressedArray[i]).assertEqual(originalArray[i]);
          }

          hilog.info(DOMAIN, TAG, `Round trip success: original=${originalBuffer.byteLength}, compressed=${compressed.byteLength}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Uncompress_RoundTrip error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================Uncompress_RoundTrip end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_Uncompress_ERROR_001
     * @tc.desc: 测试 uncompress 函数，损坏数据解压
     * @tc.type: FUNC
     */
    it('Uncompress_CorruptData', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================Uncompress_CorruptData start==================');
        try {
          const corruptBuffer: ArrayBuffer = new ArrayBuffer(32);
          const corruptArray: Uint8Array = new Uint8Array(corruptBuffer);
          for (let i = 0; i < corruptArray.length; i++) {
            corruptArray[i] = (i + 1) * 7;
          }

          testNapi.uncompressCorruptData(corruptBuffer, 1024);

          expect.fail('Test should throw error but no error thrown');
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.info(DOMAIN, TAG, `Uncompress_CorruptData caught error: errCode:${code} message:${errMsg}`);
          expect(code === '-3' || code === '-5').assertTrue();
        }
        done();
        hilog.info(DOMAIN, TAG, '==================Uncompress_CorruptData end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_CompressBound_RETURN_001
     * @tc.desc: 测试 compressBound 函数，正常数据大小
     * @tc.type: FUNC
     */
    it('CompressBound_NormalSize', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressBound_NormalSize start==================');
        try {
          const sourceLen: number = 100;

          const bound: number = testNapi.compressBoundNormalSize(sourceLen);

          expect(bound).assertLarger(0);
          expect(bound).assertLarger(sourceLen);

          hilog.info(DOMAIN, TAG, `compressBound(${sourceLen}) = ${bound}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressBound_NormalSize error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressBound_NormalSize end==================');
      });

    /**
     * @tc.name: SUB_ZLIB_CompressBound_BOUNDARY_001
     * @tc.desc: 测试 compressBound 函数，零长度边界值
     * @tc.type: FUNC
     */
    it('CompressBound_ZeroLength', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        hilog.info(DOMAIN, TAG, '==================CompressBound_ZeroLength start==================');
        try {
          const bound: number = testNapi.compressBoundZeroLength();

          expect(bound).assertLarger(0);

          hilog.info(DOMAIN, TAG, `compressBound(0) = ${bound}`);
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `CompressBound_ZeroLength error: errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
        }
        done();
        hilog.info(DOMAIN, TAG, '==================CompressBound_ZeroLength end==================');
      });

  });
}
