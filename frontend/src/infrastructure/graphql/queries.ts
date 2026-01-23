import { gql } from "@apollo/client";

export const STATES_QUERY = gql`
  query States {
    states {
      code
      name
      baseTariffPerKwh
    }
  }
`;

export const QUOTE_QUERY = gql`
  query Quote($stateCode: String!, $consumptionKwh: Float!) {
    quote(stateCode: $stateCode, consumptionKwh: $consumptionKwh) {
      stateCode
      stateName
      baseTariffPerKwh
      consumptionKwh
      baseCost
      solutions {
        solutionType
        bestEconomy
        bestEconomyPercent
        suppliers {
          supplierId
          supplierName
          supplierLogoUrl
          supplierOriginState
          totalCustomers
          averageRating
          solutionType
          costPerKwh
          costTotal
          economy
          economyPercent
        }
      }
    }
  }
`;
