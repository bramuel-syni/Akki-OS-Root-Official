"""Arithmetic only; synthetic quantities do not represent live usage."""
from decimal import Decimal
import pytest
from services.activation.native_joins import usage_totals
from services.northena.execution_models import Held


def test_repeated_units_are_summed_not_silently_overwritten():
    assert usage_totals([{'unit':'tokens','quantity':'100'},{'unit':'tokens','quantity':'1'}]) == {'tokens':Decimal(101)}


@pytest.mark.parametrize('quantity',['NaN','Infinity','-1','not-a-measurement'])
def test_invalid_native_quantities_fail_closed(quantity):
    with pytest.raises(Held,match='CERTIFICATE_NATIVE_USAGE_INVALID'):
        usage_totals([{'unit':'tokens','quantity':quantity}])