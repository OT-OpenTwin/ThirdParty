VARYING vec2 vTexCoord;
VARYING vec4 vColor;

float fresnel = 1.0;

void MAIN(){
	BASE_COLOR = vec4(0.0);
	
	float fresnelBase = abs(dot(VAR_WORLD_NORMAL, VIEW_VECTOR));
	fresnel = smoothstep(0.0,1.0,fresnelBase);
	//fresnel *= smoothstep(1.0,.50,fresnelBase);
	fresnel *= vColor.a;
	
}

void POST_PROCESS()
{
	vec2 centerCoord = vTexCoord*2.0-1.0;
	float centerDist = smoothstep(1.0,0.0,length(centerCoord));
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	vec2 screenCoord = vec2(screenPos);
	
	float distortion = centerDist*0.5;
	
	float depthSample = texture(DEPTH_TEXTURE, screenCoord).x;
	
	//screenCoord.x = centerCoord.x > 0.0 ? mix(screenCoord.x, 0.0,centerCoord.x*distortion) : mix(screenCoord.x, 1.0,-centerCoord.x*distortion);
	
	//screenCoord.y = centerCoord.y > 0.0 ? mix(screenCoord.y, 0.0,centerCoord.y*distortion) : mix(screenCoord.y, 1.0,-centerCoord.y*distortion);
	
	//if (FRAMEBUFFER_Y_UP < 0.0) // effectively: if not OpenGL
        //screencoord.y = 1.0 - screencoord.y;
	
    vec4 sceneSample = texture(SCREEN_TEXTURE, screenCoord);
	
	//COLOR_SUM = vec4(vec3(vTexCoord,0.0)*centerDist,centerDist);
	
	vec3 fColor = sceneSample.rgb;// * vColor.rgb;
	float a = baseColor.a;
	
	float depthFade = smoothstep(0.0,0.05,abs(depthSample-gl_FragCoord.z));
	depthFade *= smoothstep(0.50,1.0,gl_FragCoord.z);
	a *= depthFade;
	
	a *= (fresnel);
	a *= opacity;
	
	COLOR_SUM = vec4((fColor+baseColor.rgb*a)*a*a*a,a);
	//baseColor;//mix(COLOR_SUM,refraction,1.0-vFresnel)*baseColor;
	//COLOR_SUM = vec4(a,a,a,1.0);
}