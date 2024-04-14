VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vViewDir;
VARYING vec3 vViewNormal;

float fresnel = 1.0;

vec4 rainTex = vec4(1.0);

vec3 blend_rnm(vec3 n1, vec3 n2)
{
    vec3 t = n1.xyz*vec3( 2,  2, 2) + vec3(-1, -1,  0);
    vec3 u = n2.xyz*vec3(-2, -2, 2) + vec3( 1,  1, -1);
    vec3 r = t*dot(t, u) - u*t.z;
    return normalize(r);
}

void MAIN(){
	rainTex = texture(rainmap, UV0*1.0);
	fresnel = abs(dot(normalize(vViewDir),normalize(VAR_WORLD_NORMAL)));
	fresnel *= 1.0 - abs(VAR_WORLD_NORMAL.y);

	BASE_COLOR = baseColor;
	SPECULAR_AMOUNT = 1.0;
	ROUGHNESS = 0.250;
	METALNESS = 0.0;
	NORMAL = blend_rnm(normalize(VAR_WORLD_NORMAL) * 0.5 + 0.5,rainTex.xyz);
	rainTex.rgb = rainTex.rgb * 2.0-1.0;
}

void POST_PROCESS()
{
	
	float a = rainTex.a*vColor.a*fresnel;
	if(a <= 0.0){discard;}

	vec2 centerCoord = vTexCoord*2.0-1.0;
	float centerDist = smoothstep(1.0,0.0,length(rainTex.rg));
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	vec2 screenCoord = vec2(screenPos);
	
	float distortion = 1.*centerDist;
	
	screenCoord.x = centerCoord.x > 0.0 ? mix(screenCoord.x, 0.0,centerCoord.x*distortion) : mix(screenCoord.x, 1.0,-centerCoord.x*distortion);
	
	screenCoord.y = centerCoord.y > 0.0 ? mix(screenCoord.y, 0.0,centerCoord.y*distortion) : mix(screenCoord.y, 1.0,-centerCoord.y*distortion);
	
	//if (FRAMEBUFFER_Y_UP < 0.0) // effectively: if not OpenGL
        //screencoord.y = 1.0 - screencoord.y;
	
	float depthSample = texture(DEPTH_TEXTURE, screenCoord).x;
    vec4 sceneSample = texture(SCREEN_TEXTURE, screenCoord);
	
	//COLOR_SUM = vec4(vec3(vTexCoord,0.0)*centerDist,centerDist);
	
	vec3 fColor = sceneSample.rgb*(1.0 + centerDist);//  vColor.rgb;
	
	a *= opacity;
	
	COLOR_SUM = vec4((DIFFUSE.rgb+SPECULAR+fColor)*baseColor.rgb,a);
	//baseColor;//mix(COLOR_SUM,refraction,1.0-vFresnel)*baseColor;
	//COLOR_SUM = vec4(vDepth,vDepth,vDepth,1.0);
}