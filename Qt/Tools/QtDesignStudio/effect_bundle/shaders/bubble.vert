VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vViewNormal;
VARYING vec3 vNormal;

void MAIN()
{
	vTexCoord = UV0;
	vColor = COLOR;
	vViewNormal = normalize((VIEW_MATRIX * vec4(NORMAL, 0.0)).xyz);
	vNormal = normalize(NORMAL_MATRIX * NORMAL);
}