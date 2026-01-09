"""
API эндпоинты для заправочных станций (пользовательские)
"""
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import uuid

from app.database import get_db
from app.models.user import User
from app.api.deps import get_current_active_user
from app.services.gas_station_service.crud import (
    create_gas_station,
    get_gas_station_by_id,
    get_gas_stations,
    create_review,
    get_reviews_by_station,
    update_review,
    delete_review,
    add_gas_station_photo,
    get_gas_station_photos,
    delete_gas_station_photo,
    create_or_update_fuel_price,
    bulk_update_fuel_prices,
    get_fuel_prices_by_station,
)
from app.schemas.gas_station import (
    GasStationCreate,
    GasStationResponse,
    GasStationDetailResponse,
    GasStationListResponse,
    GasStationFilter,
    FuelPriceCreate,
    ReviewCreate,
    ReviewResponse,
    ReviewUpdate,
    GasStationPhotoResponse,
    BulkFuelPriceUpdate,
)
from app.core.config import settings
from app.models.gas_station import StationStatus

router = APIRouter()

# Директория для загрузки фотографий станций
GAS_STATION_PHOTOS_DIR = Path(settings.UPLOAD_DIR) / "gas_stations"
GAS_STATION_PHOTOS_DIR.mkdir(parents=True, exist_ok=True)


def save_uploaded_photo(file: UploadFile, station_id: int) -> str:
    """Сохранение загруженной фотографии и возврат URL"""
    file_extension = Path(file.filename).suffix if file.filename else ".jpg"
    unique_filename = f"{station_id}_{uuid.uuid4().hex}{file_extension}"
    file_path = GAS_STATION_PHOTOS_DIR / unique_filename
    
    with open(file_path, "wb") as buffer:
        content = file.file.read()
        buffer.write(content)
    
    # Возвращаем URL
    relative_path = f"uploads/gas_stations/{unique_filename}"
    return f"{settings.BASE_URL}/{relative_path}"


@router.post("/", response_model=GasStationResponse, status_code=status.HTTP_201_CREATED)
async def create_station(
    station_data: GasStationCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Создание новой заправочной станции (требует модерации)"""
    station = create_gas_station(
        db=db,
        station_data=station_data,
        created_by_user_id=current_user.id
    )
    
    # Загружаем данные станции с ценами и фотографиями
    db.refresh(station)
    return GasStationResponse.model_validate(station)


@router.get("/", response_model=GasStationListResponse)
async def list_stations(
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    fuel_type: Optional[str] = Query(None, description="Тип топлива: AI-80, AI-91, AI-95, AI-98, Дизель, Газ"),
    min_rating: Optional[float] = Query(None, ge=0, le=5),
    max_price: Optional[float] = Query(None, gt=0),
    is_24_7: Optional[bool] = Query(None),
    has_promotions: Optional[bool] = Query(None),
    search_query: Optional[str] = Query(None),
    latitude: Optional[float] = Query(None, ge=-90, le=90),
    longitude: Optional[float] = Query(None, ge=-180, le=180),
    radius_km: Optional[float] = Query(None, gt=0)
):
    """Получение списка заправочных станций с фильтрацией"""
    filters = GasStationFilter(
        fuel_type=fuel_type,
        min_rating=min_rating,
        max_price=max_price,
        is_24_7=is_24_7,
        has_promotions=has_promotions,
        search_query=search_query,
        latitude=latitude,
        longitude=longitude,
        radius_km=radius_km
    )
    
    stations, total = get_gas_stations(db, skip=skip, limit=limit, filters=filters)
    
    # Преобразуем в ответы
    station_responses = []
    for station in stations:
        station_dict = GasStationResponse.model_validate(station).model_dump()
        # Находим главную фотографию
        main_photo = next((p for p in station.photos if p.is_main), None)
        if main_photo:
            station_dict["main_photo"] = main_photo.photo_url
        station_responses.append(GasStationResponse(**station_dict))
    
    return GasStationListResponse(
        stations=station_responses,
        total=total,
        skip=skip,
        limit=limit
    )


@router.get("/{station_id}", response_model=GasStationDetailResponse)
async def get_station(
    station_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Получение детальной информации о заправочной станции"""
    station = get_gas_station_by_id(db, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    if station.status != StationStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    # Получаем отзывы
    reviews, _ = get_reviews_by_station(db, station_id, skip=0, limit=50)
    
    # Преобразуем отзывы с именами пользователей
    from app.services.user_service.crud import get_user_extended_by_id
    review_responses = []
    for review in reviews:
        review_dict = ReviewResponse.model_validate(review).model_dump()
        user_extended = get_user_extended_by_id(db, review.user_id)
        if user_extended:
            review_dict["user_name"] = user_extended.name
        review_responses.append(ReviewResponse(**review_dict))
    
    station_dict = GasStationDetailResponse.model_validate(station).model_dump()
    station_dict["reviews"] = review_responses
    
    # Находим главную фотографию
    main_photo = next((p for p in station.photos if p.is_main), None)
    if main_photo:
        station_dict["main_photo"] = main_photo.photo_url
    
    return GasStationDetailResponse(**station_dict)


@router.post("/{station_id}/photos", response_model=GasStationPhotoResponse, status_code=status.HTTP_201_CREATED)
async def upload_station_photo(
    station_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)],
    file: Annotated[UploadFile, File(...)],
    is_main: bool = Query(False),
    order: int = Query(0, ge=0)
):
    """Загрузка фотографии для заправочной станции"""
    station = get_gas_station_by_id(db, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    # Проверяем права: только создатель или админ может добавлять фото
    if station.created_by_user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для добавления фотографий"
        )
    
    # Проверяем тип файла
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Недопустимый тип файла. Разрешены: {', '.join(settings.ALLOWED_IMAGE_TYPES)}"
        )
    
    # Сохраняем файл
    photo_url = save_uploaded_photo(file, station_id)
    
    # Добавляем в БД
    photo = add_gas_station_photo(
        db=db,
        station_id=station_id,
        photo_url=photo_url,
        is_main=is_main,
        order=order,
        uploaded_by_user_id=current_user.id if not current_user.is_admin else None,
        uploaded_by_admin_id=current_user.id if current_user.is_admin else None
    )
    
    return GasStationPhotoResponse.model_validate(photo)


@router.delete("/{station_id}/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_station_photo(
    station_id: int,
    photo_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Удаление фотографии заправочной станции"""
    station = get_gas_station_by_id(db, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    photo = next((p for p in station.photos if p.id == photo_id), None)
    if not photo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Фотография не найдена"
        )
    
    # Проверяем права
    if station.created_by_user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для удаления фотографий"
        )
    
    delete_gas_station_photo(db, photo_id)
    return None


@router.post("/{station_id}/fuel-prices", response_model=list[FuelPriceCreate])
async def update_fuel_prices(
    station_id: int,
    prices: BulkFuelPriceUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Обновление цен на топливо для станции"""
    station = get_gas_station_by_id(db, station_id)
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    # Проверяем права: только создатель или админ может обновлять цены
    if station.created_by_user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Нет прав для обновления цен"
        )
    
    updated_prices = bulk_update_fuel_prices(
        db=db,
        station_id=station_id,
        prices=prices.fuel_prices,
        updated_by_user_id=current_user.id if not current_user.is_admin else None,
        updated_by_admin_id=current_user.id if current_user.is_admin else None
    )
    
    return [FuelPriceCreate.model_validate(p) for p in updated_prices]


@router.post("/{station_id}/reviews", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def create_station_review(
    station_id: int,
    review_data: ReviewCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Создание отзыва о заправочной станции"""
    station = get_gas_station_by_id(db, station_id)
    if not station or station.status != StationStatus.APPROVED:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Заправочная станция не найдена"
        )
    
    review = create_review(
        db=db,
        station_id=station_id,
        user_id=current_user.id,
        review_data=review_data
    )
    
    # Получаем имя пользователя
    from app.services.user_service.crud import get_user_extended_by_id
    user_extended = get_user_extended_by_id(db, current_user.id)
    review_dict = ReviewResponse.model_validate(review).model_dump()
    if user_extended:
        review_dict["user_name"] = user_extended.name
    
    return ReviewResponse(**review_dict)


@router.put("/{station_id}/reviews/{review_id}", response_model=ReviewResponse)
async def update_station_review(
    station_id: int,
    review_id: int,
    review_update: ReviewUpdate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Обновление отзыва о заправочной станции"""
    review = update_review(
        db=db,
        review_id=review_id,
        user_id=current_user.id,
        review_update=review_update
    )
    
    if not review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    
    # Получаем имя пользователя
    from app.services.user_service.crud import get_user_extended_by_id
    user_extended = get_user_extended_by_id(db, current_user.id)
    review_dict = ReviewResponse.model_validate(review).model_dump()
    if user_extended:
        review_dict["user_name"] = user_extended.name
    
    return ReviewResponse(**review_dict)


@router.delete("/{station_id}/reviews/{review_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_station_review(
    station_id: int,
    review_id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Annotated[Session, Depends(get_db)]
):
    """Удаление отзыва о заправочной станции"""
    success = delete_review(db, review_id, current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Отзыв не найден"
        )
    return None

