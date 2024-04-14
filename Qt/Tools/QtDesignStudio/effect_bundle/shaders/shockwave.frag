VARYING vec2 vTexCoord;
VARYING vec4 vColor;

float fresnel = 1.0;
float diskmask = 1.0;
float streaks = 1.0;
vec3 fn = vec3(0.0);

void MAIN(){
	BASE_COLOR = vec4(0.0);
	
	fn = normalize(VAR_WORLD_NORMAL);
	
	float dmbase = length(fn.xz);
	diskmask = smoothstep(.0,.05,dmbase);
	diskmask *= smoothstep(.05,.025,dmbase);
	
	streaks = atan(fn.x,fn.z);
	streaks = sin(streaks*7.0)*0.5+0.5;
	streaks += sin(streaks*13.0)*0.5+0.5;
	streaks += sin(streaks*17.0)*0.5+0.5;
	streaks += sin(streaks*23.0)*0.5+0.5;
	streaks += sin(streaks*29.0)*0.5+0.5;
	streaks /= 5.0;
	streaks = smoothstep(.0,1.0,streaks);
	//streaks = 1.0-streaks;
	
	streaks *= diskmask;
	streaks += diskmask;
	
	float fresnelBase = abs(dot(fn, VIEW_VECTOR));
	fresnel = smoothstep(0.0,.50,fresnelBase);
	fresnel *= smoothstep(1.0,.50,fresnelBase);
	fresnel *= vColor.a;
	
}

void POST_PROCESS()
{
	vec2 centerCoord = vTexCoord*2.0-1.0;
	float centerDist = smoothstep(1.0,0.0,length(centerCoord));
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	vec2 screenCoord = vec2(screenPos);
	
	float distortion = diskmask*0.25;
	
	float depthSample = texture(DEPTH_TEXTURE, screenCoord).x;
	
	screenCoord.x = centerCoord.x > 0.0 ? mix(screenCoord.x, 0.0,centerCoord.x*distortion) : mix(screenCoord.x, 1.0,-centerCoord.x*distortion);
	
	screenCoord.y = centerCoord.y > 0.0 ? mix(screenCoord.y, 0.0,centerCoord.y*distortion) : mix(screenCoord.y, 1.0,-centerCoord.y*distortion);
	
	//if (FRAMEBUFFER_Y_UP < 0.0) // effectively: if not OpenGL
        //screencoord.y = 1.0 - screencoord.y;
	
    vec4 sceneSample = texture(SCREEN_TEXTURE, screenCoord);
	
	//COLOR_SUM = vec4(vec3(vTexCoord,0.0)*centerDist,centerDist);
	
	vec3 fColor = baseColor.rgb*sceneSample.rgb;// * vColor.rgb;
	
	float depthFade = smoothstep(0.0,0.05,abs(depthSample-gl_FragCoord.z));//depthSample;//smoothstep(0.0,.10,abs(depthSample - (gl_FragCoord.z/gl_FragCoord.w)));
	//a *= depthFade;
	
	float a = streaks * smoothstep(0.25,1.0,vColor.a);
	
	COLOR_SUM = vec4(fColor*2.0*a,a);
	//baseColor;//mix(COLOR_SUM,refraction,1.0-vFresnel)*baseColor;
	//COLOR_SUM = vec4(a,a,a,1.0);
}