"""insert initial catalog data

Revision ID: a5bcaddcc6de
Revises: b70cbc149da7
Create Date: 2026-11-10 14:07:03.289792

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a5bcaddcc6de'
down_revision: Union[str, Sequence[str], None] = 'b70cbc149da7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    monedas = sa.table(
        "monedas",
        sa.column("id", sa.BigInteger()),
        sa.column("codigo", sa.String(3)),
        sa.column("nombre", sa.String(100)),
        sa.column("simbolo", sa.String(10)),
    )

    op.bulk_insert(
        monedas,
        [
            {"id": 1, "codigo": "GBP", "nombre": "Libra esterlina", "simbolo": "£"},
            {"id": 2, "codigo": "JPY", "nombre": "Yen japonés", "simbolo": "¥"},
            {"id": 3, "codigo": "INR", "nombre": "Rupia india", "simbolo": "₹"},
            {"id": 4, "codigo": "DKK", "nombre": "Corona danesa", "simbolo": "kr"},
        ],
    )

    paises = sa.table(
        "paises",
        sa.column("id", sa.BigInteger()),
        sa.column("nombre", sa.String(100)),
        sa.column("codigo", sa.String(2)),
        sa.column("moneda_id", sa.BigInteger()),
    )

    op.bulk_insert(
        paises,
        [
            {"id": 1, "nombre": "Inglaterra", "codigo": "GB", "moneda_id": 1},
            {"id": 2, "nombre": "Japón", "codigo": "JP", "moneda_id": 2},
            {"id": 3, "nombre": "India", "codigo": "IN", "moneda_id": 3},
            {"id": 4, "nombre": "Dinamarca", "codigo": "DK", "moneda_id": 4},
        ],
    )

    ciudades = sa.table(
        "ciudades",
        sa.column("id", sa.BigInteger()),
        sa.column("pais_id", sa.BigInteger()),
        sa.column("nombre", sa.String(150)),
        sa.column("latitud", sa.Float()),
        sa.column("longitud", sa.Float()),
    )

    op.bulk_insert(
        ciudades,
        [
            {"id": 1, "pais_id": 1, "nombre": "Londres", "latitud": 51.5072, "longitud": -0.1276},
            {"id": 2, "pais_id": 1, "nombre": "Mánchester", "latitud": 53.4808, "longitud": -2.2426},
            {"id": 3, "pais_id": 2, "nombre": "Tokio", "latitud": 35.6762, "longitud": 139.6503},
            {"id": 4, "pais_id": 2, "nombre": "Osaka", "latitud": 34.6937, "longitud": 135.5023},
            {"id": 5, "pais_id": 3, "nombre": "Nueva Delhi", "latitud": 28.6139, "longitud": 77.2090},
            {"id": 6, "pais_id": 3, "nombre": "Bombay", "latitud": 19.0760, "longitud": 72.8777},
            {"id": 7, "pais_id": 4, "nombre": "Copenhague", "latitud": 55.6761, "longitud": 12.5683},
            {"id": 8, "pais_id": 4, "nombre": "Aarhus", "latitud": 56.1629, "longitud": 10.2039},
        ],
    )

    for tabla in ("monedas", "paises", "ciudades"):
        op.execute(
            sa.text(
                f"""
                SELECT setval(
                    pg_get_serial_sequence('public.{tabla}', 'id'),
                    COALESCE((SELECT MAX(id) FROM public.{tabla}), 1),
                    EXISTS (SELECT 1 FROM public.{tabla})
                )
                """
            )
        )


def downgrade() -> None:

    op.execute(
        sa.text("""
            DELETE FROM ciudades
            WHERE id BETWEEN 1 AND 8
            AND pais_id BETWEEN 1 AND 4
        """)
    )

    op.execute(
        sa.text("""
            DELETE FROM paises
            WHERE id BETWEEN 1 AND 4
            AND moneda_id BETWEEN 1 AND 4
        """)
    )

    op.execute(
        sa.text("""
            DELETE FROM monedas
            WHERE codigo IN ('GBP', 'JPY', 'INR', 'DKK')
        """)
    )
