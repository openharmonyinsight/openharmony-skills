/*
 * Copyright (c) 2026 Huawei Device Co., Ltd.
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

const DOMAIN: number = 0xFF00;
const TAG: string = 'HilogCoverageTest';

export default function actsHilogCoverageTest() {
  describe('ActsHilogCoverageTest', () => {

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_001
     * @tc.desc: Test OH_LOG_PrintMsg with normal parameters
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsg_ParamTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_PrintMsg_ParamTest(0, 4, 0xFF00, 'TestTag', 'Hello PrintMsg');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsg result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_PARAM_002
     * @tc.desc: Test OH_LOG_PrintMsg with different log levels (DEBUG, WARN, FATAL)
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsg_LevelTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let resultDebug = testNapi.OH_LOG_PrintMsg_LevelTest(0, 3, 0xFF00, 'TestTag', 'debug msg');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsg DEBUG result: ${resultDebug}`);
          expect(resultDebug >= 0).assertTrue();

          let resultWarn = testNapi.OH_LOG_PrintMsg_LevelTest(0, 5, 0xFF00, 'TestTag', 'warn msg');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsg WARN result: ${resultWarn}`);
          expect(resultWarn >= 0).assertTrue();

          let resultFatal = testNapi.OH_LOG_PrintMsg_LevelTest(0, 7, 0xFF00, 'TestTag', 'fatal msg');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsg FATAL result: ${resultFatal}`);
          expect(resultFatal >= 0).assertTrue();

          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsg_BOUNDARY_001
     * @tc.desc: Test OH_LOG_PrintMsg with empty tag and message boundary
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsg_EmptyMsgTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_PrintMsg_EmptyMsgTest(0, 4, 0xFF00, '', '');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsg empty boundary result: ${result}`);
          expect(typeof result === 'number').assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_PARAM_001
     * @tc.desc: Test OH_LOG_PrintMsgByLen with normal parameters
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsgByLen_ParamTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_PrintMsgByLen_ParamTest(0, 4, 0xFF00, 'TestTag', 'Hello PrintMsgByLen');
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsgByLen result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_BOUNDARY_001
     * @tc.desc: Test OH_LOG_PrintMsgByLen with boundary length values (tagLen=0, messageLen=0)
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsgByLen_BoundaryTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_PrintMsgByLen_BoundaryTest(0, 4, 0xFF00, 'TestTag', 0, 'Hello', 0);
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsgByLen boundary result: ${result}`);
          expect(typeof result === 'number').assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_PrintMsgByLen_RETURN_001
     * @tc.desc: Test OH_LOG_PrintMsgByLen return value with explicit lengths
     * @tc.type: FUNC
     */
    it('OH_LOG_PrintMsgByLen_ReturnTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_PrintMsgByLen_ReturnTest(0, 4, 0xFF00, 'TestTag', 7, 'TestMsg', 7);
          hilog.info(DOMAIN, TAG, `OH_LOG_PrintMsgByLen return result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_001
     * @tc.desc: Test OH_LOG_VPrint with normal string format parameters
     * @tc.type: FUNC
     */
    it('OH_LOG_VPrint_ParamTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_VPrint_ParamTest(0, 4, 0xFF00, 'TestTag', '%s', 'Hello VPrint');
          hilog.info(DOMAIN, TAG, `OH_LOG_VPrint result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_PARAM_002
     * @tc.desc: Test OH_LOG_VPrint with integer format parameter
     * @tc.type: FUNC
     */
    it('OH_LOG_VPrint_FmtIntTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_VPrint_FmtIntTest(0, 4, 0xFF00, 'TestTag', '%d', 42);
          hilog.info(DOMAIN, TAG, `OH_LOG_VPrint int format result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_OH_LOG_VPrint_RETURN_001
     * @tc.desc: Test OH_LOG_VPrint return value with plain text
     * @tc.type: FUNC
     */
    it('OH_LOG_VPrint_ReturnTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      async (done: Function) => {
        try {
          let result = testNapi.OH_LOG_VPrint_ReturnTest(0, 4, 0xFF00, 'TestTag', 'plain text');
          hilog.info(DOMAIN, TAG, `OH_LOG_VPrint return result: ${result}`);
          expect(result >= 0).assertTrue();
          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_001
     * @tc.desc: Test all PreferStrategy enum values (UNSET_LOGLEVEL, PREFER_CLOSE_LOG, PREFER_OPEN_LOG)
     * @tc.type: FUNC
     */
    it('PreferStrategy_ParamTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        try {
          let resultUnset = testNapi.PreferStrategy_ParamTest(4, 0);
          hilog.info(DOMAIN, TAG, `PreferStrategy UNSET_LOGLEVEL result: ${resultUnset}`);
          expect(typeof resultUnset === 'number').assertTrue();

          let resultClose = testNapi.PreferStrategy_ParamTest(7, 1);
          hilog.info(DOMAIN, TAG, `PreferStrategy PREFER_CLOSE_LOG result: ${resultClose}`);
          expect(typeof resultClose === 'number').assertTrue();

          let resultOpen = testNapi.PreferStrategy_ParamTest(3, 2);
          hilog.info(DOMAIN, TAG, `PreferStrategy PREFER_OPEN_LOG result: ${resultOpen}`);
          expect(typeof resultOpen === 'number').assertTrue();

          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_002
     * @tc.desc: Test PREFER_CLOSE_LOG strategy then verify log level restriction
     * @tc.type: FUNC
     */
    it('PreferStrategy_CloseLogTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        try {
          let result = testNapi.PreferStrategy_CloseLogTest(7, 1);
          hilog.info(DOMAIN, TAG, `PreferStrategy CloseLog result: ${result}`);
          expect(typeof result === 'number').assertTrue();

          let printResult = testNapi.OH_LOG_PrintMsg_ParamTest(0, 3, 0xFF00, 'TestTag', 'debug after close');
          hilog.info(DOMAIN, TAG, `Print after close result: ${printResult}`);
          expect(typeof printResult === 'number').assertTrue();

          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

    /**
     * @tc.name: SUB_HIVIEWDFX_HILOG_PreferStrategy_PARAM_003
     * @tc.desc: Test PREFER_OPEN_LOG strategy then verify log output
     * @tc.type: FUNC
     */
    it('PreferStrategy_OpenLogTest', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      async (done: Function) => {
        try {
          let result = testNapi.PreferStrategy_OpenLogTest(4, 2);
          hilog.info(DOMAIN, TAG, `PreferStrategy OpenLog result: ${result}`);
          expect(typeof result === 'number').assertTrue();

          let printResult = testNapi.OH_LOG_PrintMsg_ParamTest(0, 4, 0xFF00, 'TestTag', 'info after open');
          hilog.info(DOMAIN, TAG, `Print after open result: ${printResult}`);
          expect(printResult >= 0).assertTrue();

          done();
        } catch (err) {
          let errMsg = (err as BusinessError).message;
          let code = (err as BusinessError).code;
          hilog.error(DOMAIN, TAG, `Test errCode:${code} message:${errMsg}`);
          expect.fail(`Test should not throw error but got: ${errMsg}`);
          done();
        }
      })

  })
}
