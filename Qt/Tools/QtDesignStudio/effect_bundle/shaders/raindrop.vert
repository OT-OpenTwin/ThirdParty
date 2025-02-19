VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vViewDir;
VARYING vec3 vViewNormal;

void MAIN()
{
	vTexCoord = UV0;
	vColor = COLOR;
	vViewDir = normalize(CAMERA_POSITION - (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz);
	vViewNormal = normalize((VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
}