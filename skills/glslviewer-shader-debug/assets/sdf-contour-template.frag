#version 330 core

uniform vec2 u_resolution;

out vec4 fragColor;

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

float debugSdf(vec2 fragCoord)
{
    vec2 centerPos = u_resolution * 0.5;
    vec2 p = fragCoord - centerPos;

    // Replace this with the shader math you want to inspect.
    float radius = 40.0;
    return length(p) - radius;
}

void main()
{
    float sdf = debugSdf(gl_FragCoord.xy);
    fragColor = previewColor(sdf);
}
