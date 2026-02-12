/**
 * Static and Dynamic API Synchronization Example
 *
 * This file demonstrates how to properly synchronize Static API (.static.d.ets)
 * and Dynamic API (*Modifier.d.ts) when adding new component properties.
 *
 * File Location Reference:
 * - Static API: OpenHarmony/interface/sdk-js/api/arkui/component/<component>.static.d.ets
 * - Dynamic API: OpenHarmony/interface/sdk-js/api/arkui/<Component>Modifier.d.ts
 */

// ============================================
// EXAMPLE 1: Adding a New Property
// ============================================

// Scenario: Adding "iconSize" property to Button component

// ===== Static API: button.static.d.ets =====
/**
 * Location: OpenHarmony/interface/sdk-js/api/arkui/component/button.static.d.ets
 *
 * Purpose: Declarative UI API for ArkTS static type system
 * Usage: Button({ label: 'Click', iconSize: 32 })
 */
declare class Button_StaticAPI_Example {
  /**
   * Button label text.
   *
   * @type { string | Resource }
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 static
   * @stagemodelonly
   */
  label: string | Resource;

  /**
   * Icon size.
   * This is the NEW property we're adding.
   *
   * @type { number | string }
   * @unit vp
   * @default 24vp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 12 static
   * @stagemodelonly
   */
  iconSize: number | string;

  /**
   * Creates a button component.
   *
   * @param label - Button label text.
   * @param options - Button options.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 static
   * @stagemodelonly
   */
  constructor(label: string | Resource, options?: {
    type?: ButtonType;
    stateEffect?: boolean;
    iconSize?: number | string; // NEW property
  });
}

// ===== Dynamic API: ButtonModifier.d.ts =====
/**
 * Location: OpenHarmony/interface/sdk-js/api/arkui/ButtonModifier.d.ts
 *
 * Purpose: Imperative modifier API for command-style property setting
 * Usage: Button({ label: 'Click' }).iconSize(32)
 */
declare interface ButtonAttribute_DynamicAPI_Example extends CommonMethod<ButtonAttribute> {
  /**
   * Sets the button label.
   *
   * @param value - Label text to display.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   * @stagemodelonly
   */
  label(value: string | Resource): ButtonAttribute;

  /**
   * Sets the icon size.
   * This is the NEW method we're adding to match the static API.
   *
   * @param value - Icon size in vp. Valid range: 0-100vp.
   *              If undefined, restores to default size (24vp).
   *              If null, removes icon size setting.
   * @unit vp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 12 dynamic
   * @stagemodelonly
   */
  iconSize(value: number | string | Length | undefined | null): ButtonAttribute;
}

// ============================================
// EXAMPLE 2: Synchronization Checklist
// ============================================

/**
 * When adding a new property, ensure both APIs are synchronized:
 *
 * ✅ CHECKLIST:
 *
 * [ ] Static API (button.static.d.ets)
 *     [ ] Property added to class/interface
 *     [ ] Type matches dynamic API
 *     [ ] JSDOC includes @since X static
 *     [ ] JSDOC includes @stagemodelonly
 *     [ ] Default value documented
 *     [ ] Unit specified (if applicable)
 *
 * [ ] Dynamic API (ButtonModifier.d.ts)
 *     [ ] Method added to Modifier interface
 *     [ ] Signature matches static API
 *     [ ] Return type is correct (Modifier attribute)
 *     [ ] JSDOC includes @since X dynamic
 *     [ ] JSDOC includes @stagemodelonly
 *     [ ] undefined/null behavior documented
 *
 * [ ] Type Consistency
 *     [ ] Parameter types match
 *     [ ] Return type is correct
 *     [ ] Optional flags match
 *     [ ] Resource support included (if theme-able)
 *
 * [ ] Documentation
 *     [ ] @since tags consistent (with static/dynamic suffix)
 *     [ ] @syscap tags present
 *     [ ] @stagemodelonly tags present
 *     [ ] Examples work for both APIs
 */

// ============================================
// EXAMPLE 3: Type Consistency Rules
// ============================================

/**
 * RULE 1: Property types must match exactly
 *
 * Static: iconSize: number | string
 * Dynamic: iconSize(value: number | string | Length | undefined | null)
 *
 * ✅ OK: Static uses subset of Dynamic types
 * ❌ BAD: Static has 'boolean' but Dynamic doesn't
 */

/**
 * RULE 2: Optional parameters in Dynamic API
 *
 * Static API: property can be optional (iconSize?: number)
 * Dynamic API: method should accept undefined/null
 *
 * ✅ OK: iconSize(value: number | string | Length | undefined | null)
 * ❌ BAD: iconSize(value: number, value: string) - Overloads not recommended
 */

/**
 * RULE 3: Resource type support
 *
 * For theme-able properties (color, size, string):
 *
 * ✅ OK: Include Resource type
 *   - Static: iconSize: number | string | Resource
 *   - Dynamic: iconSize(value: number | string | Length | Resource | undefined | null)
 *
 * ✅ BETTER: Use ResourceStr to simplify when both string and Resource are supported
 *   - Static: iconSize: number | ResourceStr
 *   - Dynamic: iconSize(value: number | Length | ResourceStr | undefined | null)
 *   Benefit: ResourceStr already includes string, simpler type definition
 *
 * ❌ AVOID: Only number/string for theme-able properties
 *   - Static: iconSize: number | string
 *   - Dynamic: iconSize(value: number | string)
 */

/**
 * RULE 4: JSDOC tag format
 *
 * Static API: @since [version] static
 * Dynamic API: @since [version] dynamic
 *
 * ✅ CORRECT:
 *   - Static: @since 12 static
 *   - Dynamic: @since 12 dynamic
 *
 * ❌ WRONG:
 *   - @since 12 (missing static/dynamic indicator)
 *   - @since 12\n @static (separate lines)
 */

// ============================================
// EXAMPLE 4: API Deprecation Pattern
// ============================================

// Scenario: Deprecating old method name

// ===== Static API: text.static.d.ets =====
declare class Text_Deprecation_Example {
  /**
   * Font size.
   *
   * @type { number | string | Resource }
   * @unit fp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 10 static
   * @stagemodelonly
   */
  fontSize: number | string | Resource;

  /**
   * Sets the font size (OLD METHOD).
   *
   * @param value - Font size value.
   * @deprecated since API 10. Use fontSize property instead.
   * @see fontSize
   * @migration Text({ content: 'Hello', fontSize: 16 })
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 static
   * @obsoleted 10
   * @stagemodelonly
   */
  setFontSize(value: number | string | Resource): void;
}

// ===== Dynamic API: TextModifier.d.ts =====
declare interface TextAttribute_Deprecation_Example extends CommonMethod<TextAttribute> {
  /**
   * Sets the font size (NEW METHOD).
   *
   * @param value - Font size in fp. Valid range: 0-1000fp.
   * @unit fp
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 10 dynamic
   * @stagemodelonly
   */
  fontSize(value: number | string | Length | Resource | undefined | null): TextAttribute;

  /**
   * Sets the font size (OLD METHOD - deprecated).
   *
   * @param value - Font size value.
   * @deprecated since API 10. Use fontSize() instead.
   * @see fontSize
   * @migration Text().fontSize(16)
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since 7 dynamic
   * @obsoleted 10
   * @stagemodelonly
   */
  setFontSize(value: number | string | Resource): TextAttribute;
}

/**
 * DEPRECATION CHECKLIST:
 *
 * [ ] Mark BOTH static and dynamic APIs as @deprecated (同步废弃)
 * [ ] Provide @see reference to new API
 * [ ] Add @migration example in JSDOC
 * [ ] Specify @obsoleted version
 * [ ] Keep old implementation for backward compatibility
 * [ ] Update documentation and examples
 * [ ] Ensure @stagemodelonly tag is present
 * [ ] Verify @since X static/dynamic format
 * [ ] Both APIs have matching deprecation tags
 */

// ============================================
// EXAMPLE 5: Common Pitfalls to Avoid
// ============================================

/**
 * ❌ PITFALL 1: Only updating one API
 *
 * Problem:
 * - Static API has the new property
 * - Dynamic API is missing the method
 *
 * Result:
 * - Declarative: Text({ content: 'Hello', newProp: 123 }) // Works
 * - Imperative: Text().newProp(123) // Error: method doesn't exist
 *
 * Solution: ALWAYS update both static and dynamic APIs
 */

/**
 * ❌ PITFALL 2: Type mismatch
 *
 * Problem:
 * - Static API: iconSize: number | string
 * - Dynamic API: iconSize(value: number | Resource) // Missing string!
 *
 * Result:
 * - Type inconsistency leads to compilation errors
 *
 * Solution: Ensure types match between both APIs
 */

/**
 * ❌ PITFALL 3: Missing undefined/null handling in Dynamic API
 *
 * Problem:
 * - Static API: iconSize?: number // Optional
 * - Dynamic API: iconSize(value: number) // No undefined/null
 *
 * Result:
 * - Cannot remove property after setting it
 * - Inconsistent behavior between static and dynamic
 *
 * Solution: Dynamic API should accept undefined | null for optional properties
 */

/**
 * ❌ PITFALL 4: Incorrect JSDOC tag format
 *
 * Problem:
 * - @since 12 (missing static/dynamic indicator)
 * - @since 12\n @static (wrong format)
 *
 * Result:
 * - Incomplete documentation
 * - Automated tools cannot parse API type
 *
 * Solution: Use correct format
 *   - Static: @since 12 static
 *   - Dynamic: @since 12 dynamic
 */

/**
 * ❌ PITFALL 5: Missing @stagemodelonly tag
 *
 * Problem:
 * - JSDOC doesn't include @stagemodelonly tag
 *
 * Result:
 * - API documentation is incomplete
 * - Cannot distinguish stage model APIs
 *
 * Solution: Always add @stagemodelonly tag to both static and dynamic APIs
 */

// ============================================
// EXAMPLE 6: Complete Property Addition Template
// ============================================

/**
 * TEMPLATE: Adding a new property to a component
 *
 * Step 1: Update Static API (component/*.static.d.ets)
 * Step 2: Update Dynamic API (*Modifier.d.ts)
 * Step 3: Build SDK to verify
 * Step 4: Check generated output
 */

// ===== Step 1: Static API Template =====
// File: component/[YourComponent].static.d.ets
/*
declare class YourComponent {
  // ... existing properties ...

  /**
   * [Brief property description].
   *
   * @type { [Type] }
   * @unit [unit if applicable]
   * @default [default value]
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since [API version] static
   * @stagemodelonly
   */
  yourNewProperty: [Type];

  /**
   * Creates a [Component] component.
   *
   * @param [param] - [Description].
   * @param options - [Component] options.
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since [API version] static
   * @stagemodelonly
   */
  constructor([param]: [ParamType], options?: {
    // ... existing options ...
    yourNewProperty?: [Type]; // Add to constructor options
  });
}
*/

// ===== Step 2: Dynamic API Template =====
// File: api/arkui/[YourComponent]Modifier.d.ts
/*
declare interface YourComponentAttribute extends CommonMethod<YourComponentAttribute> {
  // ... existing methods ...

  /**
   * [Brief method description].
   *
   * @param value - [Description]. Valid range: [min]-[max][unit].
   *              If undefined, [restores/removes] [description].
   *              If null, [removes behavior].
   * @unit [unit if applicable]
   * @syscap SystemCapability.ArkUI.ArkUI.Full
   * @since [API version] dynamic
   * @stagemodelonly
   */
  yourNewProperty(value: [Type] | undefined | null): YourComponentAttribute;
}
*/

// ===== Step 3: Build SDK =====
// Command from OpenHarmony root:
/*
./build.sh --export-para PYCACHE_ENABLE:true --product-name ohos-sdk --ccache
*/

// ===== Step 4: Verify Output =====
/*
# Check Static API
grep -n "yourNewProperty" out/ohos-sdk/interfaces/sdk-js/api/arkui/component/[yourcomponent].static.d.ets

# Check Dynamic API
grep -n "yourNewProperty" out/ohos-sdk/interfaces/sdk-js/api/arkui/[YourComponent]Modifier.d.ts

# Verify JSDOC tags are correct
grep "@since.*static\|@since.*dynamic" out/ohos-sdk/interfaces/sdk-js/api/arkui/
grep "@stagemodelonly" out/ohos-sdk/interfaces/sdk-js/api/arkui/

# Verify no compilation errors
# Check build.log for errors
*/

// ============================================
// END OF EXAMPLE
// ============================================

/**
 * SUMMARY:
 *
 * When adding or modifying ArkUI component APIs:
 *
 * 1. ALWAYS update both Static (.static.d.ets) and Dynamic (*Modifier.d.ts) APIs
 * 2. Ensure type signatures match between both APIs
 * 3. Include complete JSDOC with proper tag format:
 *    - @since [version] static (for Static API)
 *    - @since [version] dynamic (for Dynamic API)
 *    - @stagemodelonly (for all APIs)
 * 4. Support Resource type for theme-able properties
 * 5. Build SDK to verify compilation
 * 6. Check generated output to confirm changes and tags
 *
 * File Locations:
 * - Static API: OpenHarmony/interface/sdk-js/api/arkui/component/*.static.d.ets
 * - Dynamic API: OpenHarmony/interface/sdk-js/api/arkui/*Modifier.d.ts
 * - Build Output: out/ohos-sdk/interfaces/sdk-js/api/arkui/
 */
