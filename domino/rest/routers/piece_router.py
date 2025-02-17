from fastapi import APIRouter, HTTPException, status, Depends
from services.piece_service import PieceService
from schemas.context.auth_context import AuthorizationContextData
from schemas.requests.piece import ListPiecesFilters
from schemas.responses.piece import GetPiecesResponse
from schemas.exceptions.base import BaseException, ForbiddenException
from schemas.errors.base import SomethingWrongError, ForbiddenError
from typing import List
from auth.permission_authorizer import Authorizer
from database.models.enums import Permission

router = APIRouter(prefix="/pieces-repositories/{piece_repository_id}/pieces")

piece_service = PieceService()
read_authorizer = Authorizer(permission_level=Permission.read.value)


@router.get(
    path='',
    status_code=200,
    responses={
        status.HTTP_200_OK: {'model': List[GetPiecesResponse]},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError}
    }
)
def get_pieces(
    piece_repository_id: int,
    page: int = 0,
    page_size: int = 100,
    filters: ListPiecesFilters = Depends(),
    auth_context: AuthorizationContextData = Depends(read_authorizer.authorize_piece_repository)
):
    """List pieces from a piece repository"""
    try:
        response = piece_service.list_pieces(
            piece_repository_id=piece_repository_id,
            page=page,
            page_size=page_size,
            filters=filters
        )
        return response
    except (BaseException, ForbiddenException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)