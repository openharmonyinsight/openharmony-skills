# Runtime Shader To GLSL

Use this note when the source shader comes from a runtime-effect string, SkSL-like snippet, or engine-specific fragment dialect.

## Common Rewrites

- Replace `half`, `half2`, `half3`, `half4` with `float`, `vec2`, `vec3`, `vec4`.
- Replace `float2`, `float3`, `float4` with `vec2`, `vec3`, `vec4`.
- Keep uniform names unless they conflict with `glslViewer` built-ins.
- Add:
```glsl
#version 330 core
uniform vec2 u_resolution;
out vec4 fragColor;
```

## Entry Point Rewrite

If the source uses:

```glsl
half4 main(vec2 fragCoord)
```

rewrite it as:

```glsl
void main()
{
    vec2 fragCoord = gl_FragCoord.xy;
    fragColor = ...;
}
```

If the source uses `main(float2 fragCoord)`, treat it the same way.

## Coordinate Conventions

- `gl_FragCoord.xy` is the easiest replacement for incoming fragment coordinates.
- If the original shader expects center-relative coordinates, compute them explicitly:
```glsl
vec2 centerPos = u_resolution * 0.5;
vec2 local = gl_FragCoord.xy - centerPos;
```

## Debug Output Patterns

### Contour preview for SDFs

Use a helper like this:

```glsl
vec4 previewColor(float sdf)
{
    float aa = max(fwidth(sdf) * 1.5, 1e-4);
    float fill = 1.0 - smoothstep(-aa, aa, sdf);
    float edge = 1.0 - smoothstep(0.0, aa * 2.0, abs(sdf));
    vec3 bg = vec3(0.97);
    vec3 inside = vec3(0.10, 0.16, 0.22);
    vec3 contour = vec3(0.90, 0.22, 0.18);
    vec3 color = mix(bg, inside, fill);
    color = mix(color, contour, edge);
    return vec4(color, 1.0);
}
```

This makes the zero crossing obvious and avoids mistaking a full rectangular texture for a rectangular contour.

### Raw channel preview

If a downstream stage consumes raw SDF or packed channels, write them out directly for inspection:

```glsl
fragColor = vec4(vec3(sdf * 0.02 + 0.5), 1.0);
```

or

```glsl
fragColor = vec4(normalize(vec3(grad, 1.0)) * 0.5 + 0.5, 1.0);
```

## Failure Modes

- If the preview is correct but device output is wrong, check uniform binding and downstream interpretation.
- If the preview is boxy, verify the translated radius math before suspecting the renderer.
- If `glslViewer` renders black or empty frames, simplify the shader until a minimal output works, then add logic back incrementally.
