from app.models.collection_point import CollectionPoint


class CollectionPointService:
    def __init__(self, repository):
        self._repository = repository

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacio.")

    def _validate_capacity(self, capacity_kg: float) -> None:
        if float(capacity_kg) <= 0:
            raise ValueError("La capacidad maxima debe ser un numero positivo mayor a 0.")

    def _validate_point_id_unique(self, point_id: str) -> None:
        if self._repository.get_by_id(point_id):
            raise ValueError(f"El ID del punto de recoleccion '{point_id}' ya existe.")

    def _clean_materials(self, accepted_materials: str) -> str:
        materials = [
            material.strip().lower()
            for material in accepted_materials.split(",")
            if material.strip()
        ]

        if not materials:
            raise ValueError("Debe indicar al menos un material aceptado para este punto.")

        return ",".join(materials)

    def register_collection_point(
        self,
        point_id: str,
        name: str,
        location: str,
        district: str,
        accepted_materials: str,
        capacity_kg: float,
    ) -> CollectionPoint:
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(name, "name")
        self._validate_not_empty(location, "location")
        self._validate_not_empty(district, "district")
        self._validate_not_empty(accepted_materials, "accepted_materials")
        self._validate_capacity(capacity_kg)
        self._validate_point_id_unique(point_id.strip())

        point = CollectionPoint(
            point_id=point_id.strip(),
            name=name.strip(),
            location=location.strip(),
            district=district.strip(),
            accepted_materials=self._clean_materials(accepted_materials),
            capacity_kg=float(capacity_kg),
            current_load_kg=0.0,
            is_active=True,
        )

        return self._repository.add(point)

    def get_all_points(self) -> list:
        return self._repository.get_all()

    def get_point_by_id(self, point_id: str) -> CollectionPoint:
        self._validate_not_empty(point_id, "point_id")
        point = self._repository.get_by_id(point_id.strip())
        if not point:
            raise ValueError(f"Punto de recoleccion con ID '{point_id}' no encontrado.")
        return point

    def list_active_points(self) -> list:
        return [point for point in self._repository.get_all() if point.is_active]

    def calculate_occupancy_percentage(self, point: CollectionPoint) -> float:
        if point.capacity_kg == 0:
            return 0.0
        return (point.current_load_kg / point.capacity_kg) * 100

    def add_load(self, point_id: str, weight_kg: float) -> CollectionPoint:
        point = self.get_point_by_id(point_id)
        point.current_load_kg += float(weight_kg)
        return self._repository.update(point)

    def set_active_status(self, point_id: str, is_active: bool) -> CollectionPoint:
        point = self.get_point_by_id(point_id)
        point.is_active = is_active
        return self._repository.update(point)

    def update_collection_point(
        self,
        point_id: str,
        name: str | None = None,
        location: str | None = None,
        district: str | None = None,
        accepted_materials: str | None = None,
        capacity_kg: float | None = None,
        current_load_kg: float | None = None,
        is_active: bool | None = None,
    ) -> CollectionPoint:
        point = self.get_point_by_id(point_id)

        if name is not None:
            self._validate_not_empty(name, "name")
            point.name = name.strip()

        if location is not None:
            self._validate_not_empty(location, "location")
            point.location = location.strip()

        if district is not None:
            self._validate_not_empty(district, "district")
            point.district = district.strip()

        if accepted_materials is not None:
            self._validate_not_empty(accepted_materials, "accepted_materials")
            point.accepted_materials = self._clean_materials(accepted_materials)

        if capacity_kg is not None:
            self._validate_capacity(capacity_kg)
            if point.current_load_kg > float(capacity_kg):
                raise ValueError("La capacidad no puede ser menor a la carga actual del punto.")
            point.capacity_kg = float(capacity_kg)

        if current_load_kg is not None:
            if float(current_load_kg) < 0:
                raise ValueError("La carga actual no puede ser negativa.")
            if float(current_load_kg) > point.capacity_kg:
                raise ValueError("La carga actual no puede superar la capacidad maxima.")
            point.current_load_kg = float(current_load_kg)

        if is_active is not None:
            point.is_active = is_active

        return self._repository.update(point)

    def delete_collection_point(self, point_id: str) -> None:
        point = self.get_point_by_id(point_id)
        self._repository.delete(point)
