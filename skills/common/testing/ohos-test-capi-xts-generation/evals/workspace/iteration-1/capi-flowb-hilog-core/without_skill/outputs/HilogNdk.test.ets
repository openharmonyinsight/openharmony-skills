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
import { describe, beforeAll, beforeEach, afterEach, afterAll, it, expect, TestType, Level, Size } from '@ohos/hypium'
// @ts-ignore
import hilogndk from 'libhilogndk.so'

const LOG_APP = 0;
const LOG_DEBUG = 3;
const LOG_INFO = 4;
const LOG_WARN = 5;
const LOG_ERROR = 6;
const LOG_FATAL = 7;

export default function HilogNdkTest() {
describe('HilogNdkTest', function () {

    beforeAll(function () {
        console.info('HilogNdkTest beforeAll called');
    })

    afterAll(function () {
        hilogndk.oHLogSetMinLogLevel(LOG_INFO);
        console.info('HilogNdkTest afterAll called');
    })

    beforeEach(function () {
        console.info('HilogNdkTest beforeEach called');
    })

    afterEach(function () {
        console.info('HilogNdkTest afterEach called');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0100
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0100
     * @tc.desc   Test OH_LOG_Print with LOG_DEBUG level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0100 start');
        const res = hilogndk.oHLogPrintDebugLevel();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0100 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0200
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0200
     * @tc.desc   Test OH_LOG_Print with LOG_INFO level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0200 start');
        const res = hilogndk.oHLogPrintInfoLevel();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0200 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0300
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0300
     * @tc.desc   Test OH_LOG_Print with LOG_WARN level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0300 start');
        const res = hilogndk.oHLogPrintWarnLevel();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0300 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0400
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0400
     * @tc.desc   Test OH_LOG_Print with LOG_ERROR level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0400 start');
        const res = hilogndk.oHLogPrintErrorLevel();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0400 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0500
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0500
     * @tc.desc   Test OH_LOG_Print with LOG_FATAL level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0500 start');
        const res = hilogndk.oHLogPrintFatalLevel();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0500 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0600
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0600
     * @tc.desc   Test OH_LOG_Print with generic parameters
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0600', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0600 start');
        const ret = hilogndk.oHLogPrint(LOG_APP, LOG_INFO, 0x3200, 'testTag', 'generic print test');
        expect(ret >= 0).assertTrue();
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0600 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0700
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0700
     * @tc.desc   Test OH_LOG_Print with format arguments
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0700', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0700 start');
        const ret = hilogndk.oHLogPrintWithArgs(LOG_APP, LOG_INFO, 0x3200, 'testTag', '%{public}s', 'formatArg');
        expect(ret >= 0).assertTrue();
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0700 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0800
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0800
     * @tc.desc   Test OH_LOG_Print with {private} identifier
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0800', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0800 start');
        const res = hilogndk.oHLogPrintPrivateArg();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0800 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_0900
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_0900
     * @tc.desc   Test OH_LOG_Print with {public} identifier
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_0900', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0900 start');
        const res = hilogndk.oHLogPrintPublicArg();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_0900 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_1000
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_1000
     * @tc.desc   Test OH_LOG_Print with boundary domain 0x0000
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_1000', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1000 start');
        const res = hilogndk.oHLogPrintBoundaryDomain0();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1000 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_1100
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_1100
     * @tc.desc   Test OH_LOG_Print with boundary domain 0xFFFF
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_1100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1100 start');
        const res = hilogndk.oHLogPrintBoundaryDomainFFFF();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1100 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_1200
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_1200
     * @tc.desc   Test OH_LOG_Print with empty tag
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_1200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1200 start');
        const res = hilogndk.oHLogPrintEmptyTag();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1200 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogPrint_1300
     * @tc.number SUB_DFX_DFT_Hilog_OHLogPrint_1300
     * @tc.desc   Test OH_LOG_Print with empty format string
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogPrint_1300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1300 start');
        const res = hilogndk.oHLogPrintEmptyFmt();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogPrint_1300 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0100
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0100
     * @tc.desc   Test OH_LOG_IsLoggable with LOG_DEBUG level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0100 start');
        const res = hilogndk.oHLogIsLoggableDebug();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0100 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0200
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0200
     * @tc.desc   Test OH_LOG_IsLoggable with LOG_INFO level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0200 start');
        const res = hilogndk.oHLogIsLoggableInfo();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0200 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0300
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0300
     * @tc.desc   Test OH_LOG_IsLoggable with LOG_WARN level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0300 start');
        const res = hilogndk.oHLogIsLoggableWarn();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0300 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0400
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0400
     * @tc.desc   Test OH_LOG_IsLoggable with LOG_ERROR level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0400 start');
        const res = hilogndk.oHLogIsLoggableError();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0400 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0500
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0500
     * @tc.desc   Test OH_LOG_IsLoggable with LOG_FATAL level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0500 start');
        const res = hilogndk.oHLogIsLoggableFatal();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0500 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0600
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0600
     * @tc.desc   Test OH_LOG_IsLoggable with invalid level (100) returns false
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0600', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0600 start');
        const res = hilogndk.oHLogIsLoggableInvalidLevel();
        expect(res).assertEqual(false);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0600 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0700
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0700
     * @tc.desc   Test OH_LOG_IsLoggable with empty tag
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0700', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0700 start');
        const res = hilogndk.oHLogIsLoggableEmptyTag();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0700 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0800
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0800
     * @tc.desc   Test OH_LOG_IsLoggable with boundary domain 0x0000
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0800', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0800 start');
        const res = hilogndk.oHLogIsLoggableBoundaryDomain0();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0800 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_0900
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_0900
     * @tc.desc   Test OH_LOG_IsLoggable with boundary domain 0xFFFF
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0900', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0900 start');
        const res = hilogndk.oHLogIsLoggableBoundaryDomainFFFF();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_0900 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogIsLoggable_1000
     * @tc.number SUB_DFX_DFT_Hilog_OHLogIsLoggable_1000
     * @tc.desc   Test OH_LOG_IsLoggable with generic parameters
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogIsLoggable_1000', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_1000 start');
        const res = hilogndk.oHLogIsLoggable(0x3200, 'testTag', LOG_INFO);
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogIsLoggable_1000 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0100
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0100
     * @tc.desc   Test OH_LOG_SetMinLogLevel to LOG_DEBUG, all levels loggable
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0100', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0100 start');
        const res = hilogndk.oHLogSetMinLogLevelDebug();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0100 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0200
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0200
     * @tc.desc   Test OH_LOG_SetMinLogLevel to LOG_INFO, DEBUG filtered
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0200', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0200 start');
        const res = hilogndk.oHLogSetMinLogLevelInfo();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0200 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0300
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0300
     * @tc.desc   Test OH_LOG_SetMinLogLevel to LOG_WARN, INFO filtered
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0300', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0300 start');
        const res = hilogndk.oHLogSetMinLogLevelWarn();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0300 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0400
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0400
     * @tc.desc   Test OH_LOG_SetMinLogLevel to LOG_ERROR, WARN filtered
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0400', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0400 start');
        const res = hilogndk.oHLogSetMinLogLevelError();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0400 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0500
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0500
     * @tc.desc   Test OH_LOG_SetMinLogLevel to LOG_FATAL, ERROR filtered
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0500', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0500 start');
        const res = hilogndk.oHLogSetMinLogLevelFatal();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0500 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0600
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0600
     * @tc.desc   Test OH_LOG_SetMinLogLevel then OH_LOG_Print filtered by level
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0600', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0600 start');
        const res = hilogndk.oHLogSetMinLogLevelThenPrint();
        expect(res).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0600 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0700
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0700
     * @tc.desc   Test OH_LOG_SetMinLogLevel with generic set and check
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0700', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0700 start');
        hilogndk.oHLogSetMinLogLevel(LOG_ERROR);
        const loggableError = hilogndk.oHLogIsLoggable(0x3200, 'testTag', LOG_ERROR);
        const loggableInfo = hilogndk.oHLogIsLoggable(0x3200, 'testTag', LOG_INFO);
        expect(loggableError).assertEqual(true);
        expect(loggableInfo).assertEqual(false);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0700 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0800
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0800
     * @tc.desc   Test OH_LOG_SetMinLogLevelAndCheck with WARN set, check INFO and WARN
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0800', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0800 start');
        const infoLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_WARN, LOG_INFO);
        expect(infoLoggable).assertEqual(false);
        const warnLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_WARN, LOG_WARN);
        expect(warnLoggable).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0800 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0900
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0900
     * @tc.desc   Test OH_LOG_SetMinLogLevelAndCheck with FATAL set, check ERROR and FATAL
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0900', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0900 start');
        const errorLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_FATAL, LOG_ERROR);
        expect(errorLoggable).assertEqual(false);
        const fatalLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_FATAL, LOG_FATAL);
        expect(fatalLoggable).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_0900 end');
    })

    /**
     * @tc.name   SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_1000
     * @tc.number SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_1000
     * @tc.desc   Test OH_LOG_SetMinLogLevel with DEBUG set, check all levels loggable
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL2
     */
    it('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_1000', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2, function () {
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_1000 start');
        const debugLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_DEBUG, LOG_DEBUG);
        expect(debugLoggable).assertEqual(true);
        const infoLoggable = hilogndk.oHLogSetMinLogLevelAndCheck(LOG_DEBUG, LOG_INFO);
        expect(infoLoggable).assertEqual(true);
        console.info('SUB_DFX_DFT_Hilog_OHLogSetMinLogLevel_1000 end');
    })
})
}
