from __future__ import annotations
from typing import Any
from ._integration import OdooIntegration


class PartnerModel(OdooIntegration):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def get_partner_by_id(
        self, partner_id: int, fields: list[str] | None = None
    ) -> list[dict[str, Any]]:
        response = self.read("res.partner", [partner_id], fields)
        return response

    def get_partner_id_by_name(
        self, partner_name: str, fields: list[str] | None = None
    ) -> int:
        response = self.search("res.partner", [[["name", "=", partner_name]]], fields)
        if response:
            return response[0]
        raise Exception(f"Partner '{partner_name}' not found")

    def update_partner(
        self,
        partner_id: int,
        partner_data: dict[str, Any],
    ) -> bool:
        response = self.update("res.partner", partner_id, partner_data)
        return response

    def create_partner_from_scratch(
        self,
        partner_data: dict[str, Any],
    ) -> int | list[int]:
        response = self.create("res.partner", [partner_data])
        return response

    def create_partner(
        self,
        name: str,
        street: str,
        city: str,
        state_id: int,
        country_id: int,
        zip_code: str,
        nif: str,
        contact_type: str,
        anf_code: str | None,
        pharmacy_name: str | None,
        owner_name: str | None,
        phone: str | None,
        mobile: str | None,
        email: str | None,
        list_category_id: list[int],
        list_crm_tag_id: list[int],
        vendor_user_id: int | None,
        reference: str | None,
        language: str = "pt_PT",
        is_company: bool = True,
        company_type: str = "company",
    ) -> int | list[int]:
        partner_data = {
            "name": name,
            "street": street,
            "city": city,
            "state_id": state_id,  # "Lisboa", # aqui deve-se buscar o state_id pelo nome do estado
            "country_id": country_id,  # "Portugal", # aqui deve-se buscar o country_id pelo nome do país
            "zip": zip_code,
            "vat": nif,  # NIF
            "x_studio_tipo_de_contacto_1": contact_type,  # Tipo de Contacto
            "x_studio_cdigo_anf_1": anf_code,  # apenas para tipo farmácia
            "x_studio_nome_da_farmcia_1": pharmacy_name,  # apenas para tipo farmácia
            "x_studio_nome_do_proprietrio_1": owner_name,  # apenas para tipo farmácia
            "phone": phone,
            "mobile": mobile,
            "email": email,
            "lang": language,  # idioma
            "category_id": list_category_id,  # Etiquetas / labels - models: res.partner.category - fields: name, active (booleean), parent_id (categoria pai), display_name
            "x_studio_etiquetas_crm": list_crm_tag_id,  # model: crm.tag - fields: name, id, color
            "user_id": vendor_user_id,  # models: res.users - fields: name
            "ref": reference,  # Referência
            "is_company": is_company,  # se é empresa ou não
            "company_type": company_type,  # tipo de empresa
        }
        response = self.create("res.partner", [partner_data])
        return response

    def get_and_read_all_partners(
        self, fields: list[str] | None = None, limit: int = 10, offset: int = 0
    ) -> list[dict[str, Any]]:
        response = self.search_read("res.partner", [], fields or [], limit, offset)
        return response

    def count_partners_by_any_filter(self, filter: list[Any] | None = None) -> int:
        response = self.search_count("res.partner", [filter or []])
        return response

    def get_and_read_partners_by_any_filter(
        self,
        filter: list[Any],
        fields: list[str] | None = None,
        limit: int = 10,
        offset: int = 0,
    ) -> list[dict[str, Any]]:
        response = self.search_read(
            "res.partner", [filter], fields or [], limit, offset
        )
        return response

    def action_archive_partner(self, partner_id: int) -> dict[str, Any]:
        response = self.execute_action("res.partner", "action_archive", partner_id)
        return response
