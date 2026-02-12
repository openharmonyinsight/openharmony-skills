/**
 * Example: Complete Modifier Implementation for ArkUI Component
 *
 * This example demonstrates how to properly implement modifier methods
 * for ArkUI components following OpenHarmony coding standards.
 */

import { Resource } from '@kit.ArkUI';

// Type definitions
type ResourceColor = string | Resource | Color;
type ResourceStr = string | Resource;
type Length = string | number;
type PaddingValue =
  | Length
  | [Length]
  | [Length, Length]
  | [Length, Length, Length, Length];

/**
 * Button attribute class.
 * Provides modifier methods for button component styling.
 *
 * @since 8
 */
class ButtonAttribute {
  // Private properties with default values
  private width_: Length = 'auto';
  private height_: Length = 40;
  private type_: ButtonType = ButtonType.Normal;
  private backgroundColor_: ResourceColor = '#007DFF';
  private fontSize_: number = 16;
  private fontColor_: ResourceColor = '#FFFFFF';
  private enabled_: boolean = true;
  private borderRadius_: number = 0;
  private icon_: ResourceStr | undefined = undefined;
  private iconSize_: number = 24;
  private opacity_: number = 1.0;
  private padding_: PaddingValue = [8, 16];

  // Constants
  private static readonly DEFAULT_WIDTH = 200;
  private static readonly DEFAULT_HEIGHT = 40;
  private static readonly DEFAULT_FONT_SIZE = 16;
  private static readonly DEFAULT_ICON_SIZE = 24;
  private static readonly DEFAULT_OPACITY = 1.0;
  private static readonly MAX_BORDER_RADIUS = 1000;
  private static readonly MAX_FONT_SIZE = 1000;
  private static readonly MIN_FONT_SIZE = 0;

  /**
   * Sets the button width.
   *
   * @param value Width value in vp or percentage.
   *              Valid range: 0-10000vp or '0%'-'100%'.
   *              If undefined, restores default width (200vp).
   *              Accepts number (vp), string with unit ('100vp', '50%'),
   *              Length object, or resource reference.
   * @unit vp
   * @throws {RangeError} If value is negative after parsing.
   * @throws {TypeError} If value type is invalid.
   * @since 8
   * @example
   * // Direct value in vp
   * Button().width(100)
   *
   * // With percentage
   * Button().width('50%')
   *
   * // With resource reference
   * Button().width($r('app.float.button_width'))
   */
  width(value: number | string | Length | Resource | undefined): ButtonAttribute {
    if (value === undefined) {
      this.width_ = ButtonAttribute.DEFAULT_WIDTH;
      return this;
    }

    const numValue = this.parseLengthToNumber(value);
    if (numValue !== null && numValue < 0) {
      throw new RangeError(`Width must be non-negative, got ${numValue}`);
    }

    this.width_ = value;
    return this;
  }

  /**
   * Sets the button height.
   *
   * @param value Height value in vp.
   *              Valid range: 0-10000vp.
   *              If undefined, restores default height (40vp).
   * @unit vp
   * @throws {RangeError} If value is negative.
   * @since 8
   * @example
   * Button().height(50)
   * Button().height('60vp')
   */
  height(value: number | string | Length | Resource | undefined): ButtonAttribute {
    if (value === undefined) {
      this.height_ = ButtonAttribute.DEFAULT_HEIGHT;
      return this;
    }

    const numValue = this.parseLengthToNumber(value);
    if (numValue !== null && numValue < 0) {
      throw new RangeError(`Height must be non-negative, got ${numValue}`);
    }

    this.height_ = value;
    return this;
  }

  /**
   * Sets the button type.
   *
   * @param value Button type defining shape and appearance.
   *              If undefined, restores default (ButtonType.Normal).
   * @since 8
   * @example
   * Button().type(ButtonType.Capsule)
   * Button().type(ButtonType.Circle)
   */
  type(value: ButtonType | undefined): ButtonAttribute {
    this.type_ = value ?? ButtonType.Normal;

    // Update border radius based on type
    if (value === ButtonType.Capsule) {
      this.borderRadius_ = 20;
    } else if (value === ButtonType.Normal) {
      this.borderRadius_ = 0;
    }
    // For Circle, border radius is set dynamically based on height

    return this;
  }

  /**
   * Sets the background color.
   *
   * @param value Background color value or resource reference.
   *              Accepts hex color (#RRGGBB, #AARRGGBB),
   *              color name, or resource reference ($r('app.color.xxx')).
   *              If undefined, restores default color (#007DFF).
   * @since 8
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

  /**
   * Sets the font size of button text.
   *
   * @param value Font size in fp. Valid range: 0-1000fp.
   *              Values exceeding 1000fp will be clamped to 1000fp.
   *              Negative values are treated as 0.
   *              If undefined, restores default size (16fp).
   * @unit fp
   * @since 8
   * @example
   * Button().fontSize(18)
   * Button().fontSize($r('app.float.font_size_large'))
   */
  fontSize(value: number | string | Length | Resource | undefined): ButtonAttribute {
    if (value === undefined) {
      this.fontSize_ = ButtonAttribute.DEFAULT_FONT_SIZE;
      return this;
    }

    const numValue = this.parseLengthToNumber(value);
    if (numValue !== null) {
      // Clamp to valid range
      const clampedValue = Math.max(
        ButtonAttribute.MIN_FONT_SIZE,
        Math.min(ButtonAttribute.MAX_FONT_SIZE, numValue)
      );
      this.fontSize_ = clampedValue;
    } else {
      // Store string/Resource value as-is
      this.fontSize_ = value as number;
    }

    return this;
  }

  /**
   * Sets the font color of button text.
   *
   * @param value Font color value or resource reference.
   *              If undefined, restores default color (#FFFFFF).
   * @since 8
   * @example
   * Button().fontColor('#000000')
   * Button().fontColor($r('app.color.text_primary'))
   */
  fontColor(value: ResourceColor | undefined): ButtonAttribute {
    this.fontColor_ = value ?? '#FFFFFF';
    return this;
  }

  /**
   * Sets whether the button is enabled.
   *
   * @param value Enable state.
   *              - true: Button can interact with user (default)
   *              - false: Button is disabled and cannot interact
   *              If undefined, restores default (true).
   * @since 8
   * @example
   * Button().enabled(true)   // Enable button
   * Button().enabled(false)  // Disable button
   */
  enabled(value: boolean | undefined): ButtonAttribute {
    this.enabled_ = value ?? true;
    return this;
  }

  /**
   * Sets the border radius of the button.
   *
   * @param value Border radius value in vp.
   *              Valid range: 0-1000vp.
   *              Values exceeding 1000vp will be clamped to 1000vp.
   *              Negative values are treated as 0.
   *              If undefined, restores default based on button type.
   * @unit vp
   * @since 8
   * @example
   * Button().borderRadius(10)
   * Button().borderRadius($r('app.float.border_radius'))
   */
  borderRadius(value: number | string | Length | Resource | undefined): ButtonAttribute {
    if (value === undefined) {
      // Restore default based on type
      if (this.type_ === ButtonType.Capsule) {
        this.borderRadius_ = 20;
      } else {
        this.borderRadius_ = 0;
      }
      return this;
    }

    const numValue = this.parseLengthToNumber(value);
    if (numValue !== null) {
      // Clamp to valid range
      const clampedValue = Math.max(0, Math.min(ButtonAttribute.MAX_BORDER_RADIUS, numValue));
      this.borderRadius_ = clampedValue;
    } else {
      this.borderRadius_ = value as number;
    }

    return this;
  }

  /**
   * Sets the icon to display on the button.
   *
   * @param value Icon resource or string.
   *              If undefined, removes icon.
   * @since 8
   * @example
   * // Direct string
   * Button().icon('search')
   *
   * // Resource reference
   * Button().icon($r('app.media.icon_search'))
   * Button().icon($r('sys.symbol.plus'))
   */
  icon(value: ResourceStr | undefined): ButtonAttribute {
    this.icon_ = value;
    return this;
  }

  /**
   * Sets the icon size.
   *
   * @param value Icon size in vp.
   *              Valid range: 0-1000vp.
   *              If undefined, restores default size (24vp).
   * @unit vp
   * @since 8
   * @example
   * Button().iconSize(30)
   * Button().iconSize($r('app.float.icon_size_large'))
   */
  iconSize(value: number | string | Length | Resource | undefined): ButtonAttribute {
    if (value === undefined) {
      this.iconSize_ = ButtonAttribute.DEFAULT_ICON_SIZE;
      return this;
    }

    const numValue = this.parseLengthToNumber(value);
    if (numValue !== null) {
      this.iconSize_ = Math.max(0, Math.min(1000, numValue));
    } else {
      this.iconSize_ = value as number;
    }

    return this;
  }

  /**
   * Sets the opacity of the button.
   *
   * @param value Opacity value. Valid range: 0-1.
   *              0 = fully transparent, 1 = fully opaque.
   *              If undefined, restores default opacity (1.0).
   *              If null, removes opacity setting and uses inherited value.
   *              Values < 0 are treated as 0.
   *              Values > 1 are treated as 1.
   * @since 9
   * @example
   * Button().opacity(0.5)  // 50% transparent
   * Button().opacity(0)    // Fully transparent
   * Button().opacity(1)    // Fully opaque
   */
  opacity(value: number | string | undefined | null): ButtonAttribute {
    if (value === undefined) {
      this.opacity_ = ButtonAttribute.DEFAULT_OPACITY;
    } else if (value !== null) {
      const numValue = typeof value === 'number' ? value : this.parseLengthToNumber(value) ?? 1;
      // Clamp to valid range
      this.opacity_ = Math.max(0, Math.min(1, numValue));
    }
    // If null, keep current value (remove setting)

    return this;
  }

  /**
   * Sets the padding of the button.
   *
   * @param value Padding value in vp.
   *              Can be:
   *              - Single value: all sides
   *              - Two values: [vertical, horizontal]
   *              - Four values: [top, right, bottom, left]
   *              If undefined, removes padding (sets to 0).
   * @unit vp
   * @since 8
   * @example
   * // All sides
   * Button().padding(10)
   *
   * // Vertical and horizontal
   * Button().padding([10, 20])
   *
   * // Individual sides
   * Button().padding([10, 20, 10, 20])
   */
  padding(value: PaddingValue | undefined): ButtonAttribute {
    if (value === undefined) {
      this.padding_ = 0;
    } else {
      this.padding_ = value;
    }
    return this;
  }

  /**
   * Registers a callback for click events.
   *
   * @param action Callback invoked when button is clicked.
   *               Receives ClickEvent with click details.
   *               If undefined, removes the callback.
   * @since 8
   * @example
   * Button().onClick((event: ClickEvent) => {
   *   console.log('Button clicked at:', event.x, event.y)
   * })
   */
  onClick(action: ((event: ClickEvent) => void) | undefined): ButtonAttribute {
    if (action !== undefined) {
      // Register click callback
      this.registerClickCallback(action);
    } else {
      // Remove callback
      this.unregisterClickCallback();
    }
    return this;
  }

  // Private helper methods

  /**
   * Parses length value to number.
   * Returns null if value cannot be parsed to a number.
   *
   * @param value Length value to parse.
   * @returns Parsed number or null.
   */
  private parseLengthToNumber(value: number | string | Length | Resource): number | null {
    if (typeof value === 'number') {
      return value;
    }

    if (typeof value === 'string') {
      // Parse string like "100vp", "50%", etc.
      const match = value.match(/^([\d.]+)(vp|px|fp|%)?$/);
      if (match) {
        return parseFloat(match[1]);
      }
    }

    // Resource or complex Length object - return null
    return null;
  }

  /**
   * Registers click callback.
   *
   * @param callback Callback function.
   */
  private registerClickCallback(callback: (event: ClickEvent) => void): void {
    // Implementation details...
  }

  /**
   * Unregisters click callback.
   */
  private unregisterClickCallback(): void {
    // Implementation details...
  }
}

/**
 * Button type enumeration.
 *
 * @since 8
 * @enum {string}
 */
enum ButtonType {
  /**
   * Normal button with rectangular shape.
   */
  Normal = 'normal',

  /**
   * Capsule-shaped button with rounded corners.
   */
  Capsule = 'capsule',

  /**
   * Circular button (width and height must be equal).
   */
  Circle = 'circle'
}

/**
 * Click event data structure.
 *
 * @since 8
 */
interface ClickEvent {
  /**
   * X coordinate of the click position in px.
   */
  x: number;

  /**
   * Y coordinate of the click position in px.
   */
  y: number;

  /**
   * Timestamp of the click event.
   */
  timestamp: number;
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

// Export for use
export { ButtonAttribute, ButtonType, ClickEvent, Color };
