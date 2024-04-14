VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vNormal;
VARYING vec3 vViewVec;
VARYING float vFresnel;
float fFresnel;

vec3 fNormal = vec3(0.0);


void MAIN(){
	BASE_COLOR = vec4(0.0);
	fNormal = normalize(VAR_WORLD_NORMAL);
	fFresnel = dot(fNormal, normalize(vViewVec));
}

void POST_PROCESS()
{
	vec2 centerCoord = vTexCoord*2.0-1.0;
	float centerDist = smoothstep(1.0,0.0,length(centerCoord));
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	vec2 screenCoord = vec2(screenPos);
	
	float ripple = (sin(fNormal.y*5.0));
	
	float fd = smoothstep(0.0,1.0,fFresnel)*ripple;
	float distortion = .05*fd;
	
	float depthSample = texture(DEPTH_TEXTURE, screenCoord).x;
	
	screenCoord.x = centerCoord.x > 0.0 ? mix(screenCoord.x, 0.0,centerCoord.x*distortion) : mix(screenCoord.x, 1.0,-centerCoord.x*distortion);
	
	screenCoord.y = centerCoord.y > 0.0 ? mix(screenCoord.y, 0.0,centerCoord.y*distortion) : mix(screenCoord.y, 1.0,-centerCoord.y*distortion);
	
	//if (FRAMEBUFFER_Y_UP < 0.0) // effectively: if not OpenGL
        //screencoord.y = 1.0 - screencoord.y;
	
    vec4 sceneSample = texture(SCREEN_TEXTURE, screenCoord);
	
	//COLOR_SUM = vec4(vec3(vTexCoord,0.0)*centerDist,centerDist);
	
	vec3 fColor = sceneSample.rgb;// * vColor.rgb;
	float a = min(max(0.0,centerDist*smoothstep(0.0,1.0,vColor.a)),1.0);
	
	float depthFade = smoothstep(0.0,0.01,abs(depthSample-gl_FragCoord.z));//depthSample;//smoothstep(0.0,.10,abs(depthSample - (gl_FragCoord.z/gl_FragCoord.w)));
	float fa = smoothstep(0.50,1.0,fFresnel);
	a *= depthFade * fa;
	a *= opacity;
	COLOR_SUM = vec4(fColor*baseColor.rgb,a);
	//baseColor;//mix(COLOR_SUM,refraction,1.0-vFresnel)*baseColor;
	//COLOR_SUM = vec4(f,f,f,1.0);
}