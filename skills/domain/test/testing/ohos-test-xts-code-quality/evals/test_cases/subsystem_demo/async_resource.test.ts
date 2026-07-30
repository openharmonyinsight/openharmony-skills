import expect from '@ohos/hypium';
import emitter from '@ohos.emitter';

export default function testsuite() {
  describe('AsyncResourceTest', () => {
    beforeAll(() => {
      let res = createResource();
    });

    it('SUB_demo_R201_asyncNoDone_0100', 0, () => {
      setTimeout(() => {
        console.info('async work');
      }, 1000);
    });

    it('SUB_demo_R202_promiseNoCatch_0100', 0, () => {
      fetchSomething().then(data => {
        expect(data).assertEqual('ok');
      });
    });

    it('SUB_demo_R203_concurrent_0100', 0, async () => {
      let conn = createConnection();
      await conn.open();
      conn.start();
      await conn.close();
    });

    it('SUB_demo_R204_listenerNoOff_0100', 0, () => {
      emitter.on('event', (data) => {
        expect(data).assertEqual(1);
      });
    });

    it('SUB_demo_R206_globalStateA_0100', 0, () => {
      globalThis.sharedCounter = 0;
      globalThis.sharedCounter += 1;
      expect(globalThis.sharedCounter).assertEqual(1);
    });

    it('SUB_demo_R206_globalStateB_0100', 0, () => {
      expect(globalThis.sharedCounter).assertEqual(1);
    });

    it('SUB_demo_R018_dupCase_0100', 0, () => {
      expect(1).assertEqual(1);
    });

    it('SUB_demo_R018_dupCase_0100', 0, () => {
      expect(2).assertEqual(2);
    });
  });
}

function createResource() {
  return { id: 1 };
}

function fetchSomething() {
  return Promise.resolve('ok');
}

function createConnection() {
  return {
    open() { return Promise.resolve(); },
    start() { return Promise.resolve(); },
    close() { return Promise.resolve(); },
  };
}
