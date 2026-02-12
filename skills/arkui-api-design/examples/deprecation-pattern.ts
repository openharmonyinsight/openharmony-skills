/**
 * Example: API Deprecation Pattern with Migration Guide
 *
 * This example demonstrates how to properly deprecate existing APIs
 * while maintaining backward compatibility and providing clear migration paths.
 */

import { Resource } from '@kit.ArkUI';

// Type definitions
type Length = string | number;
type ResourceColor = string | Resource | Color;

/**
 * Button attribute class demonstrating API deprecation patterns.
 *
 * @since 8
 */
class ButtonAttribute {
  // Private properties
  private width_: Length = 200;
  private height_: Length = 40;
  private backgroundColor_: ResourceColor = '#007DFF';

  // ==================== DEPRECATION PATTERN 1: Unit Change ====================

  /**
   * Sets the button width in pixels.
   *
   * @param value Width value in px. Valid range: 0-10000px.
   * @deprecated Use width() instead. width() uses vp (virtual pixels) by default,
   *             which provides better cross-device compatibility.
   *             VP scales automatically with screen density.
   *             Conversion: 1vp ≈ 1px on a 160dpi screen.
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration guide:
   * // Before: Button().widthPx(200)
   * // After:  Button().width(200)
   *
   * // Note: The value remains the same, but the unit changes from px to vp.
   * //       VP automatically scales on different screen densities.
   *
   * Button().widthPx(200)  // Old API (deprecated)
   * Button().width(200)    // New API (recommended)
   */
  widthPx(value: number | string | undefined): ButtonAttribute {
    // Convert px to vp and call new API
    // For backward compatibility, we assume the conversion ratio
    const vpValue = this.pxToVp(value ?? 200);
    return this.width(vpValue);
  }

  /**
   * Sets the button width.
   *
   * @param value Width value in vp or percentage.
   *              Valid range: 0-10000vp or '0%'-'100%'.
   *              If undefined, restores default width (200vp).
   * @unit vp
   * @since 10
   * @example
   * // Direct value in vp
   * Button().width(200)
   *
   * // With percentage
   * Button().width('50%')
   *
   * // With resource reference
   * Button().width($r('app.float.button_width'))
   */
  width(value: number | string | Length | Resource | undefined): ButtonAttribute {
    this.width_ = value ?? 200;
    return this;
  }

  // ==================== DEPRECATION PATTERN 2: Method Renaming ====================

  /**
   * Sets the button height.
   *
   * @param value Height value in px. Valid range: 0-10000px.
   * @deprecated Renamed to height(). The new API uses vp by default.
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration:
   * // Before: Button().setHeight(40)
   * // After:  Button().height(40)
   */
  setHeight(value: number | undefined): ButtonAttribute {
    return this.height(value);
  }

  /**
   * Sets the button height.
   *
   * @param value Height value in vp. Valid range: 0-10000vp.
   *              If undefined, restores default height (40vp).
   * @unit vp
   * @since 10
   */
  height(value: number | string | Length | Resource | undefined): ButtonAttribute {
    this.height_ = value ?? 40;
    return this;
  }

  // ==================== DEPRECATION PATTERN 3: Parameter Type Change ====================

  /**
   * Sets the background color.
   *
   * @param value Background color as hex string (#RRGGBB).
   * @deprecated Use backgroundColor() instead.
   *             The new API supports Resource type for theming:
   *             - Hex color: '#FF0000'
   *             - Color name: 'red'
   *             - Resource: $r('app.color.primary')
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration:
   * // Before: Button().bgColor('#FF0000')
   * // After:  Button().backgroundColor('#FF0000')
   * // After (with resource): Button().backgroundColor($r('app.color.primary'))
   */
  bgColor(value: string | undefined): ButtonAttribute {
    return this.backgroundColor(value);
  }

  /**
   * Sets the background color.
   *
   * @param value Background color value or resource reference.
   *              Accepts hex color (#RRGGBB, #AARRGGBB),
   *              color name, or resource reference ($r('app.color.xxx')).
   *              If undefined, restores default color (#007DFF).
   * @since 10
   * @example
   * // Hex color
   * Button().backgroundColor('#FF0000')
   *
   * // Color name
   * Button().backgroundColor('red')
   *
   * // Resource reference for theming
   * Button().backgroundColor($r('app.color.primary'))
   * Button().backgroundColor($r('sys.color.ohos_id_color_primary'))
   */
  backgroundColor(value: ResourceColor | undefined): ButtonAttribute {
    this.backgroundColor_ = value ?? '#007DFF';
    return this;
  }

  // ==================== DEPRECATION PATTERN 4: Split into Multiple APIs ====================

  /**
   * Sets the button text style.
   *
   * @param options Text style options including fontSize, fontColor, fontWeight, etc.
   * @deprecated Use individual modifiers instead:
   *             - fontSize() for font size
   *             - fontColor() for font color
   *             - fontWeight() for font weight
   *             - fontFamily() for font family
   *             This provides better type safety and clearer API.
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration:
   * // Before:
   * // Button().textStyle({
   * //   fontSize: 18,
   * //   fontColor: '#000000',
   * //   fontWeight: 'bold'
   * // })
   *
   * // After:
   * // Button()
   * //   .fontSize(18)
   * //   .fontColor('#000000')
   * //   .fontWeight(FontWeight.Bold)
   */
  textStyle(options: TextStyleOptions | undefined): ButtonAttribute {
    if (options === undefined) {
      return this;
    }

    // Convert to individual API calls
    if (options.fontSize !== undefined) {
      this.fontSize(options.fontSize);
    }
    if (options.fontColor !== undefined) {
      this.fontColor(options.fontColor);
    }
    if (options.fontWeight !== undefined) {
      this.fontWeight(options.fontWeight);
    }

    return this;
  }

  /**
   * Sets the font size of button text.
   *
   * @param value Font size in fp. Valid range: 0-1000fp.
   *              If undefined, restores default size (16fp).
   * @unit fp
   * @since 10
   */
  fontSize(value: number | string | Length | Resource | undefined): ButtonAttribute {
    // Implementation...
    return this;
  }

  /**
   * Sets the font color of button text.
   *
   * @param value Font color value or resource reference.
   *              If undefined, restores default color (#FFFFFF).
   * @since 10
   */
  fontColor(value: ResourceColor | undefined): ButtonAttribute {
    // Implementation...
    return this;
  }

  /**
   * Sets the font weight of button text.
   *
   * @param value Font weight value.
   *              If undefined, restores default (FontWeight.Normal).
   * @since 10
   */
  fontWeight(value: FontWeight | undefined): ButtonAttribute {
    // Implementation...
    return this;
  }

  // ==================== DEPRECATION PATTERN 5: Behavior Change ====================

  /**
   * Sets whether the button responds to user interaction.
   *
   * @param value Touchable state.
   *              - true: Button responds to touch
   *              - false: Button does not respond to touch
   * @deprecated Split into two separate APIs for clarity:
   *             - enabled() controls whether button is enabled/disabled
   *             - touchable() controls whether button responds to touch
   *             This provides more granular control.
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration:
   * // Before: Button().touchable(false)
   * // After:  Button().enabled(false)
   *
   * // Note: The new enabled() API is more semantically clear.
   * //       Use touchable() only when you need a button that is
   *       enabled but does not respond to touch (rare case).
   */
  touchable(value: boolean | undefined): ButtonAttribute {
    // Map to enabled() for backward compatibility
    return this.enabled(value ?? true);
  }

  /**
   * Sets whether the button is enabled.
   *
   * @param value Enable state.
   *              - true: Button can interact with user (default)
   *              - false: Button is disabled and cannot interact
   * @since 10
   */
  enabled(value: boolean | undefined): ButtonAttribute {
    // Implementation...
    return this;
  }

  // ==================== DEPRECATION PATTERN 6: Complete Replacement ====================

  /**
   * Sets the button style using a legacy style object.
   *
   * @param style Legacy style configuration.
   * @deprecated Use individual modifier methods instead.
   *             The new API provides:
   *             - Better type safety
   *             - IDE autocomplete support
   *             - Clearer code intent
   *             - JSDOC documentation for each property
   * @deprecated_since 10
   * @since 8
   * @example
   * // Migration:
   * // Before:
   * // Button().style({
   * //   width: 200,
   * //   height: 40,
   * //   backgroundColor: '#FF0000',
   * //   fontSize: 18
   * // })
   *
   * // After:
   * // Button()
   * //   .width(200)
   * //   .height(40)
   * //   .backgroundColor('#FF0000')
   * //   .fontSize(18)
   *
   * // Benefits:
   * // - Each modifier has its own JSDOC
   * // - Better IDE autocomplete
   * // - Type checking for each property
   * // - Easier to read and maintain
   */
  style(style: LegacyButtonStyle | undefined): ButtonAttribute {
    if (style === undefined) {
      return this;
    }

    // Convert to individual API calls
    if (style.width !== undefined) {
      this.width(style.width);
    }
    if (style.height !== undefined) {
      this.height(style.height);
    }
    if (style.backgroundColor !== undefined) {
      this.backgroundColor(style.backgroundColor);
    }
    if (style.fontSize !== undefined) {
      this.fontSize(style.fontSize);
    }

    return this;
  }

  // ==================== Helper Methods ====================

  /**
   * Converts px value to vp.
   * Conversion ratio: 1vp = 1px at 160dpi (baseline).
   *
   * @param pxValue Value in px.
   * @returns Value in vp.
   */
  private pxToVp(pxValue: number | string): number {
    const numValue = typeof pxValue === 'string' ? parseFloat(pxValue) : pxValue;
    // Simplified conversion (actual implementation would consider screen density)
    return numValue;
  }
}

/**
 * Legacy text style options interface.
 *
 * @deprecated Use individual modifier methods instead.
 * @since 8
 */
interface TextStyleOptions {
  /**
   * Font size in fp.
   */
  fontSize?: number;

  /**
   * Font color as hex string.
   */
  fontColor?: string;

  /**
   * Font weight.
   */
  fontWeight?: string | FontWeight;
}

/**
 * Legacy button style interface.
 *
 * @deprecated Use individual modifier methods instead.
 * @since 8
 */
interface LegacyButtonStyle {
  /**
   * Width in px.
   */
  width?: number;

  /**
   * Height in px.
   */
  height?: number;

  /**
   * Background color as hex string.
   */
  backgroundColor?: string;

  /**
   * Font size in fp.
   */
  fontSize?: number;
}

/**
 * Font weight enumeration.
 *
 * @since 10
 * @enum {number}
 */
enum FontWeight {
  Lighter = 100,
  Light = 300,
  Normal = 400,
  Medium = 500,
  Bold = 700,
  Bolder = 900
}

/**
 * Color interface.
 *
 * @since 8
 */
interface Color {
  red: number;
  green: number;
  blue: number;
  alpha: number;
}

// Export
export { ButtonAttribute, TextStyleOptions, LegacyButtonStyle, FontWeight, Color };

/**
 * ============================================
 * DEPRECATION CHECKLIST
 * ============================================
 *
 * When deprecating an API, ensure:
 *
 * ✅ Add @deprecated tag with clear explanation
 * ✅ Add @deprecated_since tag
 * ✅ Provide alternative API name
 * ✅ Include migration guide in @example
 * ✅ Explain why the API is deprecated
 * ✅ Keep old API functional (backward compatibility)
 * ✅ Old API internally calls new API
 * ✅ Document conversion rules (if applicable)
 *
 * ============================================
 * MIGRATION GUIDE TEMPLATE
 * ============================================
 *
 * @deprecated Use [newMethod]() instead.
 *             [Reason for deprecation and benefits of new API].
 * @deprecated_since [version]
 * @since [original version]
 * @example
 * // Migration guide:
 * // Before: [old usage example]
 * // After: [new usage example]
 *
 * // Note: [Any important notes about the migration]
 */
