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

export const OH_LOG_PrintMsg_ParamTest: (type: number, level: number, domain: number, tag: string, message: string) => number;
export const OH_LOG_PrintMsg_LevelTest: (type: number, level: number, domain: number, tag: string, message: string) => number;
export const OH_LOG_PrintMsg_EmptyMsgTest: (type: number, level: number, domain: number, tag: string, message: string) => number;
export const OH_LOG_PrintMsgByLen_ParamTest: (type: number, level: number, domain: number, tag: string, message: string) => number;
export const OH_LOG_PrintMsgByLen_BoundaryTest: (type: number, level: number, domain: number, tag: string, tagLen: number, message: string, messageLen: number) => number;
export const OH_LOG_PrintMsgByLen_ReturnTest: (type: number, level: number, domain: number, tag: string, tagLen: number, message: string, messageLen: number) => number;
export const OH_LOG_VPrint_ParamTest: (type: number, level: number, domain: number, tag: string, fmt: string, message: string) => number;
export const OH_LOG_VPrint_FmtIntTest: (type: number, level: number, domain: number, tag: string, fmt: string, intArg: number) => number;
export const OH_LOG_VPrint_ReturnTest: (type: number, level: number, domain: number, tag: string, message: string) => number;
export const PreferStrategy_ParamTest: (level: number, strategy: number) => number;
export const PreferStrategy_CloseLogTest: (level: number, strategy: number) => number;
export const PreferStrategy_OpenLogTest: (level: number, strategy: number) => number;
