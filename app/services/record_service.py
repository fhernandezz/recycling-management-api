from datetime import date

from app.models.recycling_record import RecyclingRecord

VALID_MATERIALS = {"plastico", "vidrio", "papel", "metal", "organico"}


class RecordService:
    def __init__(self, repository, recycler_service, point_service):
        self._repository = repository
        self._recycler_service = recycler_service
        self._point_service = point_service

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacio.")

    def _validate_record_id_unique(self, record_id: str) -> None:
        if self._repository.get_by_id(record_id):
            raise ValueError(f"El ID de registro '{record_id}' ya existe.")

    def _parse_date(self, value: str) -> date:
        normalized_value = value.split("T")[0]
        return date.fromisoformat(normalized_value)

    def register_delivery(
        self,
        record_id: str,
        recycler_id: str,
        point_id: str,
        material_type: str,
        weight_kg: float,
        notes: str = "",
        record_date: date | None = None,
    ) -> RecyclingRecord:
        self._validate_not_empty(record_id, "record_id")
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(point_id, "point_id")
        self._validate_not_empty(material_type, "material_type")
        self._validate_record_id_unique(record_id.strip())

        clean_material = material_type.strip().lower()

        if clean_material not in VALID_MATERIALS:
            raise ValueError(f"El tipo de material '{material_type}' no es valido en el sistema.")

        if float(weight_kg) <= 0:
            raise ValueError("El peso de la entrega debe ser un numero mayor a cero.")

        recycler = self._recycler_service.get_recycler_by_id(recycler_id.strip())
        if not recycler.is_active:
            raise ValueError("Operacion denegada: el reciclador se encuentra inactivo.")

        point = self._point_service.get_point_by_id(point_id.strip())
        if not point.is_active:
            raise ValueError("Operacion denegada: el punto de recoleccion esta inactivo.")

        accepted_materials = [
            material.strip().lower()
            for material in point.accepted_materials.split(",")
            if material.strip()
        ]
        if clean_material not in accepted_materials:
            raise ValueError(f"Este punto de recoleccion no acepta el material '{material_type}'.")

        if point.current_load_kg + float(weight_kg) > point.capacity_kg:
            raise ValueError("La entrega supera la capacidad maxima restante del punto.")

        record = RecyclingRecord(
            record_id=record_id.strip(),
            recycler_id=recycler.recycler_id,
            point_id=point.point_id,
            material_type=clean_material,
            weight_kg=float(weight_kg),
            record_date=record_date or date.today(),
            notes=notes.strip(),
        )

        created_record = self._repository.add(record)
        self._point_service.add_load(point.point_id, float(weight_kg))
        return created_record

    def get_all_records(self) -> list:
        return self._repository.get_all()

    def get_record_by_id(self, record_id: str) -> RecyclingRecord:
        self._validate_not_empty(record_id, "record_id")
        record = self._repository.get_by_id(record_id.strip())
        if not record:
            raise ValueError(f"Registro con ID '{record_id}' no encontrado.")
        return record

    def get_records_by_recycler(self, recycler_id: str) -> list:
        self._recycler_service.get_recycler_by_id(recycler_id)
        return self._repository.get_by_recycler(recycler_id)

    def get_records_by_point(self, point_id: str) -> list:
        self._point_service.get_point_by_id(point_id)
        return self._repository.get_by_point(point_id)

    def get_top_recyclers(self) -> list:
        totals_per_recycler = {}

        for record in self._repository.get_all():
            if record.recycler_id not in totals_per_recycler:
                totals_per_recycler[record.recycler_id] = [0.0, 0]
            totals_per_recycler[record.recycler_id][0] += record.weight_kg
            totals_per_recycler[record.recycler_id][1] += 1

        recycler_tuples = []
        for recycler_id, metrics in totals_per_recycler.items():
            try:
                recycler = self._recycler_service.get_recycler_by_id(recycler_id)
                recycler_tuples.append(
                    (recycler.full_name, recycler.district, metrics[0], metrics[1])
                )
            except ValueError:
                continue

        return sorted(recycler_tuples, key=lambda item: item[2], reverse=True)

    def get_collection_points_status(self) -> list:
        status_report = []

        for point in self._point_service.list_active_points():
            occupancy_percentage = self._point_service.calculate_occupancy_percentage(point)

            if occupancy_percentage > 80.0:
                status = "Critico"
            elif occupancy_percentage > 60.0:
                status = "Atencion"
            else:
                status = "Normal"

            status_report.append({
                "name": point.name,
                "current_load": point.current_load_kg,
                "max_capacity": point.capacity_kg,
                "percentage": round(occupancy_percentage, 2),
                "status": status,
            })

        return status_report

    def get_materials_breakdown(self) -> dict:
        kg_per_material = {material: 0.0 for material in VALID_MATERIALS}

        for record in self._repository.get_all():
            if record.material_type in kg_per_material:
                kg_per_material[record.material_type] += record.weight_kg

        return kg_per_material

    def get_records_by_date_range(self, start_date_str: str, end_date_str: str) -> dict:
        self._validate_not_empty(start_date_str, "start_date")
        self._validate_not_empty(end_date_str, "end_date")

        start_date = self._parse_date(start_date_str)
        end_date = self._parse_date(end_date_str)

        if start_date > end_date:
            raise ValueError("La fecha de inicio no puede ser posterior a la fecha de fin.")

        filtered_records = []
        total_period_kg = 0.0

        for record in self._repository.get_by_date_range(start_date, end_date):
            try:
                recycler_name = self._recycler_service.get_recycler_by_id(record.recycler_id).full_name
            except ValueError:
                recycler_name = "Desconocido"

            try:
                point_name = self._point_service.get_point_by_id(record.point_id).name
            except ValueError:
                point_name = "Desconocido"

            filtered_records.append({
                "recycler_name": recycler_name,
                "point_name": point_name,
                "material": record.material_type,
                "weight": record.weight_kg,
                "date": record.record_date,
            })
            total_period_kg += record.weight_kg

        return {
            "records": filtered_records,
            "total_period_kg": round(total_period_kg, 2),
        }

    def update_record(
        self,
        record_id: str,
        recycler_id: str | None = None,
        point_id: str | None = None,
        material_type: str | None = None,
        weight_kg: float | None = None,
        record_date: date | None = None,
        notes: str | None = None,
    ) -> RecyclingRecord:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Registro con ID '{record_id}' no encontrado.")

        if recycler_id is not None:
            recycler = self._recycler_service.get_recycler_by_id(recycler_id)
            if not recycler.is_active:
                raise ValueError("Operacion denegada: el reciclador se encuentra inactivo.")
            record.recycler_id = recycler.recycler_id

        old_point = self._point_service.get_point_by_id(record.point_id)
        target_point = self._point_service.get_point_by_id(point_id or record.point_id)
        target_weight = float(weight_kg) if weight_kg is not None else record.weight_kg
        target_material = material_type.strip().lower() if material_type is not None else record.material_type

        if point_id is not None:
            if not target_point.is_active:
                raise ValueError("Operacion denegada: el punto de recoleccion esta inactivo.")

        accepted_materials = [
            material.strip().lower()
            for material in target_point.accepted_materials.split(",")
            if material.strip()
        ]

        if material_type is not None:
            if target_material not in VALID_MATERIALS:
                raise ValueError(f"El tipo de material '{material_type}' no es valido en el sistema.")

        if target_material not in accepted_materials:
            raise ValueError(f"Este punto de recoleccion no acepta el material '{target_material}'.")

        if weight_kg is not None:
            if target_weight <= 0:
                raise ValueError("El peso de la entrega debe ser un numero mayor a cero.")

        if old_point.point_id == target_point.point_id:
            target_load = old_point.current_load_kg + (target_weight - record.weight_kg)
            if target_load > old_point.capacity_kg:
                raise ValueError("La entrega supera la capacidad maxima restante del punto.")
            if target_load < 0:
                raise ValueError("La carga actual del punto no puede quedar negativa.")
            old_point.current_load_kg = target_load
            self._point_service._repository.update(old_point)
        else:
            old_point.current_load_kg = max(0.0, old_point.current_load_kg - record.weight_kg)
            if target_point.current_load_kg + target_weight > target_point.capacity_kg:
                raise ValueError("La entrega supera la capacidad maxima restante del nuevo punto.")
            target_point.current_load_kg += target_weight
            self._point_service._repository.update(old_point)
            self._point_service._repository.update(target_point)

        record.point_id = target_point.point_id
        record.material_type = target_material
        record.weight_kg = target_weight

        if record_date is not None:
            record.record_date = record_date

        if notes is not None:
            record.notes = notes.strip()

        return self._repository.update(record)

    def delete_record(self, record_id: str) -> None:
        record = self._repository.get_by_id(record_id)
        if not record:
            raise ValueError(f"Registro con ID '{record_id}' no encontrado.")

        point = self._point_service.get_point_by_id(record.point_id)
        point.current_load_kg = max(0.0, point.current_load_kg - record.weight_kg)
        self._point_service._repository.update(point)
        self._repository.delete(record)
