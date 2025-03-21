VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vViewDir;

float fresnel = 1.0;

void MAIN(){
	BASE_COLOR = baseColor;
	SPECULAR_AMOUNT = 0.0;
	ROUGHNESS = 0.01;
	METALNESS = 0.0;
	fresnel = abs(dot(normalize(vViewDir),normalize(VAR_WORLD_NORMAL)));
}

void DIRECTIONAL_LIGHT()
{
    DIFFUSE += LIGHT_COLOR * SHADOW_CONTRIB * vec3(smoothstep(-1.0,1.0,abs( dot(normalize(VAR_WORLD_NORMAL), TO_LIGHT_DIR))));
}

void POST_PROCESS()
{
	vec4 df = texture(dfMask, vTexCoord);
	float dfMaskDot = dot(vColor.rgb,df.rgb);///length(vColor);
	float dfAdjust = smoothstep(0.0,1.0,dfMaskDot);	
	float a = dfAdjust*vColor.a;//min(max(0.0,centerDist*smoothstep(0.0,1.0,vColor.a)),1.0);
	a *= fresnel;
	if(a <= 0.0){discard;}
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	
	float depthSample = texture(DEPTH_TEXTURE, screenPos).x;
	
	vec3 fColor = vec3(1.0);// * vColor.rgb;
	
	float depthFade = smoothstep(0.0,0.025,abs(depthSample-gl_FragCoord.z));
	depthFade *= smoothstep(0.50,1.0,gl_FragCoord.z);
	a *= depthFade;
	a *= opacity;
	
	COLOR_SUM = vec4((baseColor.rgb * DIFFUSE.rgb + SPECULAR.rgb),a);
}