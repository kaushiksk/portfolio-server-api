from decimal import Decimal
from bson.decimal128 import Decimal128
from bson.codec_options import TypeCodec
from bson.codec_options import TypeRegistry
from bson.codec_options import CodecOptions
import locale

locale.setlocale(locale.LC_NUMERIC, "en_IN")


class DecimalCodec(TypeCodec):
    """DecimalCodec

    MongoDB does not understand the Decimal type
    We will transform it into the Decimal128 type which it understands
    This will help in accurate aggregation etc in queries

    We will read the data back as a localized string"""

    python_type = Decimal
    bson_type = Decimal128

    def transform_python(self, value):
        return Decimal128(value)

    def transform_bson(self, value):
        return locale.format_string("%.4f", value.to_decimal(), grouping=True)


def get_type_registry():
    decimal_codec = DecimalCodec()
    type_registry = TypeRegistry([decimal_codec])
    return type_registry
