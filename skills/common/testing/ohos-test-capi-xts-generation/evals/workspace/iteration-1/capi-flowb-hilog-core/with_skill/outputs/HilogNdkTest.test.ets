/*
 * Copyright (c) 2024 Huawei Device Co., Ltd.
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

import { describe, beforeAll, afterEach, afterAll, it, expect, TestType, Size, Level } from '@ohos/hypium';
import hilog from '@ohos.hilog';
import testNapi from 'libentry.so';

const DOMAIN: number = 0xFF00;
const TAG: string = 'HilogNdkTest';

export default function HilogNdkTest() {
  describe('HilogNdkTest', function () {

    beforeAll(function () {
      hilog.info(DOMAIN, TAG, 'HilogNdkTest beforeAll called');
    });

    afterAll(function () {
      hilog.setMinLogLevel(hilog.LogLevel.INFO);
      hilog.info(DOMAIN, TAG, 'HilogNdkTest afterAll called');
    });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001
     * @tc.desc Test OH_LOG_Print with normal parameters LOG_APP/LOG_INFO
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001 start');
        try {
          const res = testNapi.ohLogPrintNormalParam();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002
     * @tc.desc Test OH_LOG_Print with all log levels (DEBUG/INFO/WARN/ERROR/FATAL)
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002 start');
        try {
          const res = testNapi.ohLogPrintAllLevels();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001
     * @tc.desc Test OH_LOG_Print return value is >= 0 on success
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001 start');
        try {
          const ret = testNapi.ohLogPrintReturn();
          expect(ret >= 0).assertTrue();
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_BOUNDARY_001
     * @tc.desc Test OH_LOG_Print with domain boundary values (0x0 and 0xFFFF)
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_BOUNDARY_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_BOUNDARY_001 start');
        try {
          const res = testNapi.ohLogPrintDomainBoundary();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_Print_BOUNDARY_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001
     * @tc.desc Test OH_LOG_IsLoggable returns true for valid loggable level
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001 start');
        try {
          const res = testNapi.ohLogIsLoggableTrue();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002
     * @tc.desc Test OH_LOG_IsLoggable returns false when level is blocked
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002 start');
        try {
          const res = testNapi.ohLogIsLoggableFalse();
          expect(res).assertEqual(false);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_BOUNDARY_001
     * @tc.desc Test OH_LOG_IsLoggable with empty tag string
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_BOUNDARY_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_BOUNDARY_001 start');
        try {
          const res = testNapi.ohLogIsLoggableEmptyTag();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_BOUNDARY_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_ERROR_001
     * @tc.desc Test OH_LOG_IsLoggable with invalid log level (100)
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_ERROR_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_ERROR_001 start');
        try {
          const res = testNapi.ohLogIsLoggableInvalidLevel();
          expect(res).assertEqual(false);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_ERROR_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001
     * @tc.desc Test OH_LOG_SetMinLogLevel to LOG_INFO and verify print succeeds
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL1
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001 start');
        try {
          const res = testNapi.ohLogSetMinLogLevelInfo();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002
     * @tc.desc Test OH_LOG_SetMinLogLevel to LOG_FATAL blocks lower level prints
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002 start');
        try {
          const res = testNapi.ohLogSetMinLogLevelFatal();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002 end');
      });

    /**
     * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_RETURN_001
     * @tc.desc Test OH_LOG_SetMinLogLevel restore to DEBUG enables previously blocked logs
     * @tc.type FUNCTION
     * @tc.size MEDIUMTEST
     * @tc.level LEVEL2
     */
    it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_RETURN_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
      function () {
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_RETURN_001 start');
        try {
          const res = testNapi.ohLogSetMinLogLevelRestore();
          expect(res).assertEqual(true);
        } catch (error) {
          hilog.error(DOMAIN, TAG, `got error: ${JSON.stringify(error)}`);
          expect().assertFail();
        }
        hilog.info(DOMAIN, TAG, 'SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_RETURN_001 end');
      });
  });
}
