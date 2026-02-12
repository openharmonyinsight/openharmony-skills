/**
 * Example: Complete Interface Definition for ArkUI Component
 *
 * This example demonstrates how to properly define interfaces for ArkUI components
 * following OpenHarmony coding standards and API design guidelines.
 *
 * NOTE: This is an INTERNAL interface definition example.
 * When creating actual SDK APIs, you must define both:
 * - Static API (*.static.d.ets) with @since X static tags
 * - Dynamic API (*Modifier.d.ts) with @since X dynamic tags
 *
 * All API definitions should include @stagemodelonly tag.
 */

import { Resource } from '@kit.ArkUI';

/**
 * Button component style interface.
 * Defines all configurable properties for button appearance and behavior.
 *
 * @since 8 static
 * @stagemodelonly
 * @systemapi
 */
interface ButtonStyle {
  /**
   * Button width in vp or percentage.
   * Valid range: 0-10000vp or '0%'-'100%'.
   * Default: 'auto' (content-based width).
   *
   * @unit vp
   * @since 8
   */
  width?: Length;

  /**
   * Button height in vp.
   * Valid range: 0-10000vp.
   * Default: 40vp.
   *
   * @unit vp
   * @since 8
   */
  height?: Length;

  /**
   * Button type defining shape and appearance.
   * Default: ButtonType.Normal.
   *
   * @since 8
   */
  type?: ButtonType;

  /**
   * Background color of the button.
   * Supports hex color, color name, or resource reference.
   * Default: System primary color.
   *
   * @since 8
   */
  backgroundColor?: ResourceColor;

  /**
   * Font size of button text in fp.
   * Valid range: 0-1000fp.
   * Default: 16fp.
   *
   * @unit fp
   * @since 8
   */
  fontSize?: number;

  /**
   * Font color of button text.
   * Supports hex color, color name, or resource reference.
   * Default: White (#FFFFFF) for enabled state.
   *
   * @since 8
   */
  fontColor?: ResourceColor;

  /**
   * Button state: enabled or disabled.
   * Default: true (enabled).
   *
   * @since 8
   */
  enabled?: boolean;

  /**
   * Border radius in vp.
   * Valid range: 0-1000vp.
   * Default: Depends on button type:
   * - Normal: 0vp
   * - Capsule: 20vp
   * - Circle: 50% of height
   *
   * @unit vp
   * @since 8
   */
  borderRadius?: number;

  /**
   * Icon resource to display on button.
   * Optional: Button works without icon.
   *
   * @since 8
   */
  icon?: ResourceStr;

  /**
   * Icon size in vp.
   * Valid range: 0-1000vp.
   * Default: 24vp.
   *
   * @unit vp
   * @since 8
   */
  iconSize?: number;
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
   * X coordinate of the click position.
   * Unit: px.
   *
   * @unit px
   */
  x: number;

  /**
   * Y coordinate of the click position.
   * Unit: px.
   *
   * @unit px
   */
  y: number;

  /**
   * Timestamp of the click event.
   * Unit: milliseconds since epoch.
   */
  timestamp: number;
}

/**
 * Button state enumeration.
 *
 * @since 10
 * @enum {number}
 */
enum ButtonState {
  /**
   * Normal state (default).
   */
  Normal = 0,

  /**
   * Pressed state (button is being pressed).
   */
  Pressed = 1,

  /**
   * Disabled state (button cannot be interacted with).
   */
  Disabled = 2
}

/**
 * Advanced button options interface.
 *
 * @since 10
 */
interface ButtonOptions {
  /**
   * Text content of the button.
   * Supports direct string or resource reference for i18n.
   *
   * @since 8
   */
  text?: string | Resource;

  /**
   * Icon to display before the text.
   *
   * @since 8
   */
  icon?: ResourceStr;

  /**
   * Spacing between icon and text in vp.
   * Valid range: 0-100vp.
   * Default: 8vp.
   *
   * @unit vp
   * @since 8
   */
  space?: number;

  /**
   * Whether to show progress indicator.
   * Default: false.
   *
   * @since 10
   */
  showProgress?: boolean;

  /**
   * Progress value (0-100) when showProgress is true.
   * Valid range: 0-100.
   * Default: 0.
   *
   * @since 10
   */
  progress?: number;
}

/**
 * Type definitions for resource and color values.
 *
 * @since 8
 */
type ResourceColor = string | Resource | Color;
type ResourceStr = string | Resource;
type Length = string | number;

/**
 * Color interface.
 *
 * @since 8
 */
interface Color {
  /**
   * Red component (0-255).
   */
  red: number;

  /**
   * Green component (0-255).
   */
  green: number;

  /**
   * Blue component (0-255).
   */
  blue: number;

  /**
   * Alpha component (0-1).
   */
  alpha: number;
}

/**
 * Export complete button interface.
 */
export {
  ButtonStyle,
  ButtonType,
  ClickEvent,
  ButtonState,
  ButtonOptions,
  ResourceColor,
  ResourceStr,
  Length,
  Color
};
