VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vNormal;

void MAIN()
{
	vTexCoord = UV0;
	vColor = COLOR;
	vNormal = NORMAL.xyz;
}