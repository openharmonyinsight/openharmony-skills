import hilog from '@ohos.hilog';
import TestRunner from '@ohos.application.testRunner';
import AbilityDelegatorRegistry from '@ohos.app.ability.abilityDelegatorRegistry';

let abilityDelegator: AbilityDelegatorRegistry.AbilityDelegator | undefined = undefined;
let tag = 'ActsZlibCapiTest';

async function onAbilityCreateCallback() {
    hilog.info(0x0000, tag, '%{public}s', 'onAbilityCreateCallback');
}

async function addAbilityMonitorCallback(err: Error) {
    hilog.info(0x0000, tag, '%{public}s', 'addAbilityMonitorCallback : ' + JSON.stringify(err) ?? '');
}

export default class OpenHarmonyTestRunner implements TestRunner {
    onPrepare() {
        hilog.info(0x0000, tag, '%{public}s', 'OpenHarmonyTestRunner OnPrepare ');
    }

    async onRun() {
        hilog.info(0x0000, tag, '%{public}s', 'OpenHarmonyTestRunner onRun run');
        abilityDelegator = AbilityDelegatorRegistry.getAbilityDelegator();
        let testAbilityName = 'TestAbility';
        let lMonitor: AbilityDelegatorRegistry.AbilityMonitor = {
            abilityName: testAbilityName,
            onAbilityCreate: onAbilityCreateCallback,
        };
        abilityDelegator.addAbilityMonitor(lMonitor, addAbilityMonitorCallback);
        let cmd = 'aa start -d 0 -a TestAbility -b com.actszlibcapitest.test';
        let cmdResult: AbilityDelegatorRegistry.CmdResult = await abilityDelegator.executeShellCommand(cmd);
        hilog.info(0x0000, tag, '%{public}s', 'cmd : ' + cmd + ' cmdResult : ' + JSON.stringify(cmdResult) ?? '');
    }
}
