import { describe, it, expect, TestType, Size, Level, beforeAll, afterAll } from '@ohos/hypium';
import hilog from '@ohos.hilog';
import testNapi from 'libhilogndk.so';

export default function HilogNdkNewTest() {
    describe('HilogNdkNewTest', function () {
        beforeAll(function () {
            hilog.setMinLogLevel(hilog.LogLevel.DEBUG);
        });

        afterAll(function () {
            hilog.setMinLogLevel(hilog.LogLevel.INFO);
        });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001
         * @tc.desc OH_LOG_Print 正常参数 LOG_INFO 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogPrintInfoLevel();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002
         * @tc.desc OH_LOG_Print 正常参数 LOG_DEBUG 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogPrintDebugLevel();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_003
         * @tc.desc OH_LOG_Print 正常参数 LOG_WARN 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogPrintWarnLevel();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_004
         * @tc.desc OH_LOG_Print 正常参数 LOG_FATAL 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogPrintFatalLevel();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_005
         * @tc.desc OH_LOG_Print domain 为 0
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_005', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogPrintDomainZero();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_006
         * @tc.desc OH_LOG_Print domain 为 0xFFFF
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_PARAM_006', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogPrintDomainMax();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001
         * @tc.desc OH_LOG_Print 返回值验证
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_Print_RETURN_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogPrintReturnTest();
                expect(result).assertLargerThanOrEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001
         * @tc.desc OH_LOG_IsLoggable 正常参数 LOG_DEBUG 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogIsLoggableDebug();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002
         * @tc.desc OH_LOG_IsLoggable LOG_INFO 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogIsLoggableInfo();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_003
         * @tc.desc OH_LOG_IsLoggable LOG_WARN 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableWarn();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_004
         * @tc.desc OH_LOG_IsLoggable LOG_ERROR 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableError();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_005
         * @tc.desc OH_LOG_IsLoggable LOG_FATAL 级别
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_005', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableFatal();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_006
         * @tc.desc OH_LOG_IsLoggable 无效日志级别返回 false
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_006', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableInvalidLevel();
                expect(result).assertFalse();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_007
         * @tc.desc OH_LOG_IsLoggable domain 为 0
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_007', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableDomainZero();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_008
         * @tc.desc OH_LOG_IsLoggable domain 为 0xFFFF
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_PARAM_008', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL2,
            function () {
                let result = testNapi.OHLogIsLoggableDomainMax();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_001
         * @tc.desc OH_LOG_IsLoggable 返回 true
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogIsLoggableReturnTrue();
                expect(result).assertTrue();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_002
         * @tc.desc OH_LOG_IsLoggable 返回 false (超出范围 domain)
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_IsLoggable_RETURN_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogIsLoggableReturnFalse();
                expect(result).assertFalse();
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001
         * @tc.desc OH_LOG_SetMinLogLevel 设置 LOG_INFO 后过滤 DEBUG
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
            function () {
                let result = testNapi.OHLogSetMinLogLevelInfo();
                expect(result).assertEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002
         * @tc.desc OH_LOG_SetMinLogLevel 设置 LOG_WARN 后过滤 INFO
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
            function () {
                let result = testNapi.OHLogSetMinLogLevelWarn();
                expect(result).assertEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_003
         * @tc.desc OH_LOG_SetMinLogLevel 设置 LOG_ERROR 后过滤 WARN
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
            function () {
                let result = testNapi.OHLogSetMinLogLevelError();
                expect(result).assertEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_004
         * @tc.desc OH_LOG_SetMinLogLevel 设置 LOG_FATAL 后过滤 ERROR
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_004', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0,
            function () {
                let result = testNapi.OHLogSetMinLogLevelFatal();
                expect(result).assertEqual(0);
            });

        /**
         * @tc.name SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_005
         * @tc.desc OH_LOG_SetMinLogLevel 设置 LOG_DEBUG 所有级别通过
         * @tc.type FUNC
         */
        it('SUB_HIVIEWDFX_HILOG_OH_LOG_SetMinLogLevel_PARAM_005', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1,
            function () {
                let result = testNapi.OHLogSetMinLogLevelDebug();
                expect(result).assertEqual(0);
            });
    });
}
