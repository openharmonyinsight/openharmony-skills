import display from '@ohos.display';

/**
 * CreaseAvoidance.ets
 *
 * 官方 API 模板：
 * - display.getCurrentFoldCreaseRegion()
 * - display.convertGlobalToRelativeCoordinate(...)
 * - display.on/off('foldStatusChange', ...)
 *
 * 用法说明：
 * - 本模板用于“按真实折痕几何计算分界线”。
 * - rootGlobalYVp 需要接入页面根容器的全局 Y 偏移，避免分界线整体偏移。
 */
@Entry
@Component
struct CreaseAvoidanceExample {
  @State private rootHeightVp: number = 0;
  @State private splitLineVp: number = 0;
  @State private creaseHeightVp: number = 0;
  @State private hasCrease: boolean = false;

  // 页面根容器在全局坐标中的 Y 偏移（单位 vp）。
  // 实际接入时请在容器挂载后按工程方式更新该值。
  private rootGlobalYVp: number = 0;
  private foldStatusCallback?: (status: display.FoldStatus) => void;

  aboutToAppear() {
    this.recalculateCreaseBand();
    this.foldStatusCallback = () => {
      this.recalculateCreaseBand();
    };
    display.on('foldStatusChange', this.foldStatusCallback);
  }

  aboutToDisappear() {
    if (this.foldStatusCallback) {
      display.off('foldStatusChange', this.foldStatusCallback);
    }
  }

  private recalculateCreaseBand(): void {
    const region = display.getCurrentFoldCreaseRegion();
    if (!region || !region.creaseRects || region.creaseRects.length === 0) {
      this.hasCrease = false;
      this.creaseHeightVp = 0;
      this.splitLineVp = this.rootHeightVp > 0 ? this.rootHeightVp * 0.5 : 0;
      return;
    }

    const rect = region.creaseRects[0];
    const p1 = display.convertGlobalToRelativeCoordinate({ x: rect.left, y: rect.top }, region.displayId);
    const p2 = display.convertGlobalToRelativeCoordinate(
      { x: rect.left + rect.width, y: rect.top + rect.height },
      region.displayId
    );

    const mappedTopVp = px2vp(Math.min(p1.position.y, p2.position.y));
    const mappedBottomVp = px2vp(Math.max(p1.position.y, p2.position.y));
    const topInRootVp = mappedTopVp - this.rootGlobalYVp;

    this.creaseHeightVp = Math.max(0, mappedBottomVp - mappedTopVp);
    this.splitLineVp = topInRootVp + this.creaseHeightVp * 0.5;
    this.hasCrease = true;
  }

  @Builder
  private topArea() {
    Column() {
      Text('Upper Content')
    }
    .width('100%')
    .height('100%')
  }

  @Builder
  private bottomArea() {
    Column() {
      Text('Lower Actions')
    }
    .width('100%')
    .height('100%')
  }

  build() {
    Column() {
      if (this.hasCrease && this.splitLineVp > 0 && this.rootHeightVp > 0) {
        const upperHeightVp = Math.max(0, this.splitLineVp - this.creaseHeightVp * 0.5);
        const lowerHeightVp = Math.max(0, this.rootHeightVp - upperHeightVp - this.creaseHeightVp);

        Column() {
          this.topArea();
        }
        .height(`${upperHeightVp}vp`)

        Row()
          .width('100%')
          .height(`${this.creaseHeightVp}vp`)
          .backgroundColor('#E8E8E8')

        Column() {
          this.bottomArea();
        }
        .height(`${lowerHeightVp}vp`)
      } else {
        // 无折痕信息时的兜底布局
        Column() {
          this.topArea();
        }
        .layoutWeight(1)

        Column() {
          this.bottomArea();
        }
        .layoutWeight(1)
      }
    }
    .width('100%')
    .height('100%')
    .onAreaChange((_, area) => {
      this.rootHeightVp = Number(area.height);
      this.recalculateCreaseBand();
    })
  }
}
