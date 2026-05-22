from fastapi import APIRouter, Request
from controllers.pqrs_controller import PqrsController
from models.pqrs_model import Pqrs

router = APIRouter(prefix="/pqrs", tags=["pqrs"])
controller = PqrsController()

@router.post("/")
@router.post("/create_pqrs")
async def create_pqrs(request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.create_pqrs(pqrs)

@router.get("/")
async def get_pqrs_all():
    return controller.get_pqrs_all()

@router.get("/{id_pqrs}")
async def get_pqrs(id_pqrs: int):
    return controller.get_pqrs(id_pqrs)

@router.put("/update_pqrs/{id_pqrs}")
async def update_pqrs(id_pqrs: int, request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.update_pqrs(id_pqrs, pqrs)

@router.delete("/delete_pqrs/{id_pqrs}")
async def delete_pqrs(id_pqrs: int):
    return controller.delete_pqrs(id_pqrs)

@router.get("/pdf/{id_pqrs}")
async def generate_pdf(id_pqrs: int):
    from fastapi.responses import Response
    pdf_bytes = controller.generate_pdf(id_pqrs)
    return Response(
        content=pdf_bytes, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f'attachment; filename="PQRS_{id_pqrs}.pdf"'}
    )