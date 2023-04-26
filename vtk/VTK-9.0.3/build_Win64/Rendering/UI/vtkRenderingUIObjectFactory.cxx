/*=========================================================================

  Program:   Visualization Toolkit
  Module:    vtkRenderingUIObjectFactory.cxx

  Copyright (c) Ken Martin, Will Schroeder, Bill Lorensen
  All rights reserved.
  See Copyright.txt or http://www.kitware.com/Copyright.htm for details.

     This software is distributed WITHOUT ANY WARRANTY; without even
     the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
     PURPOSE.  See the above copyright notice for more information.

=========================================================================*/

#include "vtkRenderingUIObjectFactory.h"
#include "vtkVersion.h"

// Include all of the classes we want to create overrides for.
#include "vtkWin32RenderWindowInteractor.h"
#include "vtkWin32HardwareWindow.h"


vtkStandardNewMacro(vtkRenderingUIObjectFactory);

// Now create the functions to create overrides with.
VTK_CREATE_CREATE_FUNCTION(vtkWin32RenderWindowInteractor)
VTK_CREATE_CREATE_FUNCTION(vtkWin32HardwareWindow)


vtkRenderingUIObjectFactory::vtkRenderingUIObjectFactory()
{
this->RegisterOverride("vtkRenderWindowInteractor", "vtkWin32RenderWindowInteractor", "Override for VTK::RenderingUI module", 1, vtkObjectFactoryCreatevtkWin32RenderWindowInteractor);
this->RegisterOverride("vtkHardwareWindow", "vtkWin32HardwareWindow", "Override for VTK::RenderingUI module", 1, vtkObjectFactoryCreatevtkWin32HardwareWindow);

}

const char * vtkRenderingUIObjectFactory::GetVTKSourceVersion()
{
  return VTK_SOURCE_VERSION;
}

void vtkRenderingUIObjectFactory::PrintSelf(ostream &os, vtkIndent indent)
{
  this->Superclass::PrintSelf(os, indent);
}

// Registration of object factories.
static unsigned int vtkRenderingUICount = 0;

VTKRENDERINGUI_EXPORT void vtkRenderingUI_AutoInit_Construct()
{
  if(++vtkRenderingUICount == 1)
  {


    vtkRenderingUIObjectFactory* factory = vtkRenderingUIObjectFactory::New();
    if (factory)
    {
      // vtkObjectFactory keeps a reference to the "factory",
      vtkObjectFactory::RegisterFactory(factory);
      factory->Delete();
    }
  }
}
