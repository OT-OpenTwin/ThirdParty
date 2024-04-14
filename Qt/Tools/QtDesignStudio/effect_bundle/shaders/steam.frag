VARYING vec2 vTexCoord;
VARYING vec4 vColor;
VARYING vec3 vNormal;

float fresnel = 1.0;

void MAIN(){
	BASE_COLOR = baseColor;
	SPECULAR_AMOUNT = 0.0;
	ROUGHNESS = 0.0;
	METALNESS = 0.0;
	
	fresnel = smoothstep(0.0,1.0,abs(dot(VIEW_VECTOR,VAR_WORLD_NORMAL)));
}

void POST_PROCESS()
{
	vec2 centerCoord = vTexCoord*2.0-1.0;
	float centerDist = smoothstep(1.0,0.0,length(centerCoord));
	
	vec2 screenPos = gl_FragCoord.xy/textureSize(SCREEN_TEXTURE, 0);
	vec2 screenCoord = (screenPos);
	
	float distortion = 1.*centerDist;
	
	//screenCoord.x = centerCoord.x > 0.0 ? mix(screenCoord.x, 0.0,centerCoord.x*distortion) : mix(screenCoord.x, 1.0,-centerCoord.x*distortion);
	
	//screenCoord.y = centerCoord.y > 0.0 ? mix(screenCoord.y, 0.0,centerCoord.y*distortion) : mix(screenCoord.y, 1.0,-centerCoord.y*distortion);
	
	//if (FRAMEBUFFER_Y_UP < 0.0) // effectively: if not OpenGL
        //screencoord.y = 1.0 - screencoord.y;
	
	float depthSample = texture(DEPTH_TEXTURE, screenCoord).x;
    vec4 sceneSample = texture(SCREEN_TEXTURE, screenCoord);
	
	//COLOR_SUM = vec4(vec3(vTexCoord,0.0)*centerDist,centerDist);
	
	vec3 fNormal = normalize(vNormal);
	vec3 normalCoord = fNormal*0.5+0.5;
	
	vec3 df = vec3(0.0);
	df.x = texture(dfMask, normalCoord.yz).x;	
	df.y = texture(dfMask, normalCoord.xz).y;	
	df.z = texture(dfMask, normalCoord.yx).z;	
	
	float dfDot = dot(abs(fNormal), df);//*dot(abs(fNormal),vColor.rgb);
	// df = texture(dfMask, vTexCoord);	
	
	
	//vec3 fColor = ;//df.rgb;// * vColor.rgb;
	float a = vColor.a*dfDot;//1.0;//min(max(0.0,centerDist*smoothstep(0.0,1.0,vColor.a)),1.0);
	a *= mix(smoothstep(0.50,1.0,dfDot*fresnel),1.0,pow(fresnel,3.0));
	
	float depthFade = smoothstep(0.0,0.0025,abs(depthSample-gl_FragCoord.z));//depthSample;//smoothstep(0.0,.10,abs(depthSample - (gl_FragCoord.z/gl_FragCoord.w)));
	depthFade *= smoothstep(0.50,1.0,gl_FragCoord.z);
	a *= depthFade;
	a *= opacity;
	COLOR_SUM = vec4((DIFFUSE.rgb + SPECULAR.rgb)*mix(0.50,1.0,a),a);
	//COLOR_SUM = vec4(depthFade);
	//baseColor;//mix(COLOR_SUM,refraction,1.0-vFresnel)*baseColor;
	//COLOR_SUM = vec4(vDepth,vDepth,vDepth,1.0);
}