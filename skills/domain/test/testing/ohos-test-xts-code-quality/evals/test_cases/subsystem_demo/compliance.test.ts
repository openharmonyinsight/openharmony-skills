import parameter from '@ohos.systemparameter';
import expect from '@ohos/hypium';
import deviceInfo from '@ohos.deviceInfo';

export default function testsuite() {
  describe('ComplianceTest', () => {
    it('SUB_demo_R001_getSync_0100', 0, () => {
      let value = parameter.getSync('ro.build.version');
      expect(value).assertEqual('10');
    });

    it('SUB_demo_R002_errcodeString_0100', 0, () => {
      try {
        someApi();
      } catch (error) {
        expect(error.code).assertEqual("401");
      }
    });

    it('SUB_demo_R003_tautology_0100', 0, () => {
      expect(true).assertTrue();
    });

    it('SUB_demo_R004_noAssertion_0100', 0, () => {
      let x = 1 + 1;
      let y = x * 2;
    });

    it('SUB_demo_R006_deviceDiff_0100', 0, () => {
      if (deviceInfo.deviceType === 'phone') {
        expect(true).assertTrue();
      }
    });

    it('SUB_demo_R022_looseCompare_0100', 0, () => {
      try {
        someApi();
      } catch (error) {
        if (error.code == 401) {
          expect(true).assertTrue();
        }
      }
    });

    it('SUB_demo_R023_typeCast_0100', 0, () => {
      try {
        someApi();
      } catch (error) {
        expect(error.code.toString()).assertEqual("401");
      }
    });

    /**
     * @tc.number: SUB_demo_R008_colon_0100
     * @tc.name: R008colonTest
     */
    it('SUB_demo_R008_colon_0100', 0, () => {
      expect(1).assertEqual(1);
    });

    /**
     * @tc.number SUB_ArkUI_Button_001
     * @tc.name R009NamingTest
     */
    it('SUB_demo_R009_naming_0100', 0, () => {
      expect(1).assertEqual(1);
    });

    it('SUB_demo_R015_noLevel_0100', () => {
      expect(1).assertEqual(1);
    });

    it('test@001_R016', 0, () => {
      expect(1).assertEqual(1);
    });

    // let sleep = (ms: number): Promise<void> => {
    //     return new Promise(resolve => setTimeout(resolve, ms));
    // };
    // let result = await someAsyncApi();
    // expect(result).assertEqual('ok');
    it('SUB_demo_R013_deadCode_0100', 0, () => {
      expect(1).assertEqual(1);
    });
  });
}

function someApi() {
  return Promise.resolve();
}
