/*=========================================================================

  Program:   Visualization Toolkit
  Module:    vtkRenderingOpenGL2ObjectFactory.cxx

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/

#include "vtkRenderingOpenGL2ObjectFactory.h"
#include "vtkVersion.h"

// Include all of the classes we want to create overrides for.
#include "vtkDummyGPUInfoList.h"
#include "vtkOpenGLActor.h"
#include "vtkOpenGLBillboardTextActor3D.h"
#include "vtkOpenGLCamera.h"
#include "vtkOpenGLLabeledContourMapper.h"
#include "vtkOpenGLHardwareSelector.h"
#include "vtkOpenGLImageMapper.h"
#include "vtkOpenGLImageSliceMapper.h"
#include "vtkOpenGLGlyph3DMapper.h"
#include "vtkOpenGLLight.h"
#include "vtkOpenGLPointGaussianMapper.h"
#include "vtkOpenGLPolyDataMapper.h"
#include "vtkOpenGLPolyDataMapper2D.h"
#include "vtkOpenGLProperty.h"
#include "vtkOpenGLShaderProperty.h"
#include "vtkOpenGLUniforms.h"
#include "vtkOpenGLRenderer.h"
#include "vtkOpenGLRenderTimerLog.h"
#include "vtkOpenGLSkybox.h"
#include "vtkOpenGLTextActor.h"
#include "vtkOpenGLTextActor3D.h"
#include "vtkOpenGLTextMapper.h"
#include "vtkOpenGLTexture.h"
#include "vtkWin32OpenGLRenderWindow.h"


vtkStandardNewMacro(vtkRenderingOpenGL2ObjectFactory);

// Now create the functions to create overrides with.
VTK_CREATE_CREATE_FUNCTION(vtkDummyGPUInfoList)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLActor)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLBillboardTextActor3D)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLCamera)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLLabeledContourMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLHardwareSelector)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLImageMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLImageSliceMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLGlyph3DMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLLight)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLPointGaussianMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLPolyDataMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLPolyDataMapper2D)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLProperty)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLShaderProperty)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLUniforms)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLRenderer)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLRenderTimerLog)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLSkybox)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLTextActor)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLTextActor3D)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLTextMapper)
VTK_CREATE_CREATE_FUNCTION(vtkOpenGLTexture)
VTK_CREATE_CREATE_FUNCTION(vtkWin32OpenGLRenderWindow)


vtkRenderingOpenGL2ObjectFactory::vtkRenderingOpenGL2ObjectFactory()
{
this->RegisterOverride("vtkGPUInfoList", "vtkDummyGPUInfoList", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkDummyGPUInfoList);
this->RegisterOverride("vtkActor", "vtkOpenGLActor", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLActor);
this->RegisterOverride("vtkBillboardTextActor3D", "vtkOpenGLBillboardTextActor3D", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLBillboardTextActor3D);
this->RegisterOverride("vtkCamera", "vtkOpenGLCamera", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLCamera);
this->RegisterOverride("vtkLabeledContourMapper", "vtkOpenGLLabeledContourMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLLabeledContourMapper);
this->RegisterOverride("vtkHardwareSelector", "vtkOpenGLHardwareSelector", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLHardwareSelector);
this->RegisterOverride("vtkImageMapper", "vtkOpenGLImageMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLImageMapper);
this->RegisterOverride("vtkImageSliceMapper", "vtkOpenGLImageSliceMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLImageSliceMapper);
this->RegisterOverride("vtkGlyph3DMapper", "vtkOpenGLGlyph3DMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLGlyph3DMapper);
this->RegisterOverride("vtkLight", "vtkOpenGLLight", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLLight);
this->RegisterOverride("vtkPointGaussianMapper", "vtkOpenGLPointGaussianMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLPointGaussianMapper);
this->RegisterOverride("vtkPolyDataMapper", "vtkOpenGLPolyDataMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLPolyDataMapper);
this->RegisterOverride("vtkPolyDataMapper2D", "vtkOpenGLPolyDataMapper2D", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLPolyDataMapper2D);
this->RegisterOverride("vtkProperty", "vtkOpenGLProperty", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLProperty);
this->RegisterOverride("vtkShaderProperty", "vtkOpenGLShaderProperty", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLShaderProperty);
this->RegisterOverride("vtkUniforms", "vtkOpenGLUniforms", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLUniforms);
this->RegisterOverride("vtkRenderer", "vtkOpenGLRenderer", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLRenderer);
this->RegisterOverride("vtkRenderTimerLog", "vtkOpenGLRenderTimerLog", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLRenderTimerLog);
this->RegisterOverride("vtkSkybox", "vtkOpenGLSkybox", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLSkybox);
this->RegisterOverride("vtkTextActor", "vtkOpenGLTextActor", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLTextActor);
this->RegisterOverride("vtkTextActor3D", "vtkOpenGLTextActor3D", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLTextActor3D);
this->RegisterOverride("vtkTextMapper", "vtkOpenGLTextMapper", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLTextMapper);
this->RegisterOverride("vtkTexture", "vtkOpenGLTexture", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkOpenGLTexture);
this->RegisterOverride("vtkRenderWindow", "vtkWin32OpenGLRenderWindow", "Override for VTK::RenderingOpenGL2 module", 1, vtkObjectFactoryCreatevtkWin32OpenGLRenderWindow);

}

const char * vtkRenderingOpenGL2ObjectFactory::GetVTKSourceVersion()
{
  return VTK_SOURCE_VERSION;
}

void vtkRenderingOpenGL2ObjectFactory::PrintSelf(ostream &os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

// Registration of object factories.
static unsigned int vtkRenderingOpenGL2Count = 0;

VTKRENDERINGOPENGL2_EXPORT void vtkRenderingOpenGL2_AutoInit_Construct()
{
  if(++vtkRenderingOpenGL2Count == 1)
  {


    vtkRenderingOpenGL2ObjectFactory* factory = vtkRenderingOpenGL2ObjectFactory::New();
    if (factory)
    {
      // vtkObjectFactory keeps a reference to the "factory",
      vtkObjectFactory::RegisterFactory(factory);
      factory->Delete();
    }
  }
}
