import UIAbility from '@ohos.app.ability.UIAbility';
import hilog from '@ohos.hilog';
import Window from '@ohos.window';

export default class EntryAbility extends UIAbility {
    onCreate(want, launchParam) {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onCreate');
    }

    onDestroy() {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onDestroy');
    }

    onWindowStageCreate(windowStage: Window.WindowStage) {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onWindowStageCreate');
        windowStage.loadContent('pages/Index', (err, data) => {
            if (err.code) {
                hilog.error(0x0000, 'testTag', 'Failed to load the content. Cause: %{public}s',
                    JSON.stringify(err) ?? '');
                return;
            }
            hilog.info(0x0000, 'testTag', 'Succeeded in loading the content. Data: %{public}s',
                JSON.stringify(data) ?? '');
        });
    }

    onWindowStageDestroy() {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onWindowStageDestroy');
    }

    onForeground() {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onForeground');
    }

    onBackground() {
        hilog.info(0x0000, 'testTag', '%{public}s', 'EntryAbility onBackground');
    }
}
