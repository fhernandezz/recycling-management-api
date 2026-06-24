from datetime import date
from app.models.recycler import Recycler


class RecyclerService:
    def __init__(self, repository):
        self._repository = repository

    def _validate_not_empty(self, value: str, field_name: str) -> None:
        if not value or not str(value).strip():
            raise ValueError(f"El campo '{field_name}' no puede estar vacio.")

    def _validate_email_format(self, email: str) -> None:
        if "@" not in email:
            raise ValueError(f"El correo '{email}' no tiene un formato valido.")

    def _validate_id_number_unique(self, id_number: str) -> None:
        if self._repository.get_by_id_number(id_number):
            raise ValueError(f"Ya existe un reciclador registrado con la cedula '{id_number}'.")

    def _validate_recycler_id_unique(self, recycler_id: str) -> None:
        if self._repository.get_by_id(recycler_id):
            raise ValueError(f"El ID de reciclador '{recycler_id}' ya existe.")

    def register_recycler(
        self,
        recycler_id: str,
        full_name: str,
        id_number: str,
        email: str,
        phone: str,
        district: str,
        registration_date: date | None = None,
    ) -> Recycler:
        self._validate_not_empty(recycler_id, "recycler_id")
        self._validate_not_empty(full_name, "full_name")
        self._validate_not_empty(id_number, "id_number")
        self._validate_not_empty(email, "email")
        self._validate_not_empty(phone, "phone")
        self._validate_not_empty(district, "district")
        self._validate_email_format(email)
        self._validate_recycler_id_unique(recycler_id.strip())
        self._validate_id_number_unique(id_number.strip())

        recycler = Recycler(
            recycler_id=recycler_id.strip(),
            full_name=full_name.strip(),
            id_number=id_number.strip(),
            email=email.strip(),
            phone=phone.strip(),
            district=district.strip(),
            registration_date=registration_date or date.today(),
            is_active=True,
        )

        return self._repository.add(recycler)

    def get_all_recyclers(self) -> list:
        return self._repository.get_all()

    def get_recycler_by_id(self, recycler_id: str) -> Recycler:
        self._validate_not_empty(recycler_id, "recycler_id")
        recycler = self._repository.get_by_id(recycler_id.strip())
        if not recycler:
            raise ValueError(f"No se encontro ningun reciclador con el ID '{recycler_id}'.")
        return recycler

    def get_recyclers_by_district(self, district: str) -> list:
        self._validate_not_empty(district, "district")
        return self._repository.get_by_district(district.strip())

    def set_active_status(self, recycler_id: str, is_active: bool) -> Recycler:
        recycler = self.get_recycler_by_id(recycler_id)
        recycler.is_active = is_active
        return self._repository.update(recycler)

    def validate_credentials(self, recycler_id: str, password: str) -> bool:
        recycler = self._repository.get_by_id(recycler_id)
        if not recycler:
            return False
        return recycler.id_number == password

    def update_recycler(
        self,
        recycler_id: str,
        full_name: str | None = None,
        id_number: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        district: str | None = None,
        registration_date: date | None = None,
        is_active: bool | None = None,
    ) -> Recycler:
        recycler = self.get_recycler_by_id(recycler_id)

        if full_name is not None:
            self._validate_not_empty(full_name, "full_name")
            recycler.full_name = full_name.strip()

        if id_number is not None:
            self._validate_not_empty(id_number, "id_number")
            existing_recycler = self._repository.get_by_id_number(id_number.strip())
            if existing_recycler and existing_recycler.recycler_id != recycler.recycler_id:
                raise ValueError(f"Ya existe un reciclador registrado con la cedula '{id_number}'.")
            recycler.id_number = id_number.strip()

        if email is not None:
            self._validate_not_empty(email, "email")
            self._validate_email_format(email)
            recycler.email = email.strip()

        if phone is not None:
            self._validate_not_empty(phone, "phone")
            recycler.phone = phone.strip()

        if district is not None:
            self._validate_not_empty(district, "district")
            recycler.district = district.strip()

        if registration_date is not None:
            recycler.registration_date = registration_date

        if is_active is not None:
            recycler.is_active = is_active

        return self._repository.update(recycler)

    def delete_recycler(self, recycler_id: str) -> None:
        recycler = self.get_recycler_by_id(recycler_id)
        self._repository.delete(recycler)
