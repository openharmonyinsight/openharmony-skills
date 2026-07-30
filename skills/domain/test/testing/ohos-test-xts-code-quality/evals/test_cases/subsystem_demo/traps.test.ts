import expect from '@ohos/hypium';
import emitter from '@ohos.emitter';
import { Level } from '@ohos/hypium';

export default function testsuite() {
  describe('A094FalsePositiveTraps', () => {
    it('SUB_B_trap_asyncDoneMixed_0100', 0, async (done: Function) => {
      fetchSomething().then(data => {
        expect(data).assertEqual('ok');
        done();
      }).catch(err => {
        expect(err).assertEqual(null);
        done();
      });
    });

    it('SUB_B_trap_promiseAllSafe_0100', 0, async () => {
      let results = await Promise.all([taskA(), taskB()]);
      expect(results.length).assertEqual(2);
    });

    it('SUB_B_trap_onceAutoRemove_0100', 0, () => {
      emitter.once('event', (data) => {
        expect(data).assertEqual(1);
      });
    });

    it('SUB_B_trap_awaitSleepNoTry_0100', 0, async () => {
      await sleep(500);
      let result = await taskA();
      expect(result).assertEqual('a');
    });
  });
}

function fetchSomething() {
  return Promise.resolve('ok');
}

function taskA() {
  return Promise.resolve('a');
}

function taskB() {
  return Promise.resolve('b');
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
