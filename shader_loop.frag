uniform float texture_width;
uniform float texture_height;
uniform float time;

void main() {
    vec2 resolution = vec2( texture_height, texture_width );
    vec2 uv = -1. + 2. * gl_FragCoord.xy / resolution.xy;
    gl_FragColor = vec4(
        abs( sin( cos( time + 3. * uv.y ) * 2. * uv.x + time)),
        abs( cos( sin( time + 2. * uv.x ) * 3. * uv.y + time)),
        1.0,
        1.0);
}
