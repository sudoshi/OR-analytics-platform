from fastapi import APIRouter, HTTPException, status, Depends, Response
from services.piece_repository_service import PieceRepositoryService
from schemas.context.auth_context import AuthorizationContextData
from schemas.requests.piece_repository import CreateRepositoryRequest, PatchRepositoryRequest, ListRepositoryFilters
from schemas.responses.piece_repository import (
    CreateRepositoryReponse,
    GetRepositoryReleasesResponse,
    GetRepositoryReleaseDataResponse,
    GetWorkspaceRepositoriesResponse,
    GetRepositoryResponse
)
from database.models.enums import RepositorySource
from schemas.exceptions.base import BaseException, ConflictException, ForbiddenException, ResourceNotFoundException, UnauthorizedException
from schemas.errors.base import ConflictError, ForbiddenError, ResourceNotFoundError, SomethingWrongError, UnauthorizedError
from typing import List, Optional
from auth.permission_authorizer import Authorizer
from database.models.enums import Permission


router = APIRouter(prefix="/pieces-repositories")


piece_repository_service = PieceRepositoryService()

admin_authorizer = Authorizer(permission_level=Permission.admin.value)
read_authorizer = Authorizer(permission_level=Permission.read.value)


@router.post(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': CreateRepositoryReponse},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_404_NOT_FOUND: {'model': ResourceNotFoundError},
        status.HTTP_409_CONFLICT: {'model': ConflictError},
        status.HTTP_401_UNAUTHORIZED: {'model': UnauthorizedError}
    },
)
def create_piece_repository(
    body: CreateRepositoryRequest,
    auth_context: AuthorizationContextData = Depends(admin_authorizer.authorize_with_body)
) -> CreateRepositoryReponse:
    """
    Create piece repository for workspace.
    Only one piece repository version is allowed for each workspace.
    """
    try:
        response = piece_repository_service.create_piece_repository(
            piece_repository_data=body,
            auth_context=auth_context
        )
        return response
    except (BaseException, ForbiddenException, ConflictException, ResourceNotFoundException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    path="/releases",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': List[GetRepositoryReleasesResponse]},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_404_NOT_FOUND: {'model': ResourceNotFoundError},
        status.HTTP_401_UNAUTHORIZED: {'model': UnauthorizedError}
    },
)
def get_piece_repository_releases(
    source: RepositorySource,
    path: str,
    workspace_id: int,
    auth_context: AuthorizationContextData = Depends(read_authorizer.authorize)
) -> List[GetRepositoryReleasesResponse]:
    """Get piece repository releases"""
    try:
        response = piece_repository_service.get_piece_repository_releases(
            source=source,
            path=path,
            auth_context=auth_context,
        )
        return response
    except (BaseException, ForbiddenException, ResourceNotFoundException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    path="/releases/{version}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetRepositoryReleaseDataResponse},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_404_NOT_FOUND: {'model': ResourceNotFoundError},
        status.HTTP_401_UNAUTHORIZED: {'model': UnauthorizedError}
    },
)
def get_piece_repository_release_data(
    version: str,
    source: RepositorySource,
    path: str,
    workspace_id: int,
    auth_context: AuthorizationContextData = Depends(read_authorizer.authorize)
) -> GetRepositoryReleaseDataResponse:
    """Get piece repository release data"""
    try:
        response = piece_repository_service.get_piece_repository_release_data(
            version=version,
            source=source,
            path=path,
            auth_context=auth_context,
        )
        return response
    except (BaseException, ForbiddenException, ResourceNotFoundException, UnauthorizedException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetWorkspaceRepositoriesResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
    },
    dependencies=[Depends(read_authorizer.authorize)]
)
def get_pieces_repositories(
    workspace_id: int,
    page: Optional[int] = 0,
    page_size: Optional[int] = 100,
    filters: ListRepositoryFilters = Depends(),
) -> GetWorkspaceRepositoriesResponse:
    """Get pieces repositories for workspace"""
    try:
        response = piece_repository_service.get_pieces_repositories(
            workspace_id=workspace_id,
            page=page,
            page_size=page_size,
            filters=filters
        )
        return response
    except (BaseException, ForbiddenException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    path="/worker",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetWorkspaceRepositoriesResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_403_FORBIDDEN: {'model': ForbiddenError},
    },
)
def get_pieces_repositories_worker(
    workspace_id: int,
    page: Optional[int] = 0,
    page_size: Optional[int] = 100,
    filters: ListRepositoryFilters = Depends(),
) -> GetWorkspaceRepositoriesResponse:
    """
    Get pieces repositories for workspace.
    This endpoint is used by the worker to get the repositories to be processed.
    Is the same endpoint as the one above, but without the auth service.
    The authorization is done by our service mesh Authorization Policy.
    """
    try:
        response = piece_repository_service.get_pieces_repositories(
            workspace_id=workspace_id,
            page=page,
            page_size=page_size,
            filters=filters
        )
        return response
    except (BaseException, ForbiddenException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.delete(
    path="/{piece_repository_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    responses={
        status.HTTP_204_NO_CONTENT: {},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {"model": SomethingWrongError},
        status.HTTP_404_NOT_FOUND: {"model": ResourceNotFoundError},
        status.HTTP_403_FORBIDDEN: {"model": ForbiddenError},
        status.HTTP_409_CONFLICT: {"model": ConflictError}
    },
)
def delete_repository(
    piece_repository_id: int,
    auth_context: AuthorizationContextData = Depends(admin_authorizer.authorize_piece_repository)
):
    try:
        response =  piece_repository_service.delete_repository(
            piece_repository_id=piece_repository_id
        )
        return response
    except (BaseException, ResourceNotFoundException, ForbiddenException, ConflictException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)


@router.get(
    path="/{piece_repository_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_200_OK: {'model': GetRepositoryResponse},
        status.HTTP_500_INTERNAL_SERVER_ERROR: {'model': SomethingWrongError},
        status.HTTP_404_NOT_FOUND: {'model': ResourceNotFoundError}
    },

)
def get_piece_repository(
    piece_repository_id: int,
    auth_context: AuthorizationContextData = Depends(read_authorizer.authorize_piece_repository)
) -> GetRepositoryResponse:
    """Get piece repository info by id"""
    try:
        response = piece_repository_service.get_piece_repository(
            piece_repository_id=piece_repository_id
        )
        return response
    except (BaseException, ResourceNotFoundException) as e:
        raise HTTPException(status_code=e.status_code, detail=e.message)
