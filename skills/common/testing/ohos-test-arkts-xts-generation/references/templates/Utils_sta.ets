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
import { router } from '@kit.ArkUI';

export default class Utils {
  static sleep(time: number): Promise<void> {
    return new Promise<void>((resolve, reject) => {
      try {
        setTimeout(() => {
          resolve()
        }, time)
      } catch (err) {
        console.error('sleep error:' + err);
        reject()
      }
    }).then(() => {
      console.info(`sleep ${time} over...`)
    }) as Promise<void>;
  }

  static async pushPage(obj: ESObject) {
    try {
      let pages = router.getState();
      let pageParams: ESObject = router.getParams() as ESObject;
      console.info('get ' + obj.pageName + ' state pages: ' + JSON.stringify(pages));
      if (pageParams && pageParams['view'] && obj.targetView != pageParams['view']['targetView']) {
        console.info('get ' + obj.pageName + ' params: ' + JSON.stringify(pageParams));
        console.info('pageParams.view.targetView: ' + pageParams['view']['targetView']);
        console.info('targetView: ' + obj.targetView);
        await Utils.back();
        pages = router.getState();
      }

      if (!(obj.pageName == pages.name)) {
        console.info('get ' + obj.pageName + ' state pages.name:' + JSON.stringify(pages.name));
        let result = await router.pushUrl({
          url: obj.pageUrl,
          params: {
            view: obj
          }
        });
        await Utils.sleep(2000);
        console.info('push ' + obj.pageName + ' page result:' + JSON.stringify(result));
      }
    } catch (err) {
      console.error('push ' + obj.pageName + ' page error:' + err);
    }
  }

  static async back() {
    if (!('Index' == router.getState().name)) {
      router.back()
    }
    await Utils.sleep(1000);
    router.clear();
  }

  static async pushPageByParams(obj: ESObject, params: ESObject) {
    try {
      let pages = router.getState();
      let pageParams: ESObject = router.getParams() as ESObject;
      console.info('get ' + obj.pageName + ' state pages: ' + JSON.stringify(pages));
      if (pageParams && pageParams['view'] && obj.targetView != pageParams['view']['targetView']) {
        await Utils.back();
        pages = router.getState();
      }

      if (!(obj.pageName == pages.name)) {
        console.info('get ' + obj.pageName + ' state pages.name:' + JSON.stringify(pages.name));
        let result = await router.pushUrl({
          url: obj.pageUrl,
          params: params
        });
        await Utils.sleep(2000);
        console.info('push ' + obj.pageName + ' page result:' + JSON.stringify(result));
      }
    } catch (err) {
      console.error('push ' + obj.pageName + ' page error:' + err);
    }
  }

  static async replacePage(obj: ESObject) {
    try {
      router.clear();
      let pages = router.getState();
      console.info('get ' + obj.pageName + ' state pages: ' + JSON.stringify(pages));
      if (!(obj.pageName == pages.name)) {
        console.info('get ' + obj.pageName + ' state pages.name:' + JSON.stringify(pages.name));
        let result = await router.replaceUrl({
          url: obj.pageUrl,
          params: {
            view: obj
          }
        });
        await Utils.sleep(2000);
        console.info('replace ' + obj.pageName + ' page result:' + JSON.stringify(result));
      }
    } catch (err) {
      console.error('replace ' + obj.pageName + ' page error:' + err);
    }
  }
}
