#include "RenderWindowUISingleInheritance.h"
#include "ui_RenderWindowUISingleInheritance.h"

#include <vtkCamera.h>
#include <vtkGenericOpenGLRenderWindow.h>
#include <vtkLookupTable.h>
#include <vtkNamedColors.h>
#include <vtkNew.h>
#include <vtkPlatonicSolidSource.h>
#include <vtkPolyDataMapper.h>
#include <vtkProperty.h>
#include <vtkRenderWindow.h>
#include <vtkRenderer.h>
#include <vtkSphereSource.h>
#include <vtkVersion.h>

#if VTK_VERSION_NUMBER >= 89000000000ULL
#define VTK890 1
#endif

namespace {
/** Get a specialised lookup table for the platonic solids.
 *
 * Since each face of a vtkPlatonicSolidSource has a different
 * cell scalar, we create a lookup table with a different colour
 * for each face.
 * The colors have been carefully chosen so that adjacent cells
 * are colored distinctly.
 *
 * @return The lookup table.
 */
vtkNew<vtkLookupTable> GetPlatonicLUT();
} // namespace

// Constructor
RenderWindowUISingleInheritance::RenderWindowUISingleInheritance(
    QWidget* parent)
  : QMainWindow(parent), ui(new Ui::RenderWindowUISingleInheritance)
{
  this->ui->setupUi(this);

  vtkNew<vtkNamedColors> colors;

  vtkNew<vtkGenericOpenGLRenderWindow> renderWindow;
#if VTK890
  this->ui->qvtkWidget->setRenderWindow(renderWindow);
#else
  this->ui->qvtkWidget->SetRenderWindow(renderWindow);
#endif

  auto lut = GetPlatonicLUT();

  vtkNew<vtkPlatonicSolidSource> source1, source2;
  source1->SetSolidTypeToCube();
  source2->SetSolidTypeToOctahedron();

  vtkNew<vtkPolyDataMapper> mapper1, mapper2;
  mapper1->SetInputConnection(source1->GetOutputPort());
  mapper1->SetLookupTable(lut);
  mapper1->SetScalarRange(0, 19);
  mapper2->SetInputConnection(source2->GetOutputPort());
  mapper2->SetLookupTable(lut);
  mapper2->SetScalarRange(0, 19);

  vtkNew<vtkActor> actor1, actor2;
  actor1->SetMapper(mapper1);
  actor2->SetMapper(mapper2);
  actor1->SetPosition(1, 1, 1);

  vtkNew<vtkRenderer> renderer;
  renderer->AddActor(actor1);
  renderer->AddActor(actor2);
  renderer->GetActiveCamera()->Azimuth(180.0);
  renderer->ResetCamera();
  renderer->SetBackground(colors->GetColor3d("SteelBlue").GetData());

  // VTK/Qt wedded
#if VTK890
  this->ui->qvtkWidget->renderWindow()->AddRenderer(renderer);
  this->ui->qvtkWidget->renderWindow()->SetWindowName(
      "RenderWindowUISingleInheritance");
#else
  this->ui->qvtkWidget->GetRenderWindow()->AddRenderer(renderer);
  this->ui->qvtkWidget->GetRenderWindow()->SetWindowName(
      "RenderWindowUISingleInheritance");
#endif
  // Set up action signals and slots
  connect(this->ui->actionExit, SIGNAL(triggered()), this, SLOT(slotExit()));
}

RenderWindowUISingleInheritance::~RenderWindowUISingleInheritance()
{
  delete this->ui;
}

void RenderWindowUISingleInheritance::slotExit()
{
  qApp->exit();
}

namespace {

vtkNew<vtkLookupTable> GetPlatonicLUT()
{
  vtkNew<vtkLookupTable> lut;
  lut->SetNumberOfTableValues(20);
  lut->SetTableRange(0.0, 19.0);
  lut->Build();
  lut->SetTableValue(0, 1, 1, 1);
  lut->SetTableValue(1, 1, 1, 1);
  lut->SetTableValue(2, 1, 1, 1);
  lut->SetTableValue(3, 1, 1, 1);
  lut->SetTableValue(4, 1, 1, 1);
  lut->SetTableValue(5, 1, 1, 1);
  return lut;
}

} // namespace
