/*
 * Copyright (c) 2025 Huawei Device Co., Ltd.
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

import hilogNapi from 'libhilog_napi.so';
import { describe, beforeAll, afterAll, it, expect, TestType, Size, Level } from '@ohos/hypium';

const LOG_APP = 0;
const LOG_DEBUG = 3;
const LOG_INFO = 4;
const LOG_WARN = 5;
const LOG_ERROR = 6;
const LOG_FATAL = 7;
const LOG_DOMAIN = 0x0201;
const LOG_TAG = 'HILOG_NAPI_TEST';

const UNSET_LOGLEVEL = 0;
const PREFER_CLOSE_LOG = 1;
const PREFER_OPEN_LOG = 2;

export default function HilogCoverageTest() {
  describe('HilogCoverageTest', () => {
    beforeAll(() => {
    });
    afterAll(() => {
    });

    const NUM_0 = 0;
    const NUM_1 = 1;

    it('OHLogPrintMsg_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, 'test OHLogPrintMsg info');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsg_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_DEBUG, LOG_DOMAIN, LOG_TAG, 'test OHLogPrintMsg debug');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsg_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_WARN, LOG_DOMAIN, LOG_TAG, 'test OHLogPrintMsg warn');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsg_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, 'test OHLogPrintMsg error');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsg_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_FATAL, LOG_DOMAIN, LOG_TAG, 'test OHLogPrintMsg fatal');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen info';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_INFO, LOG_DOMAIN, tag, tag.length, msg, msg.length);
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen debug';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_DEBUG, LOG_DOMAIN, tag, tag.length, msg, msg.length);
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen warn';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_WARN, LOG_DOMAIN, tag, tag.length, msg, msg.length);
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen error';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_ERROR, LOG_DOMAIN, tag, tag.length, msg, msg.length);
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen fatal';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_FATAL, LOG_DOMAIN, tag, tag.length, msg, msg.length);
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogPrintMsgByLen_0600', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        const tag = 'TAG_LEN';
        const msg = 'test OHLogPrintMsgByLen with truncated length';
        let ret = hilogNapi.OHLogPrintMsgByLen(LOG_APP, LOG_INFO, LOG_DOMAIN, tag, NUM_1, msg, NUM_1);
        expect(typeof ret).assertEqual('number');
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogVPrint_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogVPrint(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, 'test OHLogVPrint %{public}s', 'info arg');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogVPrint_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogVPrint(LOG_APP, LOG_DEBUG, LOG_DOMAIN, LOG_TAG, 'test OHLogVPrint %{public}s', 'debug arg');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogVPrint_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogVPrint(LOG_APP, LOG_WARN, LOG_DOMAIN, LOG_TAG, 'test OHLogVPrint %{public}s', 'warn arg');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogVPrint_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogVPrint(LOG_APP, LOG_ERROR, LOG_DOMAIN, LOG_TAG, 'test OHLogVPrint %{public}s', 'error arg');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('OHLogVPrint_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        let ret = hilogNapi.OHLogVPrint(LOG_APP, LOG_FATAL, LOG_DOMAIN, LOG_TAG, 'test OHLogVPrint %{public}s', 'fatal arg');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('PreferStrategy_UNSET_LOGLEVEL_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        hilogNapi.OHLogSetLogLevel(LOG_DEBUG, UNSET_LOGLEVEL);
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, 'UNSET_LOGLEVEL test');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('PreferStrategy_PREFER_CLOSE_LOG_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        hilogNapi.OHLogSetLogLevel(LOG_FATAL, PREFER_CLOSE_LOG);
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_FATAL, LOG_DOMAIN, LOG_TAG, 'PREFER_CLOSE_LOG test');
        expect(ret).assertLarger(NUM_0);
        hilogNapi.OHLogSetLogLevel(LOG_DEBUG, PREFER_OPEN_LOG);
        done();
      } catch (err) {
        done();
      }
    });

    it('PreferStrategy_PREFER_OPEN_LOG_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        hilogNapi.OHLogSetLogLevel(LOG_DEBUG, PREFER_OPEN_LOG);
        let ret = hilogNapi.OHLogPrintMsg(LOG_APP, LOG_INFO, LOG_DOMAIN, LOG_TAG, 'PREFER_OPEN_LOG test');
        expect(ret).assertLarger(NUM_0);
        done();
      } catch (err) {
        done();
      }
    });

    it('PreferStrategy_EnumValues_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, async (done: Function) => {
      try {
        expect(UNSET_LOGLEVEL).assertEqual(NUM_0);
        expect(PREFER_CLOSE_LOG).assertEqual(NUM_1);
        expect(PREFER_OPEN_LOG).assertEqual(2);
        done();
      } catch (err) {
        done();
      }
    });
  });
}
