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

import zlibtest from 'libzlibcapitest.so';
import { describe, it, expect, TestType, Size, Level } from '@ohos/hypium';

export default function ActsZlibCapiTest() {
describe('ActsZlibCapiTest', () => {

    /**
     * @tc.name   Zlib_Compress_001
     * @tc.number TC-Zlib-001
     * @tc.desc   Test compress with normal string data
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('Zlib_Compress_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
        let ret: number = zlibtest.zlibCompress(0);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_Compress_002
     * @tc.number TC-Zlib-002
     * @tc.desc   Test compress with empty data
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('Zlib_Compress_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
        let ret: number = zlibtest.zlibCompress(1);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_Compress_003
     * @tc.number TC-Zlib-003
     * @tc.desc   Test compress with large data (4096 bytes)
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('Zlib_Compress_003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
        let ret: number = zlibtest.zlibCompress(2);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_Uncompress_001
     * @tc.number TC-Zlib-004
     * @tc.desc   Test uncompress with valid compressed data and verify data integrity
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('Zlib_Uncompress_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
        let ret: number = zlibtest.zlibUncompress(0);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_Uncompress_002
     * @tc.number TC-Zlib-005
     * @tc.desc   Test uncompress with corrupted data, expect Z_DATA_ERROR handling
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('Zlib_Uncompress_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
        let ret: number = zlibtest.zlibUncompress(1);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_Uncompress_003
     * @tc.number TC-Zlib-006
     * @tc.desc   Test uncompress with insufficient output buffer, expect Z_BUF_ERROR handling
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('Zlib_Uncompress_003', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
        let ret: number = zlibtest.zlibUncompress(2);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_CompressBound_001
     * @tc.number TC-Zlib-007
     * @tc.desc   Test compressBound with normal length, verify return >= sourceLen
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL0
     */
    it('Zlib_CompressBound_001', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL0, () => {
        let ret: number = zlibtest.zlibCompressBound(0);
        expect(ret).assertEqual(0);
    });

    /**
     * @tc.name   Zlib_CompressBound_002
     * @tc.number TC-Zlib-008
     * @tc.desc   Test compressBound with zero length, verify return > 0
     * @tc.type   FUNCTION
     * @tc.size   MEDIUMTEST
     * @tc.level  LEVEL1
     */
    it('Zlib_CompressBound_002', TestType.FUNCTION | Size.MEDIUMTEST | Level.LEVEL1, () => {
        let ret: number = zlibtest.zlibCompressBound(1);
        expect(ret).assertEqual(0);
    });

});
}
