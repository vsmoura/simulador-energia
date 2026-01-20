from app.graphql.schema import schema


def test_states_query_returns_data(build_context) -> None:
    query = """
        query {
            states {
                code
                name
                baseTariffPerKwh
            }
        }
    """
    result = schema.execute_sync(query, context_value=build_context)

    assert result.errors is None
    assert result.data["states"]


def test_quote_query_returns_solutions(build_context) -> None:
    query = """
        query GetQuote($stateCode: String!, $consumptionKwh: Float!) {
            quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
                stateCode
                baseCost
                solutions {
                    solutionType
                    bestEconomy
                }
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"stateCode": "SP", "consumptionKwh": 30000},
        context_value=build_context,
    )

    assert result.errors is None
    assert result.data["quote"]["solutions"]


def test_quote_query_invalid_consumption_returns_error(build_context) -> None:
    query = """
        query GetQuote($stateCode: String!, $consumptionKwh: Float!) {
            quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
                stateCode
            }
        }
    """
    result = schema.execute_sync(
        query,
        variable_values={"stateCode": "SP", "consumptionKwh": 0},
        context_value=build_context,
    )

    assert result.errors
    assert result.errors[0].extensions["code"] == "INVALID_CONSUMPTION"