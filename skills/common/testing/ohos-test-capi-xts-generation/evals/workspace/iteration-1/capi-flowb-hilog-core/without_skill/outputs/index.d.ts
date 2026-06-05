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

export const oHLogPrint: (logType: number, logLevel: number, domain: number, tag: string, fmt: string) => number;
export const oHLogPrintWithArgs: (logType: number, logLevel: number, domain: number, tag: string, fmt: string, arg: string) => number;
export const oHLogPrintDebugLevel: () => boolean;
export const oHLogPrintInfoLevel: () => boolean;
export const oHLogPrintWarnLevel: () => boolean;
export const oHLogPrintErrorLevel: () => boolean;
export const oHLogPrintFatalLevel: () => boolean;
export const oHLogPrintPrivateArg: () => boolean;
export const oHLogPrintPublicArg: () => boolean;
export const oHLogPrintBoundaryDomain0: () => boolean;
export const oHLogPrintBoundaryDomainFFFF: () => boolean;
export const oHLogPrintEmptyTag: () => boolean;
export const oHLogPrintEmptyFmt: () => boolean;
export const oHLogIsLoggable: (domain: number, tag: string, level: number) => boolean;
export const oHLogIsLoggableDebug: () => boolean;
export const oHLogIsLoggableInfo: () => boolean;
export const oHLogIsLoggableWarn: () => boolean;
export const oHLogIsLoggableError: () => boolean;
export const oHLogIsLoggableFatal: () => boolean;
export const oHLogIsLoggableInvalidLevel: () => boolean;
export const oHLogIsLoggableEmptyTag: () => boolean;
export const oHLogIsLoggableBoundaryDomain0: () => boolean;
export const oHLogIsLoggableBoundaryDomainFFFF: () => boolean;
export const oHLogSetMinLogLevel: (level: number) => void;
export const oHLogSetMinLogLevelAndCheck: (setLevel: number, checkLevel: number) => boolean;
export const oHLogSetMinLogLevelDebug: () => boolean;
export const oHLogSetMinLogLevelInfo: () => boolean;
export const oHLogSetMinLogLevelWarn: () => boolean;
export const oHLogSetMinLogLevelError: () => boolean;
export const oHLogSetMinLogLevelFatal: () => boolean;
export const oHLogSetMinLogLevelThenPrint: () => boolean;
